"""Moment ODE for the exact time-inhomogeneous Markovian projection.

If b(t,z)=A(t)z+B(t) and diffusion sqrt(2/beta), then
m'=A*m+B, var'=2*A*var+2/beta.
"""
import numpy as np
from scipy.integrate import solve_ivp


def solve_projected_moments(model, times, mean0, cov0, *, rtol=1e-10, atol=1e-12):
    times = np.asarray(times, dtype=float)
    if times.ndim != 1 or len(times) == 0 or np.any(np.diff(times) < 0) or times[0] < 0:
        raise ValueError('times must be sorted non-negative 1D values')
    if times[-1] == 0:
        return np.full(times.shape, mean0[0]), np.full(times.shape, cov0[0,0])

    def rhs(t, state):
        slope, offset = model.projected_coefficients(t, mean0, cov0)
        m, var = state
        return [slope*m+offset, 2*slope*var+2/model.beta]

    sol = solve_ivp(rhs, (0, float(times[-1])),
                    [float(mean0[0]), float(cov0[0,0])],
                    t_eval=times, rtol=rtol, atol=atol)
    if not sol.success:
        raise RuntimeError(sol.message)
    return sol.y[0], sol.y[1]


def equilibrium_closure_moments(model, times, mean0, cov0):
    """OU closure built only from the equilibrium free energy F(z)=a*z**2/2."""
    times = np.asarray(times, dtype=float)
    m = mean0[0]*np.exp(-model.a*times)
    v_inf = 1/(model.beta*model.a)
    v = v_inf + (cov0[0,0]-v_inf)*np.exp(-2*model.a*times)
    return m, v
