"""Classical conditional-regression baseline before introducing a neural estimator."""
import numpy as np


def fit_conditional_y_given_x(x, y):
    """Least squares E[Y|X=z] approximately intercept+slope*z.

    This is exact in the population for nondegenerate joint Gaussian data.
    """
    x, y = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
    if x.shape != y.shape or x.ndim != 1 or len(x) < 2:
        raise ValueError('x and y must be 1D arrays of equal length >= 2')
    design = np.column_stack([np.ones_like(x), x])
    intercept, slope = np.linalg.lstsq(design, y, rcond=None)[0]
    return float(intercept), float(slope)


def inferred_drift(model, intercept, conditional_slope):
    """Given E[Y|X=z] approx intercept+slope*z, return drift b(z)."""
    drift_slope = -model.a + model.c*model.kappa*(conditional_slope-model.kappa)
    drift_offset = model.c*model.kappa*intercept
    return drift_slope, drift_offset
