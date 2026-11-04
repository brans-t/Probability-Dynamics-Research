"""Affine conditional regression and its conversion to projected OU drift."""

import numpy as np

from .gaussian import CoupledOU


def fit_conditional_y_given_x(x, y) -> tuple[float, float]:
    """Fit E[Y | X=z] as intercept+slope*z using least squares.

    The population conditional mean is affine for nondegenerate joint Gaussian
    data; finite samples still introduce estimation error.
    """
    x, y = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
    if x.shape != y.shape or x.ndim != 1 or len(x) < 2:
        raise ValueError("x and y must be 1D arrays of equal length >= 2")
    design = np.column_stack([np.ones_like(x), x])
    intercept, slope = np.linalg.lstsq(design, y, rcond=None)[0]
    return float(intercept), float(slope)


def inferred_drift(model: CoupledOU, intercept, conditional_slope) -> tuple[float, float]:
    """Convert fitted E[Y | X=z] coefficients to drift (slope, offset)."""
    drift_slope = -model.a + model.c * model.kappa * (conditional_slope - model.kappa)
    drift_offset = model.c * model.kappa * intercept
    return drift_slope, drift_offset
