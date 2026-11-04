"""Exact Gaussian formulas for a coupled two-dimensional Langevin diffusion.

The potential is V(x, y) = a*x**2/2 + c*(y-kappa*x)**2/2.
The SDE is dZ = -H Z dt + sqrt(2/beta) dW, with H the potential Hessian.
"""

from dataclasses import dataclass

import numpy as np
from scipy.linalg import expm


@dataclass(frozen=True)
class CoupledOU:
    """Parameters of a confining quadratic potential and inverse temperature."""

    a: float = 1.0
    c: float = 2.0
    kappa: float = 1.5
    beta: float = 1.5

    def __post_init__(self):
        if not np.all(np.isfinite([self.a, self.c, self.kappa, self.beta])):
            raise ValueError("model parameters must be finite")
        if min(self.a, self.c, self.beta) <= 0:
            raise ValueError("a, c, beta must be positive")

    @property
    def H(self) -> np.ndarray:
        """Positive-definite potential Hessian (called K in the manuscript)."""
        a, c, k = self.a, self.c, self.kappa
        return np.array([[a + c * k**2, -c * k], [-c * k, c]])

    @property
    def invariant_cov(self) -> np.ndarray:
        """Equilibrium covariance satisfying H S + S H = 2 I / beta."""
        return np.linalg.inv(self.H) / self.beta

    def propagator(self, t: float) -> np.ndarray:
        """Return exp(-t H) using the same backend as the manuscript benchmark."""
        if not np.isfinite(t) or t < 0:
            raise ValueError("t must be finite and non-negative")
        return expm(-self.H * t)

    def moments(self, t, mean0, cov0) -> tuple[np.ndarray, np.ndarray]:
        """Mean and covariance at t for a Gaussian initial distribution."""
        mean0 = np.asarray(mean0, dtype=float).reshape(2)
        cov0 = np.asarray(cov0, dtype=float).reshape((2, 2))
        evolution = self.propagator(t)
        stationary = self.invariant_cov
        return evolution @ mean0, stationary + evolution @ (cov0 - stationary) @ evolution.T

    def conditional_y_coefficients(self, t, mean0, cov0) -> tuple[float, float]:
        """Return (intercept, slope) of E[Y_t | X_t=z]."""
        mean, cov = self.moments(t, mean0, cov0)
        if cov[0, 0] <= 0:
            raise ValueError("X marginal must have positive variance")
        slope = cov[1, 0] / cov[0, 0]
        return float(mean[1] - slope * mean[0]), float(slope)

    def projected_coefficients(self, t, mean0, cov0) -> tuple[float, float]:
        """Return (slope, offset) of the conditional drift b(t,z).

        The projected scalar SDE has diffusion sqrt(2/beta). Matching its
        one-time marginals does not imply matching temporal correlations.
        """
        intercept, conditional_slope = self.conditional_y_coefficients(t, mean0, cov0)
        slope = -self.a + self.c * self.kappa * (conditional_slope - self.kappa)
        offset = self.c * self.kappa * intercept
        return float(slope), float(offset)

    def stationary_correlation(self, t: float) -> float:
        """Return Cov(X_0, X_t) at equilibrium, without normalization."""
        return float((self.propagator(t) @ self.invariant_cov)[0, 0])

    def free_energy_correlation(self, t):
        """Stationary covariance of the equilibrium free-energy OU closure."""
        return np.exp(-self.a * t) / (self.beta * self.a)


def gaussian_kl(m1, v1, m2, v2):
    """Return KL(N(m1,v1) || N(m2,v2)); v1 and v2 are positive variances."""
    if min(v1, v2) <= 0:
        raise ValueError("variances must be positive")
    return 0.5 * (np.log(v2 / v1) + (v1 + (m1 - m2) ** 2) / v2 - 1.0)
