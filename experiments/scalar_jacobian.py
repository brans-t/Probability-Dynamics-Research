"""High-precision Euler/RK4 flow-Jacobian convergence for x' = x on [0, 1]."""

from decimal import Decimal, localcontext

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from _paths import OutputPaths, argument_parser, write_rows


def numerical_jacobians(steps: int) -> tuple[Decimal, Decimal]:
    """Integrate M' = M, M(0) = 1 using the active Decimal precision."""
    if steps < 1:
        raise ValueError("steps must be positive")
    h = Decimal(1) / steps
    euler = rk4 = Decimal(1)
    for _ in range(steps):
        euler += h * euler
        k1 = rk4
        k2 = rk4 + h * k1 / 2
        k3 = rk4 + h * k2 / 2
        k4 = rk4 + h * k3
        rk4 += h * (k1 + 2 * k2 + 2 * k3 + k4) / 6
    return euler, rk4


def convergence_rows(precision: int = 80) -> list[dict]:
    """Orders compare each row with the next finer mesh; the last is blank."""
    with localcontext() as context:
        context.prec = precision
        exact = Decimal(1).exp()
        rows = []
        for steps in (4, 8, 16, 32, 64, 128):
            euler, rk4 = numerical_jacobians(steps)
            rows.append(
                {
                    "K": steps,
                    "h": Decimal(1) / steps,
                    "Euler_det": euler,
                    "RK4_det": rk4,
                    "Euler_error": abs(euler - exact),
                    "RK4_error": abs(rk4 - exact),
                    "Euler_order": "",
                    "RK4_order": "",
                }
            )
        for coarse, fine in zip(rows, rows[1:]):
            for method in ("Euler", "RK4"):
                coarse[f"{method}_order"] = (
                    coarse[f"{method}_error"] / fine[f"{method}_error"]
                ).ln() / Decimal(2).ln()
        return rows


def run(paths: OutputPaths) -> list[dict]:
    rows = convergence_rows()
    paths.prepare()
    write_rows(paths.results / "scalar_jacobian_convergence.csv", rows)
    h = [float(row["h"]) for row in rows]
    with plt.rc_context({"font.size": 11, "legend.fontsize": 10}):
        fig, ax = plt.subplots(figsize=(6.4, 4.2), layout="constrained")
        for method, color, marker in (("Euler", "#0072B2", "o"), ("RK4", "#D55E00", "s")):
            ax.loglog(
                h, [float(row[f"{method}_error"]) for row in rows],
                color=color, marker=marker, linewidth=1.6, label=method,
            )
        exact = float(Decimal(1).exp())
        ax.loglog(
            h, [exact * step / 2 for step in h], "--", color="#555555", label=r"$(e/2)h$",
        )
        ax.loglog(
            h, [exact * step**4 / 120 for step in h], ":", color="#555555", label=r"$(e/120)h^4$",
        )
        ax.set(xlabel=r"Step size $h=1/K$", ylabel=r"Absolute Jacobian error $|\widehat J_K-e|$")
        ax.grid(True, which="both", alpha=0.2)
        ax.legend(ncol=2)
        fig.savefig(paths.figures / "scalar_jacobian_convergence.pdf")
        plt.close(fig)
    return rows


def main() -> None:
    args = argument_parser(__doc__).parse_args()
    rows = run(OutputPaths(args.output_root.resolve()))
    print("K h Euler_error RK4_error Euler_order RK4_order")
    for row in rows:
        orders = [
            f"{row[f'{method}_order']:.4f}" if row[f"{method}_order"] != "" else "--"
            for method in ("Euler", "RK4")
        ]
        print(
            f"{row['K']} {row['h']} {row['Euler_error']:.6E} "
            f"{row['RK4_error']:.6E} {' '.join(orders)}"
        )


if __name__ == "__main__":
    main()
