"""Provisional Chapter 2 tools; PyTorch is an optional experiment dependency.

Every solver here uses the SDE dX = b_f dt + sqrt(2 epsilon) dW,
b_f = -grad V, and the BACKWARD equation epsilon Delta q + b_f.grad q = 0.
The printed assessment equation -epsilon Delta q + b_f.grad q = 0 instead
describes SDE drift -b_f. It is deliberately not an alternative flag here.

Fourier fields and pointwise residuals support general d. Reference solves and
FNO training are two-dimensional only; no ten-dimensional grid solver is claimed.
"""

from dataclasses import dataclass
import math
from typing import Callable, Protocol

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve
import torch
from torch import nn
from torch.nn import functional as F


class Field(Protocol):
    """Interface for future sparse/low-rank, non-grid field representations."""

    def __call__(self, x: torch.Tensor) -> torch.Tensor: ...


@dataclass(frozen=True)
class FourierField:
    """Real field on [-L/2,L/2)^d with phase 2*pi*k.x/L.

    Use one representative per +/- pair, with first nonzero entry positive.
    Zero mode is allowed, but its sine coefficient must be zero. This makes
    Parseval normalization exact, independent of evaluation grid or dimension.
    """

    modes: torch.Tensor
    cosine: torch.Tensor
    sine: torch.Tensor
    length: float = 20.0

    def __post_init__(self):
        modes = torch.as_tensor(self.modes)
        a = torch.as_tensor(self.cosine)
        b = torch.as_tensor(self.sine)
        if modes.ndim != 2 or min(modes.shape) < 1:
            raise ValueError("modes must have shape (number of modes, dimension)")
        if not torch.isfinite(modes).all() or not torch.equal(modes, modes.round()):
            raise ValueError("Fourier modes must be finite integers")
        if a.shape != modes.shape[:1] or b.shape != a.shape:
            raise ValueError("coefficient shape must match modes")
        if not torch.isfinite(a).all() or not torch.isfinite(b).all():
            raise ValueError("coefficients must be finite")
        keys = [tuple(row) for row in modes.tolist()]
        if len(set(keys)) != len(keys):
            raise ValueError("duplicate modes")
        for key, sine in zip(keys, b):
            nonzero = [v for v in key if v != 0]
            if nonzero and nonzero[0] < 0:
                raise ValueError("use canonical +/- representatives")
            if not nonzero and sine != 0:
                raise ValueError("zero-mode sine coefficient must be zero")
        if not math.isfinite(self.length) or self.length <= 0:
            raise ValueError("length must be finite and positive")
        object.__setattr__(self, "modes", modes.to(torch.int64))
        object.__setattr__(self, "cosine", a)
        object.__setattr__(self, "sine", b)

    @property
    def dimension(self):
        return self.modes.shape[1]

    @property
    def volume(self):
        return self.length**self.dimension

    @property
    def l2_norm(self):
        zero = (self.modes == 0).all(dim=1).to(self.cosine.device)
        square = (self.cosine[zero] ** 2).sum()
        square = square + 0.5 * (self.cosine[~zero] ** 2 + self.sine[~zero] ** 2).sum()
        return math.sqrt(self.volume * float(square))

    def __call__(self, x):
        if x.shape[-1] != self.dimension:
            raise ValueError("point dimension differs from Fourier field")
        modes = self.modes.to(device=x.device, dtype=x.dtype)
        phase = (2 * math.pi / self.length) * (x @ modes.T)
        return (phase.cos() * self.cosine.to(x) + phase.sin() * self.sine.to(x)).sum(-1)


def sample_fourier_field(dimension, modes, *, seed=0, length=20.0, l2_per_volume=0.1):
    """Sample a coefficient direction and set ||f||_L2 / volume to the bound.

    This is a reproducible distribution on the boundary of the stated L2 ball,
    not uniform sampling of all functions in that ball. It is NOT RMS scaling.
    Pass a smaller l2_per_volume to sample a smaller radius.
    """
    if dimension < 1 or not math.isfinite(l2_per_volume) or l2_per_volume < 0:
        raise ValueError("invalid dimension or norm bound")
    generator = torch.Generator().manual_seed(seed)
    k = torch.as_tensor(modes)
    if k.ndim != 2 or k.shape[1] != dimension:
        raise ValueError("modes must have the requested dimension")
    a, b = torch.randn(2, len(k), generator=generator, dtype=torch.float64)
    b[(k == 0).all(1)] = 0
    field = FourierField(k, a, b, length)
    scale = l2_per_volume * field.volume / field.l2_norm
    return FourierField(k, a * scale, b * scale, length)


def potential(x, f: Field, *, periodize=False, length=20.0):
    """Assessment V, with optional explicitly periodized Gaussian bumps.

    Default: EXACT Euclidean formula (not periodic). Periodic mode replaces each
    Gaussian by its infinite lattice sum, evaluated by a Fourier truncation
    with exp(-omega_max^2/2) <= 1e-15. The two models must not be conflated.
    """
    bumps = []
    for center, weight in [(-1.0, 2.0), (1.0, 2.0), (0.0, 1.0)]:
        delta = x - center
        if periodize:
            if not math.isfinite(length) or length <= 0:
                raise ValueError("length must be finite and positive")
            count = math.ceil(length * math.sqrt(2 * math.log(1e15)) / (2 * math.pi))
            omega = (
                2 * math.pi / length * torch.arange(1, count + 1, device=x.device, dtype=x.dtype)
            )
            factors = (
                math.sqrt(2 * math.pi)
                / length
                * (
                    1
                    + 2 * (torch.cos(delta[..., None] * omega) * torch.exp(-(omega**2) / 2)).sum(-1)
                )
            )
            bump = factors.prod(-1)
        else:
            bump = torch.exp(-0.5 * delta.square().sum(-1))
        bumps.append(weight * bump)
    return sum(bumps) + f(x)


def _gradient(values, x):
    if not values.requires_grad:
        return x * 0
    derivative = torch.autograd.grad(
        values.sum(), x, create_graph=True, retain_graph=True, allow_unused=True
    )[0]
    return x * 0 if derivative is None else derivative + x * 0


def drift(x, f: Field, *, periodize=False, length=20.0):
    """SDE drift -grad V, retaining the graph for derivative-based losses."""
    with torch.enable_grad():
        points = x if x.requires_grad else x.detach().clone().requires_grad_(True)
        return -_gradient(potential(points, f, periodize=periodize, length=length), points)


def committor_residual(q: Callable, x, b: Callable, epsilon):
    """Pointwise AD residual +epsilon*Delta q + b.grad q, shape (points,).

    q must act independently on each row of x (no batch coupling). x contains
    interior collocation points only, not points inside A or B. A grid FNO
    instead uses grid_residual; differentiating its batch sum is not this AD.
    """
    if not math.isfinite(epsilon) or epsilon <= 0:
        raise ValueError("epsilon must be finite and positive")
    if x.ndim != 2 or min(x.shape) < 1:
        raise ValueError("x must have shape (points, dimension)")
    points = x if x.requires_grad else x.detach().clone().requires_grad_(True)
    values = q(points).reshape(-1)
    if values.shape != points.shape[:1]:
        raise ValueError("q must return one scalar per point")
    gradient = _gradient(values, points)
    laplacian = sum(_gradient(gradient[:, j], points)[:, j] for j in range(points.shape[-1]))
    velocity = b(points)
    if velocity.shape != points.shape:
        raise ValueError("drift must return one vector per point")
    return epsilon * laplacian + (velocity * gradient).sum(-1)


def boundary_loss(q_a, q_b):
    """Equal weighting of the A=0 and B=1 Dirichlet errors."""
    if q_a.numel() == 0 or q_b.numel() == 0:
        raise ValueError("both boundary sets must be sampled")
    return q_a.square().mean() + (q_b - 1).square().mean()


def range_loss(q):
    return (F.relu(-q).square() + F.relu(q - 1).square()).mean()


def periodic_grid(n, length=20.0):
    """Endpoint-excluded grid, x index first: (n,n,2)."""
    if not isinstance(n, int) or n < 4 or not math.isfinite(length) or length <= 0:
        raise ValueError("n must be an integer >= 4 and length positive")
    axis = np.arange(n) * length / n - length / 2
    return np.stack(np.meshgrid(axis, axis, indexing="ij"), axis=-1)


def ball_masks(points, *, centers_b, radius=0.5, center_a=None, length=20.0):
    """Closed, torus-distance ball masks; B centers are REQUIRED, repeats allowed."""
    points = np.asarray(points, dtype=float)
    dimension = points.shape[-1]
    a = -np.ones(dimension) if center_a is None else np.asarray(center_a, dtype=float)
    centers = np.asarray(centers_b, dtype=float)
    if centers.ndim != 2 or len(centers) == 0 or centers.shape[1] != dimension:
        raise ValueError("centers_b must have shape (number of balls, dimension)")
    if (
        a.shape != (dimension,)
        or not np.isfinite(centers).all()
        or not np.isfinite(a).all()
        or not 0 < radius < length / 2
    ):
        raise ValueError("invalid ball geometry")

    def distance_squared(delta):
        wrapped = (delta + length / 2) % length - length / 2
        return (wrapped**2).sum(-1)

    if np.any(distance_squared(centers - a) <= (2 * radius) ** 2):
        raise ValueError("A and B must have disjoint closures")
    mask_a = distance_squared(points - a) <= radius**2
    mask_b = np.any(distance_squared(points[..., None, :] - centers) <= radius**2, axis=-1)
    return mask_a, mask_b


def backward_matrix(b, epsilon, h):
    """Periodic backward CTMC generator on an n by n grid.

    Outgoing rates r_(i,i+/-e_j) = epsilon/h^2 + max(+/-b_j,0)/h.
    Positive rates give a discrete maximum principle with no Peclet condition.
    Interior consistency is first order for nonzero drift, second for b=0.
    """
    b = np.asarray(b, dtype=float)
    if (
        b.ndim != 3
        or b.shape[0] != b.shape[1]
        or b.shape[-1] != 2
        or b.shape[0] < 4
        or not np.isfinite(b).all()
    ):
        raise ValueError("b must be finite with shape (n,n,2), n >= 4")
    if not math.isfinite(epsilon) or epsilon <= 0 or not math.isfinite(h) or h <= 0:
        raise ValueError("epsilon and h must be finite and positive")
    n = b.shape[0]
    ids = np.arange(n * n).reshape(n, n)
    rows, cols, data = [], [], []
    outgoing = np.zeros((n, n))
    for j in range(2):
        for sign in (-1, 1):
            rates = epsilon / h**2 + np.maximum(sign * b[..., j], 0) / h
            rows.extend(ids.ravel())
            cols.extend(np.roll(ids, -sign, axis=j).ravel())
            data.extend(rates.ravel())
            outgoing += rates
    rows.extend(ids.ravel())
    cols.extend(ids.ravel())
    data.extend(-outgoing.ravel())
    return sparse.csr_matrix((data, (rows, cols)), shape=(n * n, n * n))


@dataclass
class ReferenceSolution:
    points: np.ndarray
    q: np.ndarray
    mask_a: np.ndarray
    mask_b: np.ndarray
    generator: sparse.csr_matrix
    h: float

    @property
    def interior(self):
        return ~(self.mask_a | self.mask_b)

    @property
    def residual_max(self):
        return float(np.max(np.abs((self.generator @ self.q.ravel())[self.interior.ravel()])))


def solve_reference(f: FourierField, *, centers_b, n=64, epsilon=0.5, radius=0.5, center_a=None):
    """2D sparse committor solve for the PERIODIZED potential.

    Balls are voxelized on this mesh; their geometric error is separate from
    the algebraic residual. Reject unresolved balls instead of inventing labels.
    """
    if f.dimension != 2:
        raise ValueError("reference solver supports dimension 2 only")
    points = periodic_grid(n, f.length)
    a, b = ball_masks(
        points, centers_b=centers_b, radius=radius, center_a=center_a, length=f.length
    )
    if not a.any() or not b.any() or (a | b).all():
        raise ValueError("grid must resolve both balls and an interior")
    x = torch.tensor(points, dtype=torch.float64)
    velocity = drift(x, f, periodize=True, length=f.length).detach().numpy()
    return solve_grid_committor(points, velocity, a, b, epsilon=epsilon, length=f.length)


def solve_grid_committor(points, velocity, mask_a, mask_b, *, epsilon, length):
    """Lower-level interface for independent manufactured/reference checks."""
    points, velocity = np.asarray(points), np.asarray(velocity)
    if (
        points.ndim != 3
        or points.shape[0] != points.shape[1]
        or points.shape[-1] != 2
        or velocity.shape != points.shape
    ):
        raise ValueError("points and velocity must both have shape (n,n,2)")
    n = points.shape[0]
    a, b = np.asarray(mask_a, bool), np.asarray(mask_b, bool)
    if (
        a.shape != (n, n)
        or b.shape != a.shape
        or (a & b).any()
        or not a.any()
        or not b.any()
        or (a | b).all()
    ):
        raise ValueError("invalid Dirichlet masks")
    generator = backward_matrix(velocity, epsilon, length / n)
    interior = np.flatnonzero(~(a | b).ravel())
    target = np.flatnonzero(b.ravel())
    matrix = -generator[interior][:, interior]
    rhs = np.asarray(generator[interior][:, target].sum(axis=1)).ravel()
    q = np.zeros(n * n)
    q[target] = 1
    q[interior] = spsolve(matrix, rhs)
    if not np.isfinite(q).all() or q.min() < -1e-9 or q.max() > 1 + 1e-9:
        raise ArithmeticError("sparse solve violated discrete maximum principle")
    # Do not clip: preserve the actual sparse-solver residual and roundoff.
    return ReferenceSolution(points, q.reshape(n, n), a, b, generator, length / n)


def grid_residual(q, b, epsilon, h):
    """Same periodic upwind backward operator as the sparse reference.

    q: (batch,n,n), b: (batch,n,n,2). Mask out ALL absorbing nodes in the loss.
    This is a discrete residual, not a continuum AD certificate.
    """
    if q.ndim != 3 or b.shape != (*q.shape, 2):
        raise ValueError("expected q (batch,n,n) and b (batch,n,n,2)")
    if not math.isfinite(epsilon) or epsilon <= 0 or not math.isfinite(h) or h <= 0:
        raise ValueError("epsilon and h must be finite and positive")
    residual = torch.zeros_like(q)
    for j in range(2):
        for sign in (-1, 1):
            rates = epsilon / h**2 + F.relu(sign * b[..., j]) / h
            residual = residual + rates * (torch.roll(q, -sign, dims=j + 1) - q)
    return residual


class SpectralConv2d(nn.Module):
    """Truncated rFFT convolution with disjoint positive/negative first-axis bands."""

    def __init__(self, in_channels, out_channels, modes):
        super().__init__()
        if modes < 1:
            raise ValueError("modes must be positive")
        self.modes = modes
        self.out_channels = out_channels
        shape = (in_channels, out_channels, modes, modes)
        scale = 1 / math.sqrt(in_channels * out_channels)
        self.positive = nn.Parameter(scale * torch.randn(*shape, dtype=torch.cfloat))
        self.negative = nn.Parameter(scale * torch.randn(*shape, dtype=torch.cfloat))

    def forward(self, x):
        batch, _, nx, ny = x.shape
        m = self.modes
        if 2 * m > nx or m > ny // 2 + 1:
            raise ValueError("truncated Fourier bands do not fit this grid")
        transformed = torch.fft.rfft2(x)
        out = transformed.new_zeros(batch, self.out_channels, nx, ny // 2 + 1)
        out[:, :, :m, :m] = torch.einsum(
            "bixy,ioxy->boxy", transformed[:, :, :m, :m], self.positive
        )
        out[:, :, -m:, :m] = torch.einsum(
            "bixy,ioxy->boxy", transformed[:, :, -m:, :m], self.negative
        )
        return torch.fft.irfft2(out, s=(nx, ny))


class FNO2d(nn.Module):
    """f grid -> sigmoid committor grid, with fixed periodic position channels.

    Position is necessary: a translation-equivariant network fed constant f
    cannot locate the fixed absorbing sets. No d>=10 claim is made here.
    """

    def __init__(self, width=16, modes=4, depth=3):
        super().__init__()
        if width < 1 or depth < 1:
            raise ValueError("width and depth must be positive")
        self.lift = nn.Conv2d(5, width, 1)
        self.spectral = nn.ModuleList([SpectralConv2d(width, width, modes) for _ in range(depth)])
        self.local = nn.ModuleList([nn.Conv2d(width, width, 1) for _ in range(depth)])
        self.project = nn.Sequential(nn.Conv2d(width, width, 1), nn.GELU(), nn.Conv2d(width, 1, 1))

    def forward(self, f):
        if f.ndim != 4 or f.shape[1] != 1:
            raise ValueError("FNO input must have shape (batch,1,nx,ny)")
        nx, ny = f.shape[-2:]
        xx = 2 * math.pi * torch.arange(nx, device=f.device, dtype=f.dtype) / nx
        yy = 2 * math.pi * torch.arange(ny, device=f.device, dtype=f.dtype) / ny
        x, y = torch.meshgrid(xx, yy, indexing="ij")
        coordinates = torch.stack([x.sin(), x.cos(), y.sin(), y.cos()])
        v = self.lift(torch.cat([f, coordinates[None].expand(len(f), -1, -1, -1)], dim=1))
        for spectral, local in zip(self.spectral, self.local):
            v = F.gelu(spectral(v) + local(v))
        return torch.sigmoid(self.project(v))


def enforce_boundary(q, mask_a, mask_b):
    """Hard grid values on absorbing sets; do not differentiate across their edge."""
    return torch.where(mask_a, torch.zeros_like(q), torch.where(mask_b, torch.ones_like(q), q))


def fno_loss(
    model, inputs, targets, velocities, mask_a, mask_b, *, epsilon, h, weights=(1.0, 0.01, 1.0, 1.0)
):
    """Supervised + discrete PDE + soft BC + range losses, all reported separately.

    The PDE uses the hard Dirichlet grid extension, with residuals evaluated
    only outside A and B. BC loss is on the raw sigmoid output. Reference data,
    masks and velocities must describe one fixed geometry and epsilon.
    """
    if len(weights) != 4 or any(not math.isfinite(w) or w < 0 for w in weights):
        raise ValueError("four nonnegative finite weights required")
    raw = model(inputs)[:, 0]
    if targets.shape != (len(raw), 1, *raw.shape[1:]):
        raise ValueError("targets must match the FNO output shape")
    a = torch.as_tensor(mask_a, device=raw.device, dtype=torch.bool).expand_as(raw)
    b = torch.as_tensor(mask_b, device=raw.device, dtype=torch.bool).expand_as(raw)
    interior = ~(a | b)
    if (a & b).any() or not a.any() or not b.any() or not interior.any():
        raise ValueError("invalid training masks")
    prediction = enforce_boundary(raw, a, b)
    terms = {
        "supervised": (prediction - targets[:, 0]).square().mean(),
        "pde": grid_residual(prediction, velocities, epsilon, h)[interior].square().mean(),
        "boundary": boundary_loss(raw[a], raw[b]),
        "range": range_loss(raw),
    }
    total = sum(weight * term for weight, term in zip(weights, terms.values()))
    return total, terms


def train_fno(
    model,
    inputs,
    targets,
    velocities,
    mask_a,
    mask_b,
    *,
    epsilon,
    h,
    steps=10,
    learning_rate=1e-3,
    weights=(1.0, 0.01, 1.0, 1.0),
):
    """Small deterministic full-batch training building block; seed before model creation."""
    if steps < 1 or learning_rate <= 0:
        raise ValueError("positive steps and learning_rate required")
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    history = []
    model.train()
    for _ in range(steps):
        optimizer.zero_grad()
        loss, terms = fno_loss(
            model,
            inputs,
            targets,
            velocities,
            mask_a,
            mask_b,
            epsilon=epsilon,
            h=h,
            weights=weights,
        )
        if not torch.isfinite(loss):
            raise ArithmeticError("nonfinite FNO loss")
        loss.backward()
        optimizer.step()
        history.append(
            {
                "total": float(loss.detach()),
                **{name: float(term.detach()) for name, term in terms.items()},
            }
        )
    return history


def pinn_failure_values(x, t, k, *, epsilon=1.0, amplitude=0.5):
    """C2 cutoff counterexample on the 2*pi torus, returning (u_k,p,residual).

    eta_k=1 for t<=1/k, 0 for t>=2/k; in between it is the quintic
    1-10s^3+15s^4-6s^5 with s=k*t-1. Residual is eta'_k*(p-p_infinity).
    This analytic construction demonstrates loss failure, not trained-network failure.
    """
    if k <= 0 or epsilon <= 0 or not 0 < amplitude < 1:
        raise ValueError("k, epsilon positive and 0 < amplitude < 1 required")
    s = torch.clamp(k * t - 1, 0, 1)
    # Stable factorization near s=1 avoids negative roundoff in eta.
    eta = (1 - s) ** 3 * (1 + 3 * s + 6 * s**2)
    derivative = -30 * k * s**2 * (1 - s) ** 2
    deviation = amplitude * torch.exp(-epsilon * t) * torch.cos(x) / (2 * math.pi)
    equilibrium = 1 / (2 * math.pi)
    return equilibrium + eta * deviation, equilibrium + deviation, derivative * deviation
