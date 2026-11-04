"""Conservative finite-volume Markov evolution with reflecting boundaries."""

import numpy as np
from scipy.sparse.linalg import expm_multiply

from _paths import OutputPaths, write_rows


def generator(cells: int = 60, diffusion: float = 0.5) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return a column generator, invariant masses, and cell centers.

    Columns sum to zero because masses evolve as m' = Q m. Each edge
    satisfies detailed balance; omitted exterior edges impose no flux.
    """
    if cells < 2 or diffusion <= 0:
        raise ValueError("cells must be at least two and diffusion must be positive")
    h = 1.0 / cells
    x = (np.arange(cells) + 0.5) * h
    potential = 2 * (x - 0.3) ** 2 + 0.7 * x
    forward = diffusion / h**2 * np.exp(-(potential[1:] - potential[:-1]) / (2 * diffusion))
    backward = diffusion / h**2 * np.exp((potential[1:] - potential[:-1]) / (2 * diffusion))
    matrix = np.zeros((cells, cells))
    for i in range(cells - 1):
        matrix[i + 1, i] += forward[i]
        matrix[i, i] -= forward[i]
        matrix[i, i + 1] += backward[i]
        matrix[i + 1, i + 1] -= backward[i]
    invariant = np.exp(-potential / diffusion)
    invariant /= invariant.sum()
    return matrix, invariant, x


def run(paths: OutputPaths) -> dict:
    """Save mass, positivity, and relative entropy at fixed observation times."""
    matrix, invariant, x = generator()
    initial = np.exp(-(((x - 0.75) / 0.11) ** 2))
    initial /= initial.sum()
    rows = []
    for t in [0.0, 0.015, 0.05, 0.2, 0.5]:
        masses = expm_multiply(matrix * t, initial)
        rows.append(
            {
                "time": t,
                "mass": float(masses.sum()),
                "minimum_cell_mass": float(masses.min()),
                "KL_to_pi": float(np.dot(masses, np.log(masses / invariant))),
            }
        )
    write_rows(paths.results / "markov_semidiscrete.csv", rows)
    return {"Markov": rows}
