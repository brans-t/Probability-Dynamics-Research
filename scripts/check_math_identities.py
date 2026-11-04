"""Exact, independent algebra checks for selected manuscript identities.

Requires SymPy (optional dependency: pip install -e '.[audit]').
These checks supplement the proof review; they are not a proof checker.
"""

import json
import sympy as sp


checks = []


def zero(name, expression):
    entries = list(expression) if isinstance(expression, sp.MatrixBase) else [expression]
    assert all(sp.simplify(x) == 0 for x in entries), name
    checks.append(name)


def main():
    x, y, z = sp.symbols("x y z", real=True)
    h, omega, a, c, beta, ell, mass, grav = sp.symbols(
        "h omega a c beta ell mass grav", positive=True
    )
    kappa = sp.symbols("kappa", real=True)
    J = sp.Matrix([[0, 1], [-1, 0]])
    s11, s12, s22 = sp.symbols("s11 s12 s22", real=True)
    S = sp.Matrix([[s11, s12], [s12, s22]])
    zero("Hamiltonian variational symplectic identity", (J * S).T * J + J * (J * S))
    verlet = sp.Matrix(
        [
            [1 - omega**2 * h**2 / 2, h],
            [-h * omega**2 * (1 - omega**2 * h**2 / 4), 1 - omega**2 * h**2 / 2],
        ]
    )
    metric = sp.diag(omega**2 * (1 - omega**2 * h**2 / 4), 1)
    zero("Verlet determinant", verlet.det() - 1)
    zero("Verlet symplecticity", verlet.T * J * verlet - J)
    zero("Verlet exact modified energy", verlet.T * metric * verlet - metric)
    euler = sp.eye(2) + h * sp.Matrix([[0, 1], [-(omega**2), 0]])
    zero("Euler determinant expansion", euler.det() - (1 + h**2 * omega**2))
    physical_metric = sp.diag(omega**2, 1)
    zero(
        "Euler exact oscillator energy amplification",
        euler.T * physical_metric * euler - (1 + h**2 * omega**2) * physical_metric,
    )

    K = sp.Matrix([[a + c * kappa**2, -c * kappa], [-c * kappa, c]])
    covariance = sp.Matrix([[1 / a, kappa / a], [kappa / a, 1 / c + kappa**2 / a]]) / beta
    zero("OU inverse covariance", K * covariance - sp.eye(2) / beta)
    zero("OU Lyapunov equation", K * covariance + covariance * K - 2 * sp.eye(2) / beta)
    zero(
        "OU conditional variance",
        covariance[1, 1] - covariance[1, 0] ** 2 / covariance[0, 0] - 1 / (beta * c),
    )
    zero("OU equilibrium conditional mean", covariance[1, 0] / covariance[0, 0] - kappa)
    zero(
        "OU covariance second-derivative gap",
        (K * K * covariance)[0, 0] - a / beta - c * kappa**2 / beta,
    )
    zero(
        "Nonlinear reaction-coordinate divergence",
        sp.diff(2 * y / (1 + 4 * y**2), y) - 2 * (1 - 4 * y**2) / (1 + 4 * y**2) ** 2,
    )

    v = sp.Matrix([x * y + x**2, -(y**3) + x])
    log_density = x**2 * y + sp.sin(x) + y**2
    variables = (x, y)
    score = sp.Matrix([sp.diff(log_density, q) for q in variables])
    Hess = sp.hessian(log_density, variables)
    A = v.jacobian(variables)
    divergence = sp.trace(A)
    time_log = -divergence - (v.dot(score))
    dt_score = sp.Matrix([sp.diff(time_log, q) for q in variables]) + Hess * v
    zero(
        "Score material-derivative commutator",
        dt_score + A.T * score + sp.Matrix([sp.diff(divergence, q) for q in variables]),
    )
    dt_hessian = sp.hessian(time_log, variables)
    for i, q in enumerate(variables):
        dt_hessian += v[i] * Hess.diff(q)
    target = -A.T * Hess - Hess * A - sp.hessian(divergence, variables)
    for i in range(2):
        target -= score[i] * sp.hessian(v[i], variables)
    zero("Log-density Hessian transport tensor", dt_hessian - target)

    p, q = sp.symbols("p q", positive=True)
    risk = p * sp.log(1 + sp.exp(-z)) + q * sp.log(1 + sp.exp(z))
    zero("Logistic optimum first derivative", sp.diff(risk, z).subs(z, sp.log(p / q)))
    zero(
        "Logistic strict convexity formula",
        sp.diff(risk, z, 2) - (p + q) * sp.exp(z) / (1 + sp.exp(z)) ** 2,
    )
    js_integrand = (p * sp.log(2 * p / (p + q)) + q * sp.log(2 * q / (p + q))) / 2
    zero(
        "Logistic/Jensen-Shannon pointwise identity",
        sp.expand_log(
            risk.subs(z, sp.log(p / q)) + 2 * js_integrand - (p + q) * sp.log(2), force=True
        ),
    )
    t = sp.symbols("t", positive=True)
    conjugate = (z * t - t * sp.log(t)).subs(t, sp.exp(z - 1))
    zero("Entropy Fenchel conjugate", conjugate - sp.exp(z - 1))
    saddle = (p - q * t) * z + q * (t * sp.log(t) - t)
    zero("Finite-state saddle derivative in discriminator", sp.diff(saddle, z).subs(t, p / q))
    zero(
        "Finite-state saddle derivative in weight",
        sp.diff(saddle, t).subs({t: p / q, z: sp.log(p / q)}),
    )
    r1, r2, r3, c1, c2 = sp.symbols("r1 r2 r3 c1 c2", positive=True)
    dm = sp.Matrix([c1 * (r2 - r1), c1 * (r1 - r2) + c2 * (r3 - r2), c2 * (r2 - r3)])
    entropy = sum(sp.log(r) * d for r, d in zip([r1, r2, r3], dm))
    zero(
        "Detailed-balance entropy dissipation",
        entropy
        + c1 * (r2 - r1) * (sp.log(r2) - sp.log(r1))
        + c2 * (r3 - r2) * (sp.log(r3) - sp.log(r2)),
    )

    canonical = sp.diag(ell, 1 / ell)
    zero("Pendulum canonical coordinate map", canonical.T * J * canonical - J)
    energy = mass * grav * ell * (1 - sp.cos(x / ell))
    zero(
        "Pendulum quartic energy coefficient",
        sp.diff(energy, x, 4).subs(x, 0) / sp.factorial(4) + mass * grav / (24 * ell**3),
    )
    zero(
        "Pendulum cubic vector-field coefficient",
        sp.diff(z - sp.sin(z), z, 3).subs(z, 0) / 6 - sp.Rational(1, 6),
    )
    A1 = sp.Matrix([[0, 1], [0, 0]])
    A2 = sp.Matrix([[0, 0], [1, 0]])
    zero(
        "Ordered noncommuting fundamental solution",
        (sp.eye(2) + A2) * (sp.eye(2) + A1) - sp.Matrix([[1, 1], [1, 2]]),
    )
    assert (sp.exp(A1 + A2) - (sp.eye(2) + A2) * (sp.eye(2) + A1)) != sp.zeros(2)
    checks.append("Unordered exponential differs in exact two-step counterexample")
    print(json.dumps({"sympy": sp.__version__, "passed": len(checks), "checks": checks}, indent=2))


if __name__ == "__main__":
    main()
