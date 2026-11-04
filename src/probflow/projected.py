"""Moment evolution for time-dependent projection and equilibrium closure."""

import numpy as np
from scipy.integrate import solve_ivp

from .gaussian import CoupledOU


def solve_projected_moments(
    model: CoupledOU,
    times,
    mean0,
    cov0,
    *,
    rtol=1e-10,
    atol=1e-12,
) -> tuple[np.ndarray, np.ndarray]:
    """Integrate m'=A(t)m+B(t), v'=2A(t)v+2/beta from time zero.

    Observation times may be nondecreasing and repeated; the initial moments
    always refer to time zero, even when the first observation is later.
    """
    times = np.asarray(times, dtype=float)
    if (
        times.ndim != 1
        or len(times) == 0
        or not np.all(np.isfinite(times))
        or np.any(np.diff(times) < 0)
        or times[0] < 0
    ):
        raise ValueError("times must be finite, sorted, non-negative 1D values")
    mean0 = np.asarray(mean0, dtype=float).reshape(2)
    cov0 = np.asarray(cov0, dtype=float).reshape(2, 2)
    if times[-1] == 0:
        return np.full(times.shape, mean0[0]), np.full(times.shape, cov0[0, 0])

    def rhs(t, state):
        slope, offset = model.projected_coefficients(t, mean0, cov0)
        mean, variance = state
        return [slope * mean + offset, 2 * slope * variance + 2 / model.beta]

    # solve_ivp requires strictly increasing t_eval; restore repeated requests.
    unique_times, inverse = np.unique(times, return_inverse=True)
    solution = solve_ivp(
        rhs,
        (0, float(times[-1])),
        [float(mean0[0]), float(cov0[0, 0])],
        t_eval=unique_times,
        rtol=rtol,
        atol=atol,
    )
    if not solution.success:
        raise RuntimeError(solution.message)
    return solution.y[0, inverse], solution.y[1, inverse]


def equilibrium_closure_moments(model: CoupledOU, times, mean0, cov0):
    """Moments of the closure using only equilibrium free energy F(z)=a*z**2/2."""
    times = np.asarray(times, dtype=float)
    mean = mean0[0] * np.exp(-model.a * times)
    stationary_variance = 1 / (model.beta * model.a)
    variance = stationary_variance + (cov0[0, 0] - stationary_variance) * np.exp(
        -2 * model.a * times
    )
    return mean, variance
