# Unselected questions: oral discussion & future study map

**Purpose:** Explain the mathematical object, the principal method, the potential failure, and a concrete next step without claiming to have solved the original question. The local source is [StudentAssessmentExercise_unlocked.pdf](StudentAssessmentExercise_unlocked.pdf). These notes are study plans, not submitted proofs or an independent audit of suspected source errors.

Project 10 items 1–4 are now incorporated in Chapter 1 with a Hamiltonian oscillator experiment; they are no longer a wholly deferred project. Projects 8, 9 and selected items of 11–14 are mapped in [source_mapping.md](source_mapping.md). Unmapped items within those projects are not implicitly claimed solved.

| Project | 30-second research explanation | What is not yet established | Next method / study priority |
|---|---|---|---|
| 1 Numerical PDE | Compare a consistent finite-difference method to nonlinear neural residual minimization; operator learning extends a single forcing term to a function-to-function map. | Global error estimates for the neural optimizer, robustness out of training distribution; check whether the PDE and stencil agree. | Check the sign/potential first, then convergence study, then controlled operator-learning baseline. |
| 2 Failure of the PINN | Discrete collocation residual convergence need not imply PDE solution convergence unless one has stability/regularity and an appropriate norm bound. | Construct the requested differentiable sequence and check the temporal sample-grid quantifiers rigorously. | Make an explicit cutoff sequence and distinguish empirical from population residual. |
| 3 High-dimensional committor learning | A committor is a hitting probability, solving a backward elliptic boundary-value problem. A learned solution must obey probabilistic bounds and boundary data. | Validated d>=10 solver; no curse-of-dimensionality claim without complexity accounting. | Monte Carlo hitting-probability baseline, residual+boundary checks, restrict parametric potential family. |
| 4 WKB/Kramers | Study small-noise escape scaling governed by barrier heights and prefactors. | Full matched asymptotic analysis / higher-dimensional proof; check the OU exit-time equation and boundary data in the source. | Backward generator boundary problem -> one-dimensional exact integral -> Laplace method -> multi-dimensional saddle prefactor. |
| 5 McKean–Vlasov | Interacting-particle empirical measure has deterministic McKean–Vlasov law in the large-N limit, with martingale fluctuations of order N^(-1/2). | Uniform propagation-of-chaos rates and all invariant-law cases. | Derive mean and covariance ODE; particle code; Ito isometry/Grönwall proof. |
| 6 Colored noise | Fast OU forcing may converge to effective white noise in a weak-limit sense, but the coupled scaling and nonlinear mean-field term matter. | Identify exact scaling and coupling from the problem before asserting the limit or strong convergence. | Generator multiscale expansion and diffusion approximation; covariance-based test. |
| 7 Foundations | PSD matrix inequality via Schur complement; score as conditional expectation of conditional score under differentiation/integrability conditions. | Generalization beyond Gaussian/noise assumptions and boundary cases. | Prove through quadratic forms and dominated differentiation. |
| 15 Feynman–Kac | Semigroup expectation solves the backward Kolmogorov equation while density evolves under the adjoint. A density ratio relative to invariant law evolves under a conjugated/time-reversed generator in general. | Reversible versus nonreversible hypothesis in the PDF. | Work out the generator conjugacy and test nonreversible OU counterexamples. |
| 16 Jarzynski equality | Exponentially weighted nonequilibrium work recovers equilibrium partition-function ratios despite the actual time marginal not being instantaneous Gibbs. | Full Feynman–Kac path-functional proof and verified work variance. | Prove finite-time identity with exponential martingale/Feynman–Kac, then driven harmonic-trap simulation. |
| 17 Diffusion bridge | Conditioning on an endpoint event changes the drift by a Doob h-transform; Girsanov describes the RN derivative between suitable path measures. | End-point singularities and integrability/Novikov hypotheses; check the source drift coefficient. | Backward h equation, transformed generator, Brownian bridge benchmark, RN derivative check. |
| 18 Wasserstein gradient flow | JKO proximal minimization of free energy in W2 produces Fokker–Planck as a gradient flow under suitable conditions. Parametrized families inherit a non-Euclidean metric. | Geodesic convexity, rigorous time-step limit, explicit Gaussian-mixture pullback metric; check the source parameter convention. | Start with Gaussian manifold closed-form W2, then JKO and mixture approximation. |

## Oral-answer skeleton (use for each deferred project)

1. State the precise object and its governing equation.
2. Separate the established exact statement from any limit/approximation and list needed hypotheses.
3. Explain the physical meaning or geometric meaning.
4. Give a benchmark with an analytic limit and a reproducible numerical scheme.
5. State the specific unresolved derivation and the text/paper or theorem you would study next.

Do not present an unfinished chapter as solved. It is better to say "I can derive the generator and identify the appropriate boundary-value problem; I have not yet justified the asymptotic matching" than to claim a proof without handling boundary layers.
