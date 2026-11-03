# Current research scope and acceptance criteria

This file describes the current repository, replacing the earlier phase-1 plan. See [the project guide](project_guide.md) for reading order and verification status, and [the source map](source_mapping.md) for exact selected items.

## Mathematical backbone

\(X_t\to\mathcal L,\mathcal L^*\to\rho_t\to\nu_t=\xi_\#\rho_t\to\mathbb E[\mathcal L(\varphi\circ\xi)\mid\xi(X_t)=z]\to(b_t,a_t)\to\) Markovian marginal projection. At equilibrium, disintegration of the Gibbs measure produces free energy \(F(z)\) and mean force. For gradient diffusions, relative entropy to Gibbs is a Lyapunov function. A probability-flow velocity converts a Fokker–Planck evolution into a continuity equation when density and coefficients are sufficiently regular.

## Current coverage

| Area | Material currently present | Remaining validation or extension |
|---|---|---|
| State / observable / measure language | Section 1.1 definitions and duality | Independent mathematical review |
| Deterministic transport and information identities | Project 9.1–9.15; selected Project 11 results in §§1.2 and 1.4 | Review hypotheses; distinguish formal kinetic stationarity from an optimizer theorem |
| Hamiltonian application | Project 10.1–10.4, oscillator formulas, Euler / Verlet data and two figures in §1.2 | Broader potentials and step-size studies |
| Conditional geometry and effective dynamics | Project 12.1–12.4 and 13.1–13.3 in §1.3 | Review regularity, integrability and forward-equation well-posedness assumptions |
| Learned flow construction | Project 14.1–14.3 and a finite-sample conditional-regression experiment | Multi-seed training, saved models, dynamical validation |
| Numerical probability evolution | Project 8 generator / centered-scheme analysis, mass / positivity / KL data | Spatial refinement and an independent fine-grid reference |
| Coupled OU model | Exact Gaussian moments, projected drift, correlation counterexample, affine and neural regression | Unify experiment and library implementations; expand tests |
| Nonlinear double well | Analytic equilibrium free energy and a research protocol | Numerical experiment remains unexecuted |

The presence of a proof in the manuscript is recorded as manuscript coverage, not as independent verification of all mathematical claims. Existing Python tests cover the reusable OU core, not every area above.

## Next priorities

1. Establish and record one complete experiment environment, including PyTorch and SciPy; preserve code version, dependency versions and run outputs.
2. Add multiple seeds and uncertainty summaries to the conditional-regression comparison. The current neural error is not monotone in training size.
3. Reduce repeated OU formulas across the library and experiment script, with explicit shared parameters and checks for new numerical components.
4. Execute the nonlinear double-well benchmark. Validate known equilibrium free energy separately from nonstationary drift, correlations and transition statistics.
5. Develop specialized later modules only after selecting a concrete question; see [future research modules](future_research_modules.md).

## Proof checklist

- Specify stochastic basis, Brownian dimensions, coefficient regularity and growth conditions.
- Justify existence of the diffusion, any invariant measure, and differentiability/integrability exchanges.
- Use \(\mathcal L\) for observables and \(\mathcal L^*\) for distributions.
- Distinguish pushforward measure from a process with a Markov property.
- State precisely which boundary conditions give flux conservation.
- For mimicking, require sufficient conditions for weak solutions and uniqueness of the induced Fokker–Planck problem; the weak identity by itself does not ensure existence or uniqueness.
- For AI, compare conditional-mean regression to exact or high-accuracy estimators, and track probability error separately from trajectory error.

## Numerical checks

- Strong/weak convergence of the integrator as relevant; discrete mass conservation and positivity.
- Exact Gaussian time-marginal baselines before nonlinear models.
- Mean, covariance, stationary two-time covariance, and distributional distances.
- Initial states both at equilibrium and out of equilibrium.
- Error sources split by sampling, function approximation, time discretization, and model reduction.

## Deliverable format

`paper/main.tex` is the editable manuscript; `paper/ref.bib` is its bibliography. `src/` contains the reusable OU library, `tests/` its mathematical regression checks, and `experiments/` both executable benchmarks and saved CSV/JSON data. Figures are generated in `paper/figures/`; compiled manuscript files go to `paper/Tmp/`. `results/` is reserved and is not the current destination of either experiment script. Local verification scratch files under `results/validation/` are ignored.

Run instructions and output ownership are maintained in [reproduction.md](reproduction.md).
