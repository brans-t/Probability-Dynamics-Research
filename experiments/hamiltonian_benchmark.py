"""Deterministic numerical check for the Hamiltonian section (Project 10).
Execute from the repository root with python experiments/hamiltonian_benchmark.py.
Data: results/benchmarks/; manuscript figures: paper/figures/.
"""

import csv
import json
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from _paths import OutputPaths, argument_parser


def run(paths: OutputPaths) -> None:
    """Compare Euler and velocity Verlet at the manuscript parameters."""
    omega = 1.0
    h = 0.1
    steps = 1000
    q0, p0 = 1.0, 0.0
    euler_q, euler_p = q0, p0
    verlet_q, verlet_p = q0, p0
    rows = []
    for n in range(steps + 1):
        t = n * h
        exact_energy = 0.5 * (q0**2 * omega**2 + p0**2)
        euler_energy = 0.5 * (omega**2 * euler_q * euler_q + euler_p * euler_p)
        verlet_energy = 0.5 * (omega**2 * verlet_q * verlet_q + verlet_p * verlet_p)
        modified_energy = 0.5 * (
            verlet_p * verlet_p + omega**2 * (1 - omega**2 * h * h / 4) * verlet_q * verlet_q
        )
        rows.append(
            (
                n,
                t,
                exact_energy,
                euler_energy,
                verlet_energy,
                modified_energy,
                euler_q,
                euler_p,
                verlet_q,
                verlet_p,
            )
        )
        # Use the old q and p simultaneously; an in-place update would change the method.
        euler_q, euler_p = euler_q + h * euler_p, euler_p - h * omega**2 * euler_q
        # Symmetric kick-drift-kick splitting preserves the discrete symplectic structure.
        half_momentum = verlet_p - (h / 2) * omega**2 * verlet_q
        verlet_q = verlet_q + h * half_momentum
        verlet_p = half_momentum - (h / 2) * omega**2 * verlet_q
    with (paths.results / "hamiltonian_energy.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "step",
                "time",
                "exact_energy",
                "euler_energy",
                "verlet_energy",
                "verlet_modified_energy",
                "euler_q",
                "euler_p",
                "verlet_q",
                "verlet_p",
            ]
        )
        writer.writerows(rows)
    trajectory = np.array(rows)
    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.semilogy(trajectory[:, 1], trajectory[:, 3], label="Explicit Euler: true energy")
    ax.semilogy(trajectory[:, 1], trajectory[:, 4], label="Velocity Verlet: true energy")
    ax.semilogy(
        trajectory[:, 1], trajectory[:, 5], label="Velocity Verlet: modified energy", linestyle="--"
    )
    ax.axhline(0.5, linestyle=":", color="black", label="Exact energy")
    ax.set(
        xlabel="Time",
        ylabel="Energy (logarithmic scale)",
        title="Harmonic oscillator: geometric versus non-symplectic integration",
    )
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(paths.figures / "hamiltonian_energy.pdf")
    plt.close(fig)

    phase_mask = trajectory[:, 1] <= 20
    fig, ax = plt.subplots(figsize=(6.6, 4.5))
    ax.plot(trajectory[phase_mask, 6], trajectory[phase_mask, 7], label="Explicit Euler", alpha=0.9)
    ax.plot(
        trajectory[phase_mask, 8], trajectory[phase_mask, 9], label="Velocity Verlet", alpha=0.9
    )
    exact_q = np.cos(np.linspace(0, 20, 1000))
    exact_p = -np.sin(np.linspace(0, 20, 1000))
    ax.plot(exact_q, exact_p, "k--", label="Exact orbit", alpha=0.7)
    ax.set(xlabel="q", ylabel="p", title="Phase-space trajectories over 20 time units")
    ax.set_aspect("equal", "box")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(paths.figures / "hamiltonian_phase.pdf")
    plt.close(fig)
    summary = {
        "h": h,
        "N": steps,
        "T": steps * h,
        "exact_energy": trajectory[0, 2],
        "euler_final_energy": trajectory[-1, 3],
        "verlet_final_energy": trajectory[-1, 4],
        "euler_energy_relative_drift": abs(trajectory[-1, 3] - 0.5) / 0.5,
        "verlet_max_energy_abs_error": max(abs(trajectory[:, 4] - 0.5)),
        "verlet_max_modified_energy_abs_drift": max(abs(trajectory[:, 5] - trajectory[0, 5])),
    }
    (paths.results / "hamiltonian_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    print(summary)


def main(argv: list[str] | None = None) -> None:
    args = argument_parser(__doc__).parse_args(argv)
    paths = OutputPaths(args.output_root.resolve())
    paths.prepare()
    run(paths)


if __name__ == "__main__":
    main()
