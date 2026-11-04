"""Shared output locations for all benchmark scripts."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "paper" / "figures"
RESULTS = ROOT / "results" / "benchmarks"

for directory in (FIGURES, RESULTS):
    directory.mkdir(parents=True, exist_ok=True)
