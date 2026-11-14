"""Mathematical checks for the provisional neural PDE module (requires torch)."""

import math

import numpy as np
import pytest

torch = pytest.importorskip("torch")

from probflow.neural_pde_solver import (  # noqa: E402 (optional dependency check first)
    FNO2d,
    SpectralConv2d,
    backward_matrix,
    ball_masks,
    boundary_loss,
    committor_residual,
    drift,
    enforce_boundary,
    fno_loss,
    grid_residual,
    periodic_grid,
    pinn_failure_values,
    potential,
    range_loss,
    sample_fourier_field,
    solve_grid_committor,
    solve_reference,
    train_fno,
)


@pytest.mark.parametrize("dimension", [1, 2, 10])
def test_fourier_periodicity_exact_norm_and_seed(dimension):
    modes = np.vstack([np.zeros(dimension, int), np.eye(dimension, dtype=int)])
    f = sample_fourier_field(dimension, modes, seed=7, length=4, l2_per_volume=0.03)
    again = sample_fourier_field(dimension, modes, seed=7, length=4, l2_per_volume=0.03)
    torch.testing.assert_close(f.cosine, again.cosine)
    x = torch.randn(11, dimension, dtype=torch.float64)
    for j in range(dimension):
        shift = torch.eye(dimension, dtype=x.dtype)[j] * f.length
        torch.testing.assert_close(f(x), f(x + shift), atol=1e-11, rtol=1e-11)
    assert f.l2_norm / f.volume == pytest.approx(0.03)
    if dimension == 1:
        points = torch.linspace(-2, 2, 4097, dtype=torch.float64)[:-1, None]
        quadrature = torch.sqrt(f(points).square().mean() * 4).item()
        assert quadrature == pytest.approx(f.l2_norm, abs=1e-12)
        assert quadrature / math.sqrt(4) != pytest.approx(0.03)


@pytest.mark.parametrize("modes", [[[1], [1]], [[1], [-1]], [[0.5]]])
def test_sampler_rejects_nonorthogonal_or_fractional_modes(modes):
    with pytest.raises(ValueError):
        sample_fourier_field(1, modes)


@pytest.mark.parametrize("periodize", [False, True])
def test_potential_drift_finite_difference_and_periodic_seam(periodize):
    f = sample_fourier_field(2, [[1, 0], [0, 1], [1, -1]], seed=2, length=6)
    x = torch.tensor([[0.3, -0.7], [2.8, -2.9]], dtype=torch.float64)
    actual = drift(x, f, periodize=periodize, length=6).detach()
    delta = 1e-5
    differences = []
    for j in range(2):
        shift = torch.eye(2, dtype=x.dtype)[j] * delta
        differences.append(
            -(
                potential(x + shift, f, periodize=periodize, length=6)
                - potential(x - shift, f, periodize=periodize, length=6)
            )
            / (2 * delta)
        )
    torch.testing.assert_close(actual, torch.stack(differences, -1), atol=2e-9, rtol=1e-8)
    if periodize:
        torch.testing.assert_close(
            potential(x, f, periodize=True, length=6), potential(x + 6, f, periodize=True, length=6)
        )
        torch.testing.assert_close(actual, drift(x + 6, f, periodize=True, length=6).detach())
        # Independent lattice-sum evaluation, rather than a second copy of the Fourier code.
        image_sum = torch.zeros(len(x), dtype=x.dtype)
        for center, weight in [(-1, 2), (1, 2), (0, 1)]:
            for i in range(-3, 4):
                for j in range(-3, 4):
                    shift = torch.tensor([i, j], dtype=x.dtype) * 6
                    image_sum += weight * torch.exp(-0.5 * ((x - center + shift) ** 2).sum(-1))
        torch.testing.assert_close(
            potential(x, f, periodize=True, length=6), image_sum + f(x), atol=1e-12, rtol=1e-12
        )
    else:
        raw = sum(
            w * torch.exp(-0.5 * ((x - c) ** 2).sum(-1)) for c, w in [(-1, 2), (1, 2), (0, 1)]
        )
        torch.testing.assert_close(potential(x, f), raw + f(x))


def test_ad_residual_sign_laplacian_constant_linear_and_training_gradient():
    x = torch.tensor([[0.2, 0.7], [-0.3, 0.5]], dtype=torch.float64)

    def b(z):
        return torch.stack([-2 * z[:, 0], 3 * z[:, 1]], -1)

    def q(z):
        return z[:, 0] ** 2 + 2 * z[:, 1] ** 2

    residual = committor_residual(q, x, b, 0.4)
    expected = 2.4 - 4 * x[:, 0] ** 2 + 12 * x[:, 1] ** 2
    assert residual.shape == (2,)
    torch.testing.assert_close(residual, expected)
    torch.testing.assert_close(committor_residual(lambda z: z[:, 0], x, b, 0.4), b(x)[:, 0])
    torch.testing.assert_close(
        committor_residual(lambda z: torch.ones(len(z)), x, b, 0.4), torch.zeros(2, dtype=x.dtype)
    )
    scale = torch.nn.Parameter(torch.tensor(0.7, dtype=x.dtype))
    committor_residual(lambda z: scale * q(z), x, b, 0.4).square().sum().backward()
    assert scale.grad is not None and scale.grad.abs() > 0


def test_geometry_repeated_centers_and_invalid_inputs():
    points = periodic_grid(32, 6)
    a, repeated = ball_masks(points, centers_b=[[1, 1], [1, 1]], length=6)
    _, single = ball_masks(points, centers_b=[[1, 1]], length=6)
    np.testing.assert_array_equal(repeated, single)
    assert a.any() and single.any() and not (a & single).any()
    with pytest.raises(ValueError, match="disjoint"):
        ball_masks(points, centers_b=[[-1, -1]], length=6)
    with pytest.raises(ValueError, match="centers_b"):
        ball_masks(points, centers_b=[], length=6)
    f = sample_fourier_field(2, [[1, 0]], length=20)
    with pytest.raises(ValueError, match="resolve"):
        solve_reference(f, centers_b=[[1, 1], [1, 1]], n=4, radius=0.01)


def test_reference_bc_range_positive_rates_and_torch_sparse_residual_agree():
    f = sample_fourier_field(2, [[1, 0], [0, 1], [1, 1]], seed=19, length=6)
    result = solve_reference(f, centers_b=[[1, 1], [1, 1]], n=32, epsilon=0.5)
    assert np.all(result.q[result.mask_a] == 0)
    assert np.all(result.q[result.mask_b] == 1)
    assert result.q.min() >= -1e-12 and result.q.max() <= 1 + 1e-12
    assert result.residual_max < 1e-11
    np.testing.assert_allclose(np.asarray(result.generator.sum(1)), 0, atol=1e-13)
    off_diagonal = result.generator - np.diag(result.generator.diagonal())
    assert off_diagonal.min() >= 0
    x = torch.tensor(result.points, dtype=torch.float64)
    velocity = drift(x, f, periodize=True, length=6).detach()
    r = grid_residual(torch.tensor(result.q)[None], velocity[None], 0.5, result.h)[0]
    np.testing.assert_allclose(r.numpy().ravel(), result.generator @ result.q.ravel(), atol=2e-13)
    # Periodic wrap: the x=0 row has a positive edge to x=n-1.
    assert result.generator[0, 31 * 32] > 0


def test_reference_independent_manufactured_solution_mesh_convergence():
    # Zero drift, absorbing vertical strips x=0 and x=L/2. On the two
    # remaining torus intervals the exact committor is a piecewise linear tent.
    errors = []
    for n in [16, 32, 64]:
        points = periodic_grid(n, 2 * math.pi)
        a, b = np.zeros((n, n), bool), np.zeros((n, n), bool)
        a[0, :], b[n // 2, :] = True, True
        out = solve_grid_committor(
            points, np.zeros_like(points), a, b, epsilon=0.7, length=2 * math.pi
        )
        indices = np.arange(n) / n
        expected = 1 - 2 * np.abs(indices - 0.5)
        errors.append(np.max(np.abs(out.q - expected[:, None])))
    assert max(errors) < 1e-12
    # Smooth periodic manufactured function: check consistency with nonzero
    # drift AND diffusion rather than only algebraic residuals of a solved grid.
    smooth_errors = []
    for n in [32, 64, 128]:
        points = periodic_grid(n, 2 * math.pi)
        xx, yy = points[..., 0], points[..., 1]
        velocity = np.stack([np.cos(yy), np.sin(xx)], -1)
        q = np.sin(xx) + np.cos(yy)
        exact = -0.7 * q + np.cos(yy) * np.cos(xx) - np.sin(xx) * np.sin(yy)
        approximate = (backward_matrix(velocity, 0.7, 2 * math.pi / n) @ q.ravel()).reshape(n, n)
        smooth_errors.append(np.max(np.abs(approximate - exact)))
    assert smooth_errors[2] < 0.55 * smooth_errors[1] < 0.55**2 * smooth_errors[0]


def test_boundary_and_range_constraints():
    assert boundary_loss(torch.zeros(3), torch.ones(2)) == 0
    assert range_loss(torch.tensor([-1.0, 0.2, 2.0])) == pytest.approx(2 / 3)
    with pytest.raises(ValueError):
        boundary_loss(torch.empty(0), torch.ones(2))


def test_spectral_convolution_known_constant_mode_and_invalid_overlap():
    layer = SpectralConv2d(1, 1, 2)
    with torch.no_grad():
        layer.positive.zero_()
        layer.negative.zero_()
        layer.positive[0, 0, 0, 0] = 2
    torch.testing.assert_close(layer(torch.ones(1, 1, 8, 8)), torch.full((1, 1, 8, 8), 2.0))
    with pytest.raises(ValueError, match="bands"):
        layer(torch.ones(1, 1, 3, 3))


def test_fno_shapes_joint_training_and_parameter_updates():
    torch.manual_seed(17)
    torch.set_num_threads(1)
    f = sample_fourier_field(2, [[1, 0], [0, 1]], seed=17, length=6)
    ref = solve_reference(f, centers_b=[[1, 1], [1, 1]], n=16)
    points = torch.tensor(ref.points, dtype=torch.float32)
    inputs = f(points)[None, None]
    targets = torch.tensor(ref.q, dtype=torch.float32)[None, None]
    velocity = drift(points, f, periodize=True, length=6).detach()[None]
    model = FNO2d(width=4, modes=3, depth=2)
    before = model.lift.weight.detach().clone()
    prediction = model(inputs)
    assert prediction.shape == inputs.shape
    assert prediction.min() >= 0 and prediction.max() <= 1
    assert model(torch.zeros(2, 1, 24, 24)).shape == (2, 1, 24, 24)
    initial, _ = fno_loss(
        model, inputs, targets, velocity, ref.mask_a, ref.mask_b, epsilon=0.5, h=ref.h
    )
    history = train_fno(
        model,
        inputs,
        targets,
        velocity,
        ref.mask_a,
        ref.mask_b,
        epsilon=0.5,
        h=ref.h,
        steps=8,
        learning_rate=0.01,
    )
    final, terms = fno_loss(
        model, inputs, targets, velocity, ref.mask_a, ref.mask_b, epsilon=0.5, h=ref.h
    )
    assert final < initial
    assert not torch.equal(before, model.lift.weight.detach())
    assert all(np.isfinite(row["total"]) for row in history)
    assert terms["range"] == 0
    bounded = enforce_boundary(prediction[:, 0], torch.tensor(ref.mask_a), torch.tensor(ref.mask_b))
    assert (bounded[:, ref.mask_a] == 0).all() and (bounded[:, ref.mask_b] == 1).all()


def test_pinn_failure_matches_ad_mass_ic_and_continuum_residual():
    x = torch.linspace(0, 2 * math.pi, 257, dtype=torch.float64)[:-1]
    times = torch.linspace(0, 1, 11, dtype=x.dtype)
    u, exact, empirical = pinn_failure_values(x[:, None], times[None], 64)
    torch.testing.assert_close((2 * math.pi) * u.mean(0), torch.ones(len(times), dtype=x.dtype))
    assert u.min() > 0
    torch.testing.assert_close(u[:, 0], exact[:, 0])
    assert empirical.abs().max() == 0
    assert (u[:, 1:] - exact[:, 1:]).abs().max() > 0.05
    # AD independently checks the analytic residual inside the missing layer.
    xx = torch.tensor([0.1, 0.8], dtype=x.dtype, requires_grad=True)
    tt = torch.tensor([1.3 / 64, 1.7 / 64], dtype=x.dtype, requires_grad=True)
    value, _, residual = pinn_failure_values(xx, tt, 64)
    dt = torch.autograd.grad(value.sum(), tt, create_graph=True)[0]
    dx = torch.autograd.grad(value.sum(), xx, create_graph=True)[0]
    dxx = torch.autograd.grad(dx.sum(), xx)[0]
    torch.testing.assert_close(dt - dxx, residual)
    assert residual.abs().max() > 1
    # The true continuum L2 residual increases rather than tending to zero.
    norms = []
    for k in [16, 32]:
        t = torch.linspace(1 / k, 2 / k, 1001, dtype=x.dtype)
        r = pinn_failure_values(x[:, None], t[None], k)[2]
        norms.append(float(torch.trapezoid((2 * math.pi) * r.square().mean(0), t)))
    assert norms[1] > 1.8 * norms[0]
