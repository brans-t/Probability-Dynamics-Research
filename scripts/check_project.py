"""Check repository paths, manuscript references, and optional snapshot fidelity.

Uses only the Python standard library. Run from any directory.
The baseline check is specific to formatting and file moves: it ignores only
comments, whitespace, display alignment, math spacing, and repeated clearpage.
It does not validate mathematical claims or reproduce neural training.
"""

import argparse
import ast
import csv
import hashlib
from pathlib import Path
import re
import runpy
import struct
import sys
import zipfile


ROOT = Path(__file__).resolve().parents[1]
ROW = re.compile(r"\\sourceindexrow\{([^}]+)\}\{([^}]+)\}\{([^}]+)\}\{([^}]+)\}")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def canonical_body(text):
    """Retain every prose/math character except the formatting allowlist."""
    body = text.split(r"\begin{document}", 1)[1]
    body = re.sub(r"(?<!\\)%[^\n]*", "", body)
    body = re.sub(r"\\(?:begin|end)\{(?:aligned|split)\}", "", body)
    body = re.sub(r"\\\\(?:\[[^\]]*\])?", "", body)
    body = re.sub(r"\\(?:qquad|quad|enspace|thinspace)\b|\\[,;:!]", "", body)
    body = re.sub(r"\s+|&", "", body)
    return re.sub(r"(?:\\clearpage){2,}", r"\\clearpage", body)


def expand_notation(tex, read_text):
    """Include the notation chapter in source and archive checks."""
    directive = r"\input{notation}"
    if directive not in tex:
        return tex
    require(tex.count(directive) == 1, "Expected one notation chapter include")
    return tex.replace(directive, read_text("paper/notation.tex").rstrip("\r\n"))


def check_manuscript():
    main = (ROOT / "paper/main.tex").read_text(encoding="utf-8")
    require(main.count(r"\input{notation}") == 1, "Separate notation chapter not included")
    tex = expand_notation(main, lambda name: (ROOT / name).read_text(encoding="utf-8"))
    preamble = (ROOT / "paper/preamble.tex").read_text(encoding="utf-8")
    labels = re.findall(r"\\label\{([^}]+)\}", tex)
    require(len(labels) == len(set(labels)), "Duplicate manuscript labels")
    references = re.findall(r"\\(?:eqref|ref|pageref\*?|hyperref)\{([^}]+)\}", tex)
    references += re.findall(r"\\hyperref\[([^\]]+)\]", tex)
    require(set(references) <= set(labels), f"Missing labels: {set(references) - set(labels)}")
    rows = ROW.findall(tex)
    require(len(rows) == 45, "Expected 45 assessment source-index rows")
    require(
        {r[1] for r in rows if r[0] == "11"} == {str(i) for i in range(1, 14)},
        "Project 11 source index must include all 13 items",
    )
    require(all(row[2] in labels for row in rows), "Unresolved source-index target")
    with (ROOT / "docs/source_index.tsv").open(encoding="utf-8", newline="") as f:
        index = list(csv.reader(f, delimiter="\t"))
    require(index[0] == ["project", "item", "label", "placement"], "Unexpected TSV columns")
    require([tuple(row) for row in index[1:]] == rows, "TSV differs from manuscript source index")
    figures = re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", tex)
    require(len(figures) == 6, "Expected six manuscript figures")
    for figure in figures:
        require((ROOT / "paper" / figure).is_file(), f"Missing figure: {figure}")
    animation_frames = []
    animations = re.findall(
        r"\\animategraphics\s*(?:\[[^\]]*\])?\s*\{(\d+)\}\s*\{([^}]+)\}\s*\{(\d+)\}\s*\{(\d+)\}",
        tex,
    )
    for fps, prefix, first, last in animations:
        require(int(fps) > 0 and int(first) <= int(last), "Invalid animation frame range")
        dimensions = set()
        for number in range(int(first), int(last) + 1):
            frame = f"{prefix}{number}.png"
            frame_path = ROOT / "paper" / frame
            require(frame_path.is_file(), f"Missing animation frame: {frame}")
            with frame_path.open("rb") as image:
                header = image.read(24)
            require(header[:8] == b"\x89PNG\r\n\x1a\n" and len(header) == 24, f"Invalid PNG: {frame}")
            dimensions.add(struct.unpack(">II", header[16:24]))
            animation_frames.append(frame)
        require(len(dimensions) == 1, f"Inconsistent animation dimensions: {prefix}")
    # Retain the supplementary matrix-flow benchmark plot, omitted from the
    # manuscript because the scalar experiment already illustrates convergence.
    benchmark_figures = {"figures/jacobian_convergence.pdf"}
    require(
        {p.relative_to(ROOT / "paper").as_posix() for p in (ROOT / "paper/figures").rglob("*") if p.is_file()}
        == set(figures + animation_frames) | benchmark_figures,
        "Unreferenced or missing files in paper/figures",
    )
    bib = (ROOT / "paper/ref.bib").read_text(encoding="utf-8")
    keys = set(re.findall(r"@\w+\s*\{([^,]+),", bib))
    cited = set()
    for group in re.findall(r"\\(?:cite|textcite|parencite)\{([^}]+)\}", tex):
        cited.update(group.split(","))
    require(cited <= keys, f"Missing bibliography keys: {cited - keys}")
    require(r"\input{preamble}" in tex, "Shared preamble not included")
    require(r"\addbibresource{ref.bib}" in preamble, "Bibliography path changed")
    print(
        f"Manuscript: {len(labels)} labels, {len(rows)} source links, {len(figures)} figures, "
        f"{len(animation_frames)} animation frames, {len(cited)} citation keys OK"
    )
    return tex


def check_repository():
    for directory in ("src", "tests", "experiments", "scripts"):
        for p in (ROOT / directory).rglob("*.py"):
            ast.parse(p.read_text(encoding="utf-8"), filename=str(p))
    for p in [ROOT / "README.md", *(ROOT / "docs").glob("*.md")]:
        for link in re.findall(r"\[[^\]\n]*\]\(([^)\n]+)\)", p.read_text(encoding="utf-8")):
            if re.match(r"[a-z]+://|mailto:|#", link):
                continue
            target = link.split("#", 1)[0]
            if target:
                require((p.parent / target).exists(), f"Broken link in {p.name}: {link}")
    require(not list((ROOT / "experiments").glob("*.csv")), "CSV data remains in experiments")
    require(not list((ROOT / "experiments").glob("*.json")), "JSON data remains in experiments")
    require(
        len(list((ROOT / "results/benchmarks").glob("*.csv"))) == 7, "Expected seven saved CSV files"
    )
    require(
        len(list((ROOT / "results/benchmarks").glob("*.json"))) == 2,
        "Expected two saved JSON files",
    )
    # Validate the configuration itself instead of matching its implementation text.
    paths = runpy.run_path(str(ROOT / "experiments/_paths.py"))["OutputPaths"]()
    require(paths.figures == ROOT / "paper/figures", "Wrong experiment figure directory")
    require(paths.results == ROOT / "results/benchmarks", "Wrong experiment data directory")
    print("Repository: Python syntax, documentation links, shared paths, saved data OK")


def check_baseline(path, tex):
    with zipfile.ZipFile(path) as baseline:
        old = expand_notation(
            baseline.read("paper/main.tex").decode("utf-8"),
            lambda name: baseline.read(name).decode("utf-8"),
        )
        require(
            canonical_body(old) == canonical_body(tex),
            "Manuscript body changed beyond the formatting allowlist",
        )
        # Preserve numbering environments, references, source links, headings,
        # and all non-layout environments separately from the token comparison.
        for command in (
            r"\\label\{[^}]+\}",
            r"\\cite\{[^}]+\}",
            r"\\(?:chapter|section|paragraph)\*?\{[^\n]+",
            r"\\(?:begin|end)\{(?:equation\*?|align\*?|theorem|proof|example|solution)\}",
        ):
            old_body = old.split(r"\begin{document}", 1)[1]
            require(
                re.findall(command, old_body) == re.findall(command, tex),
                f"Content/numbering structure changed: {command}",
            )
        preserved = 0
        for name in baseline.namelist():
            target = ROOT / name
            if name.startswith("experiments/") and Path(name).suffix in {".csv", ".json"}:
                target = ROOT / "results/benchmarks" / Path(name).name
            elif not (
                name.startswith(("src/", "tests/", "paper/figures/"))
                or name
                in {
                    "paper/ref.bib",
                    "LICENSE",
                    "pyproject.toml",
                }
            ):
                continue
            if name.endswith(".png"):
                continue
            require(target.read_bytes() == baseline.read(name), f"Preserved asset differs: {name}")
            preserved += 1
        digest = hashlib.sha256(canonical_body(tex).encode()).hexdigest()
    print(
        f"Baseline: body tokens and numbering unchanged; {preserved} source/data/assets byte-identical"
    )
    print(f"Body SHA-256 (formatting removed): {digest}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--baseline", type=Path, help="ZIP snapshot taken before formatting and moves"
    )
    args = parser.parse_args()
    tex = check_manuscript()
    check_repository()
    if args.baseline:
        check_baseline(args.baseline, tex)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, zipfile.BadZipFile) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        sys.exit(1)
