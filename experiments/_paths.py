"""Output configuration shared by benchmark entry points; no import-time writes."""

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class OutputPaths:
    """Mirror the repository layout under a chosen root for isolated reruns."""

    root: Path = ROOT

    @property
    def figures(self) -> Path:
        return self.root / "paper" / "figures"

    @property
    def results(self) -> Path:
        return self.root / "results" / "benchmarks"

    def prepare(self) -> None:
        """Create output directories only when a benchmark explicitly runs."""
        self.figures.mkdir(parents=True, exist_ok=True)
        self.results.mkdir(parents=True, exist_ok=True)


def argument_parser(description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "--output-root",
        type=Path,
        default=ROOT,
        help="Output root containing paper/figures and results/benchmarks (default: repository)",
    )
    return parser


def write_rows(path: Path, rows: list[dict]) -> None:
    """Write nonempty benchmark records with their existing column order."""
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0])
        writer.writeheader()
        writer.writerows(rows)
