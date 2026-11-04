"""Run the matrix-flow, OU, conditional-regression, and Markov benchmarks."""

import json

from _paths import OutputPaths, argument_parser
import conditional_regression
import markov
import matrix_flow

SEED = 20261102


def main(argv: list[str] | None = None) -> None:
    parser = argument_parser(__doc__)
    parser.add_argument(
        "--skip-neural",
        action="store_true",
        help="Run the affine baseline without installing or training PyTorch",
    )
    args = parser.parse_args(argv)
    # Check the optional dependency before writing any outputs.
    if not args.skip_neural:
        conditional_regression.require_torch()
    paths = OutputPaths(args.output_root.resolve())
    paths.prepare()
    results = {"seed": SEED}
    results.update(matrix_flow.run(paths))
    results.update(conditional_regression.run(paths, seed=SEED, neural=not args.skip_neural))
    results.update(markov.run(paths))
    (paths.results / "results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
