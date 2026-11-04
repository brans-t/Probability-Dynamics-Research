"""Regression checks for experiment isolation and numerical structure."""

import csv
import json
import os
from pathlib import Path
import subprocess
import sys

import numpy as np

from markov import generator
from matrix_flow import fundamental_matrix

ROOT = Path(__file__).resolve().parents[1]


def test_markov_generator_conserves_mass_and_satisfies_detailed_balance():
    matrix, invariant, _ = generator()
    np.testing.assert_allclose(matrix.sum(axis=0), 0, atol=1e-12)
    np.testing.assert_allclose(matrix @ invariant, 0, atol=1e-12)
    flux = matrix * invariant[np.newaxis, :]
    np.testing.assert_allclose(flux, flux.T, atol=1e-12)
    off_diagonal = matrix.copy()
    np.fill_diagonal(off_diagonal, 0)
    assert off_diagonal.min() >= 0


def test_determinant_convergence_matches_expected_orders():
    exact = np.exp(-0.15)
    for method, minimum_ratio in [("Euler", 1.8), ("RK4", 12.0)]:
        coarse = abs(np.linalg.det(fundamental_matrix(32, method)) - exact)
        fine = abs(np.linalg.det(fundamental_matrix(64, method)) - exact)
        assert coarse / fine > minimum_ratio


def test_importing_experiments_does_not_run_them(tmp_path):
    work = tmp_path / "work"
    work.mkdir()
    environment = dict(os.environ)
    environment["PYTHONPATH"] = os.pathsep.join([str(ROOT / "src"), str(ROOT / "experiments")])
    environment["MPLCONFIGDIR"] = str(tmp_path / "matplotlib")
    script = (
        "import sys; import run_benchmarks, hamiltonian_benchmark, project11_kl_benchmarks; "
        "assert 'torch' not in sys.modules"
    )
    result = subprocess.run(
        [sys.executable, "-c", script],
        cwd=work,
        env=environment,
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout == ""
    assert not list(work.iterdir())


def test_combined_runner_matches_saved_deterministic_results(tmp_path):
    environment = dict(os.environ)
    environment["PYTHONPATH"] = str(ROOT / "src")
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "experiments/run_benchmarks.py"),
            "--skip-neural",
            "--output-root",
            str(tmp_path),
        ],
        cwd=tmp_path,
        env=environment,
        capture_output=True,
        text=True,
        check=True,
    )
    output = tmp_path / "results/benchmarks"
    actual = json.loads((output / "results.json").read_text(encoding="utf-8"))
    saved = json.loads((ROOT / "results/benchmarks/results.json").read_text(encoding="utf-8"))
    for key in [
        "K",
        "Sigma_infinity",
        "det_exact",
        "OU_Cfull_t1",
        "OU_Cclosure_t1",
        "matrix_exponential_false_frobenius_error",
        "A_commutator_frobenius_norm",
    ]:
        np.testing.assert_allclose(actual[key], saved[key], rtol=1e-12, atol=1e-12)
    for name in ["jacobian_convergence.csv", "affine_regression.csv", "markov_semidiscrete.csv"]:
        with (output / name).open(newline="", encoding="utf-8") as file:
            rows = list(csv.reader(file))
        with (ROOT / "results/benchmarks" / name).open(newline="", encoding="utf-8") as file:
            baseline = list(csv.reader(file))
        assert rows[0] == baseline[0]
        np.testing.assert_allclose(
            np.array(rows[1:], float), np.array(baseline[1:], float), rtol=1e-10, atol=1e-12
        )
    assert actual["ML"] == []
    assert not (output / "conditional_regression.csv").exists()
    assert not (tmp_path / "paper/figures/conditional_regression.pdf").exists()
