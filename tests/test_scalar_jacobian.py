"""Independent closed-form and precision checks for the scalar experiment."""

from decimal import Decimal, localcontext

from scalar_jacobian import convergence_rows, numerical_jacobians


def test_stage_integrations_match_closed_form_jacobians():
    with localcontext() as context:
        context.prec = 100
        for steps in (4, 8, 16, 32, 64, 128):
            h = Decimal(1) / steps
            euler, rk4 = numerical_jacobians(steps)
            r4 = 1 + h + h**2 / 2 + h**3 / 6 + h**4 / 24
            assert abs(euler - (1 + h)**steps) < Decimal("1e-95")
            assert abs(rk4 - r4**steps) < Decimal("1e-95")


def test_errors_are_precision_stable_and_have_predicted_orders():
    rows = convergence_rows(80)
    reference = convergence_rows(120)
    with localcontext() as context:
        context.prec = 120
        for actual, high_precision in zip(rows, reference):
            for method in ("Euler", "RK4"):
                error = actual[f"{method}_error"]
                exact = high_precision[f"{method}_error"]
                assert abs(error / exact - 1) < Decimal("1e-60")
        assert Decimal("0.98") < rows[-2]["Euler_order"] < 1
        assert Decimal("3.98") < rows[-2]["RK4_order"] < 4
        exact_e = Decimal(1).exp()
        h = rows[-1]["h"]
        assert abs(rows[-1]["Euler_error"] / (exact_e * h / 2) - 1) < Decimal("0.02")
        assert abs(rows[-1]["RK4_error"] / (exact_e * h**4 / 120) - 1) < Decimal("0.02")
