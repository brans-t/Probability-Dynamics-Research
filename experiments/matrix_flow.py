"""Noncommuting matrix flows and Jacobian determinant convergence."""

import matplotlib
import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import expm

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from _paths import OutputPaths, write_rows


def coefficient(t: float) -> np.ndarray:
    """Time-dependent coefficient of U' = A(t) U on [0, 1]."""
    return np.array([[-0.25, 1.0 + t], [-0.6 + 0.3 * t, 0.10]])


def fundamental_matrix(steps: int, method: str) -> np.ndarray:
    """Integrate the matrix IVP with explicit Euler or classical RK4."""
    if steps < 1 or method not in {"Euler", "RK4"}:
        raise ValueError("steps must be positive and method must be Euler or RK4")
    h = 1.0 / steps
    matrix = np.eye(2)
    for k in range(steps):
        t = k * h
        if method == "Euler":
            matrix = (np.eye(2) + h * coefficient(t)) @ matrix
        else:
            k1 = coefficient(t) @ matrix
            k2 = coefficient(t + h / 2) @ (matrix + h * k1 / 2)
            k3 = coefficient(t + h / 2) @ (matrix + h * k2 / 2)
            k4 = coefficient(t + h) @ (matrix + h * k3)
            matrix = matrix + h * (k1 + 2 * k2 + 2 * k3 + k4) / 6
    return matrix


def run(paths: OutputPaths) -> dict:
    """Save determinant errors and quantify the unordered-exponential error."""
    solution = solve_ivp(
        lambda t, y: (coefficient(t) @ y.reshape(2, 2)).ravel(),
        [0, 1],
        np.eye(2).ravel(),
        rtol=1e-13,
        atol=1e-14,
    )
    if not solution.success:
        raise RuntimeError(solution.message)
    reference = solution.y[:, -1].reshape(2, 2)
    # Liouville's identity remains exact even though A(t) does not commute.
    exact_determinant = np.exp(-0.15)
    assert abs(np.linalg.det(reference) - exact_determinant) < 1e-10
    rows = []
    for steps in [8, 16, 32, 64, 128]:
        euler = np.linalg.det(fundamental_matrix(steps, "Euler"))
        rk4 = np.linalg.det(fundamental_matrix(steps, "RK4"))
        rows.append(
            {
                "N": steps,
                "h": 1 / steps,
                "Euler_det": euler,
                "Euler_error": abs(euler - exact_determinant),
                "RK4_det": rk4,
                "RK4_error": abs(rk4 - exact_determinant),
            }
        )
    write_rows(paths.results / "jacobian_convergence.csv", rows)
    fig, ax = plt.subplots(figsize=(6.1, 4.2))
    for method in ("Euler", "RK4"):
        ax.loglog([r["h"] for r in rows], [r[f"{method}_error"] for r in rows], "-o", label=method)
    ax.set(
        xlabel="Step size h",
        ylabel="Absolute error in det U(1,0)",
        title="Jacobian determinant convergence",
    )
    ax.legend()
    ax.grid(True, alpha=0.25, which="both")
    fig.tight_layout()
    fig.savefig(paths.figures / "jacobian_convergence.pdf")
    plt.close(fig)
    integral = np.array([[-0.25, 1.5], [-0.45, 0.10]])
    return {
        "det_exact": exact_determinant,
        "matrix_exponential_false_frobenius_error": np.linalg.norm(
            reference - expm(integral), ord="fro"
        ),
        "A_commutator_frobenius_norm": np.linalg.norm(
            coefficient(0) @ coefficient(1) - coefficient(1) @ coefficient(0), ord="fro"
        ),
        "Jacobian": rows,
    }
