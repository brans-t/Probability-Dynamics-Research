"""Exactly solvable 2D Langevin dynamics and its time-dependent Markovian projection.

All derivatives refer to the coordinate X, for the potential
V(x,y)=a*x^2/2 + c*(y-kappa*x)^2/2, a,c,beta>0.
"""
from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class CoupledOU:
    a: float = 1.0
    c: float = 2.0
    kappa: float = 1.5
    beta: float = 1.5

    def __post_init__(self):
        if min(self.a, self.c, self.beta) <= 0:
            raise ValueError('a, c, beta must be positive')

    @property
    def H(self):
        a, c, k = self.a, self.c, self.kappa
        return np.array([[a + c*k*k, -c*k], [-c*k, c]], dtype=float)

    @property
    def invariant_cov(self):
        return np.linalg.inv(self.H) / self.beta

    def propagator(self, t):
        if t < 0:
            raise ValueError('t must be non-negative')
        val, vec = np.linalg.eigh(self.H)
        return (vec * np.exp(-val*t)) @ vec.T

    def moments(self, t, mean0, cov0):
        """Gaussian OU marginals at t given a Gaussian initial distribution."""
        mean0 = np.asarray(mean0, dtype=float).reshape(2)
        cov0 = np.asarray(cov0, dtype=float).reshape((2, 2))
        E = self.propagator(t)
        inv = self.invariant_cov
        return E@mean0, inv + E@(cov0-inv)@E.T

    def projected_coefficients(self, t, mean0, cov0):
        """The exact affine conditional-mean drift b(t,z)=slope*z+offset.

        The scalar Markovian mimicking SDE has diffusion sqrt(2/beta).
        """
        mean, cov = self.moments(t, mean0, cov0)
        if cov[0,0] <= 0:
            raise ValueError('X marginal must have positive variance')
        r = cov[1,0]/cov[0,0]
        slope = -self.a + self.c*self.kappa*(r-self.kappa)
        offset = self.c*self.kappa*(mean[1]-r*mean[0])
        return float(slope), float(offset)

    def stationary_correlation(self, t):
        """Cov(X_0, X_t) at equilibrium, not normalized."""
        return float((self.propagator(t) @ self.invariant_cov)[0,0])

    def free_energy_correlation(self, t):
        """Stationary covariance of equilibrium free-energy closure OU model."""
        return np.exp(-self.a*t)/(self.beta*self.a)


def gaussian_kl(m1, v1, m2, v2):
    """KL(N(m1,v1)||N(m2,v2)), variances strictly positive."""
    if min(v1, v2) <= 0:
        raise ValueError('variances must be positive')
    return 0.5*(np.log(v2/v1) + (v1+(m1-m2)**2)/v2-1.0)
