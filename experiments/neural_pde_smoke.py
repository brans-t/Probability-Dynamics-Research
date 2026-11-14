"""Reproducible 2D integration check for Chapter 2; not a generalization study."""

import argparse
import json
from pathlib import Path
import platform
import sys
import time

import numpy as np
import scipy

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def run_smoke(*, seed=20261115, n=32, steps=12):
    # Lazy import keeps the experiment importable without optional torch.
    import torch
    from probflow.neural_pde_solver import (
        FNO2d,
        drift,
        enforce_boundary,
        fno_loss,
        pinn_failure_values,
        sample_fourier_field,
        solve_reference,
        train_fno,
    )

    torch.manual_seed(seed)
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    start = time.perf_counter()
    length, epsilon = 20.0, 0.5
    # Literal repeated b from the source, supplied explicitly. No invented c.
    centers_b = [[1.0, 1.0], [1.0, 1.0]]
    modes = [[1, 0], [0, 1], [1, 1], [1, -1], [2, 0], [0, 2]]
    fields = [sample_fourier_field(2, modes, seed=seed + i, length=length) for i in range(6)]
    references = [solve_reference(f, centers_b=centers_b, n=n, epsilon=epsilon) for f in fields]
    points = torch.tensor(references[0].points, dtype=torch.float32)
    inputs = torch.stack([f(points) for f in fields])[:, None]
    targets = torch.tensor(np.stack([ref.q for ref in references]), dtype=torch.float32)[:, None]
    velocities = torch.stack(
        [drift(points, f, periodize=True, length=length).detach() for f in fields]
    )
    a, b = references[0].mask_a, references[0].mask_b
    model = FNO2d(width=8, modes=4, depth=2)

    def metrics(indices):
        model.eval()
        with torch.no_grad():
            total, terms = fno_loss(
                model,
                inputs[indices],
                targets[indices],
                velocities[indices],
                a,
                b,
                epsilon=epsilon,
                h=length / n,
            )
            q = enforce_boundary(model(inputs[indices])[:, 0], torch.tensor(a), torch.tensor(b))
            error = q - targets[indices, 0]
            return {
                "loss": float(total),
                **{k: float(v) for k, v in terms.items()},
                "rmse": float(error.square().mean().sqrt()),
                "relative_l2": float(error.norm() / targets[indices, 0].norm()),
                "max_error": float(error.abs().max()),
                "q_min": float(q.min()),
                "q_max": float(q.max()),
            }

    before = metrics(slice(0, 4))
    history = train_fno(
        model,
        inputs[:4],
        targets[:4],
        velocities[:4],
        a,
        b,
        epsilon=epsilon,
        h=length / n,
        steps=steps,
        learning_rate=0.003,
    )
    after, held_out = metrics(slice(0, 4)), metrics(slice(4, 6))
    # Grid comparisons share nodes. Masks change with resolution: do not infer
    # an order of convergence from these two differences.
    refinement = [references[0]]
    for size in [2 * n, 4 * n]:
        refinement.append(solve_reference(fields[0], centers_b=centers_b, n=size, epsilon=epsilon))
    differences = []
    for coarse, fine in zip(refinement[:-1], refinement[1:]):
        differences.append(float(np.sqrt(np.mean((coarse.q - fine.q[::2, ::2]) ** 2))))
    xx = torch.arange(256, dtype=torch.float64) * 2 * np.pi / 256
    tt = torch.linspace(0, 1, 11, dtype=xx.dtype)
    u, exact, residual = pinn_failure_values(xx[:, None], tt[None], 64)
    report = {
        "status": "executed integration smoke test; accuracy/generalization study planned",
        "environment": {
            "python": platform.python_version(),
            "torch": torch.__version__,
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "device": "cpu",
        },
        "config": {
            "seed": seed,
            "n": n,
            "length": length,
            "epsilon": epsilon,
            "radius": 0.5,
            "centers_b": centers_b,
            "potential": "periodized Gaussian lattice sum",
            "pde": "+epsilon*Delta(q) + (-grad(V))*grad(q) = 0",
            "normalization": "L2(f)/volume = 0.1 (not RMS)",
            "train_samples": 4,
            "held_out_samples": 2,
            "steps": steps,
            "learning_rate": 0.003,
            "width": 8,
            "spectral_modes": 4,
            "depth": 2,
            "loss_weights": [1.0, 0.01, 1.0, 1.0],
            "fourier_modes": modes,
        },
        "fields": [
            {
                "seed": seed + i,
                "cosine": f.cosine.tolist(),
                "sine": f.sine.tolist(),
                "l2_per_volume": f.l2_norm / f.volume,
            }
            for i, f in enumerate(fields)
        ],
        "reference_max_algebraic_residual": max(ref.residual_max for ref in references),
        "refinement": {
            "n": [n, 2 * n, 4 * n],
            "successive_grid_rmse": differences,
            "interpretation": "diagnostic only; voxelized geometry changes with mesh",
        },
        "training_before": before,
        "training_after": after,
        "held_out": held_out,
        "history": history,
        "pinn_example": {
            "k": 64,
            "time_spacing": 0.1,
            "max_empirical_residual": float(residual.abs().max()),
            "max_error_at_positive_sample_times": float((u[:, 1:] - exact[:, 1:]).abs().max()),
            "mass_error": float(((2 * np.pi) * u.mean(0) - 1).abs().max()),
        },
        "elapsed_seconds": time.perf_counter() - start,
    }
    if after["loss"] >= before["loss"]:
        raise AssertionError("smoke training did not reduce its joint objective")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=ROOT)
    parser.add_argument("--seed", type=int, default=20261115)
    parser.add_argument("--n", type=int, default=32)
    parser.add_argument("--steps", type=int, default=12)
    args = parser.parse_args()
    report = run_smoke(seed=args.seed, n=args.n, steps=args.steps)
    destination = args.output_root.resolve() / "results/neural_pde/smoke.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "output": str(destination),
                "training_loss_before": report["training_before"]["loss"],
                "training_loss_after": report["training_after"]["loss"],
                "held_out_rmse": report["held_out"]["rmse"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
