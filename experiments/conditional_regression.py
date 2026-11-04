"""OU correlations and conditional-mean learning with a Gaussian baseline."""

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from probflow.gaussian import CoupledOU
from probflow.learning import fit_conditional_y_given_x
from _paths import OutputPaths, write_rows


def require_torch():
    """Load the optional training dependency only for neural experiments."""
    try:
        import torch
    except ImportError as exc:
        raise RuntimeError(
            'Install neural dependencies with python -m pip install -e ".[experiments]", '
            "or pass --skip-neural."
        ) from exc
    return torch


def sample_slices(rng, count, times, parameters):
    """Draw (time, X) features, noisy Y labels, and exact E[Y | X, time].

    Time indices are sampled uniformly, so counts per slice fluctuate.
    Float32 conversion and random draw order match the original benchmark.
    """
    ids = rng.integers(0, len(times), size=count)
    features = np.zeros((count, 2))
    labels = np.zeros((count, 1))
    targets = np.zeros((count, 1))
    for j, (mean, covariance, slope, intercept) in enumerate(parameters):
        mask = ids == j
        size = int(mask.sum())
        if size:
            pairs = rng.multivariate_normal(mean, covariance, size=size)
            features[mask] = np.column_stack((np.full(size, times[j]), pairs[:, 0]))
            labels[mask, 0] = pairs[:, 1]
            targets[mask, 0] = slope * pairs[:, 0] + intercept
    permutation = rng.permutation(count)
    return tuple(values[permutation].astype("float32") for values in (features, labels, targets))


def train_neural(rng, count, times, parameters, test_features, epochs=260):
    """Fit the original two-layer network using training-only normalization."""
    torch = require_torch()
    nn = torch.nn
    features, labels, _ = sample_slices(rng, count, times, parameters)
    x_mean, x_std = features.mean(axis=0), features.std(axis=0)
    y_mean, y_std = labels.mean(axis=0), labels.std(axis=0)
    inputs = torch.tensor((features - x_mean) / x_std)
    outputs = torch.tensor((labels - y_mean) / y_std)
    model = nn.Sequential(
        nn.Linear(2, 48),
        nn.Tanh(),
        nn.Linear(48, 48),
        nn.Tanh(),
        nn.Linear(48, 1),
    )
    optimizer = torch.optim.Adam(model.parameters(), lr=0.008)
    for _ in range(epochs):
        for batch in torch.randperm(count).split(256):
            prediction = model(inputs[batch])
            loss = ((prediction - outputs[batch]) ** 2).mean()
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
    with torch.no_grad():
        prediction = model(torch.tensor((test_features - x_mean) / x_std)).numpy() * y_std + y_mean
    return prediction.ravel()


def plot_correlations(model: CoupledOU, paths: OutputPaths) -> None:
    times = np.linspace(0, 4, 180)
    full = [model.stationary_correlation(float(t)) for t in times]
    closure = model.free_energy_correlation(times)
    fig, ax = plt.subplots(figsize=(6.1, 4.2))
    ax.plot(times, full, label="Microscopic 2D OU projected on X", lw=2)
    ax.plot(times, closure, "--", label="Equilibrium Markov closure", lw=2)
    ax.set(
        xlabel="Time lag t",
        ylabel="Stationary covariance C(t)",
        title="Equal marginals, different temporal correlations",
    )
    ax.legend()
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    fig.savefig(paths.figures / "ou_correlation.pdf")
    plt.close(fig)


def run(paths: OutputPaths, *, seed: int, neural: bool = True) -> dict:
    """Run affine and optional neural fits without changing saved results by import."""
    rng = np.random.default_rng(seed)
    if neural:
        torch = require_torch()
        torch.manual_seed(seed)
        torch.set_num_threads(2)
    # Manuscript parameters are explicit; library defaults describe another case.
    model = CoupledOU(a=0.8, c=1.7, kappa=1.1, beta=1.0)
    mean0, covariance0 = np.array([1.0, -0.8]), np.diag([0.12, 0.25])
    times = np.array([0.25, 0.5, 1.0, 2.0])
    parameters = []
    for t in times:
        mean, covariance = model.moments(t, mean0, covariance0)
        intercept, slope = model.conditional_y_coefficients(t, mean0, covariance0)
        parameters.append((mean, covariance, slope, intercept))
    plot_correlations(model, paths)
    test_features, test_labels, target = sample_slices(rng, 12000, times, parameters)
    drift_scale = abs(model.c * model.kappa)
    affine_rows = []
    # Preserve the historical RNG stream: test set, both affine fits, both networks.
    # Affine and neural fits share the test set but draw separate training samples.
    for count in [512, 4096]:
        features, labels, _ = sample_slices(rng, count, times, parameters)
        prediction = np.zeros(len(test_features))
        for t in times:
            train_mask = features[:, 0] == t
            test_mask = test_features[:, 0] == t
            intercept, slope = fit_conditional_y_given_x(
                features[train_mask, 1], labels[train_mask, 0]
            )
            # Keep float64 arithmetic: Python scalars can promote float32 features
            # differently across NumPy versions and change the reported RMSE.
            prediction[test_mask] = (
                np.float64(intercept) + np.float64(slope) * test_features[test_mask, 1]
            )
        error = float(np.sqrt(np.mean((prediction - target.ravel()) ** 2)))
        affine_rows.append(
            {
                "train_samples": count,
                "conditional_mean_RMSE": error,
                "projected_drift_RMSE": drift_scale * error,
            }
        )
    write_rows(paths.results / "affine_regression.csv", affine_rows)
    neural_rows, predictions = [], {}
    if neural:
        for count in [512, 4096]:
            prediction = train_neural(rng, count, times, parameters, test_features)
            error = np.sqrt(np.mean((prediction - target.ravel()) ** 2))
            neural_rows.append(
                {
                    "train_samples": count,
                    "test_samples": len(test_features),
                    "conditional_mean_RMSE": float(error),
                    "projected_drift_RMSE": float(drift_scale * error),
                    "noisy_Y_RMSE": float(
                        np.sqrt(np.mean((prediction - test_labels.ravel()) ** 2))
                    ),
                }
            )
            predictions[count] = prediction
        write_rows(paths.results / "conditional_regression.csv", neural_rows)
        # Plot held-out predictions at t=1; do not retrain just to draw a curve.
        _, _, slope, intercept = parameters[2]
        grid = np.linspace(-2.1, 2.1, 180)
        indices = np.flatnonzero(test_features[:, 0] == times[2])[::13]
        fig, ax = plt.subplots(figsize=(6.1, 4.2))
        ax.scatter(
            test_features[indices, 1],
            predictions[4096][indices],
            s=8,
            alpha=0.45,
            label="Neural prediction (held-out)",
        )
        ax.plot(grid, slope * grid + intercept, lw=2, color="black", label="Exact conditional mean")
        ax.set(
            xlabel="Collective variable x",
            ylabel="E[Y | X=x, t=1]",
            title="Learning a conditional coefficient for the projected dynamics",
        )
        ax.legend()
        ax.grid(True, alpha=0.25)
        fig.tight_layout()
        fig.savefig(paths.figures / "conditional_regression.pdf")
        plt.close(fig)
    return {
        "K": model.H.tolist(),
        "Sigma_infinity": model.invariant_cov.tolist(),
        "ML": neural_rows,
        "Affine": affine_rows,
        "OU_Cfull_t1": model.stationary_correlation(1.0),
        "OU_Cclosure_t1": float(model.free_energy_correlation(1.0)),
    }
