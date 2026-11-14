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
ALL_ROWS = re.compile(r"\\sourceindex(?:omitted)?row\{([^}]+)\}\{([^}]+)\}\{([^}]+)\}\{([^}]+)\}")
OMITTED_ROW = re.compile(r"\\sourceindexomittedrow\{([^}]+)\}\{([^}]+)\}\{([^}]+)\}\{([^}]+)\}")


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
    """Expand notation and legacy PDE includes in source/archive checks.

    The current PDE chapter is inline in main.tex. Keep the old include
    expansion for historical archives that still contain a separate file.
    """
    module = r"\input{neural_pde}"
    if module in tex:
        require(tex.count(module) == 1, "Expected one neural PDE include")
        tex = tex.replace(module, read_text("paper/neural_pde.tex").rstrip("\r\n"))
    directive = r"\input{notation}"
    if directive not in tex:
        return tex
    require(tex.count(directive) == 1, "Expected one notation chapter include")
    return tex.replace(directive, read_text("paper/notation.tex").rstrip("\r\n"))


def check_manuscript():
    main = (ROOT / "paper/main.tex").read_text(encoding="utf-8")
    require(main.count(r"\input{notation}") == 1, "Separate notation chapter not included")
    require(r"\input{neural_pde}" not in main, "Neural PDE chapter must be inline in main.tex")
    require(main.count(r"\label{ch:neural-pde}") == 1, "Expected one inline neural PDE chapter")
    source_tex = expand_notation(main, lambda name: (ROOT / name).read_text(encoding="utf-8"))
    # Deferred answers remain in line comments. Only live labels/references and
    # source-index rows participate in compiled navigation checks.
    tex = re.sub(r"(?<!\\)%[^\n]*", "", source_tex)
    preamble = (ROOT / "paper/preamble.tex").read_text(encoding="utf-8")
    labels = re.findall(r"\\label\{([^}]+)\}", tex)
    require(len(labels) == len(set(labels)), "Duplicate manuscript labels")
    references = re.findall(r"\\(?:eqref|ref|pageref\*?|hyperref)\{([^}]+)\}", tex)
    references += re.findall(r"\\hyperref\[([^\]]+)\]", tex)
    require(set(references) <= set(labels), f"Missing labels: {set(references) - set(labels)}")
    rows = ALL_ROWS.findall(tex)
    require(len(rows) == 47, "Expected 47 assessment source-index rows")
    require(
        {(row[0], row[1]) for row in rows if row[0] in {"2", "3"}}
        == {("2", "Main task"), ("3", "Main task")},
        "Neural PDE source index must include Projects 2 and 3",
    )
    require(
        {r[1] for r in rows if r[0] == "11"} == {str(i) for i in range(1, 14)},
        "Project 11 source index must include all 13 items",
    )
    linked_rows = ROW.findall(tex)
    require(all(row[2] in labels for row in linked_rows), "Unresolved source-index target")
    preserved_labels = set(re.findall(r"\\label\{([^}]+)\}", source_tex))
    for row in OMITTED_ROW.findall(tex):
        require(row[2] not in labels, f"Included source marked omitted: {row[2]}")
        require(row[2] in preserved_labels, f"Omitted source label not preserved: {row[2]}")
    with (ROOT / "docs/source_index.tsv").open(encoding="utf-8", newline="") as f:
        index = list(csv.reader(f, delimiter="\t"))
    require(index[0] == ["project", "item", "label", "placement"], "Unexpected TSV columns")
    require([tuple(row) for row in index[1:]] == rows, "TSV differs from manuscript source index")
    figures = re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", tex)
    preserved_figures = re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", source_tex)
    require(len(preserved_figures) == 6, "Expected six preserved manuscript figures")
    for figure in preserved_figures:
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
        == set(preserved_figures + animation_frames) | benchmark_figures,
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
        f"Manuscript: {len(labels)} labels, {len(linked_rows)} source links, "
        f"{len(rows) - len(linked_rows)} omitted entries, {len(figures)} figures, "
        f"{len(animation_frames)} animation frames, {len(cited)} citation keys OK"
    )
    return tex


def check_repository():
    for directory in ("paper", "slides"):
        for p in (ROOT / directory).rglob("*.tex"):
            content = p.read_text(encoding="utf-8")
            require(not re.search(r"\\mathscr\b|mathrsfs", content), f"Retired script font in {p}")
            require(
                not re.search(r"b(?:_\{?[^\s^]+)?\^\{\\mathrm\{aff\}\}", content),
                f"Use B_t for affine forcing in {p}",
            )
    for directory in ("src", "tests", "experiments", "scripts"):
        for p in (ROOT / directory).rglob("*.py"):
            ast.parse(p.read_text(encoding="utf-8"), filename=str(p))
    for p in [ROOT / "README.md", *(ROOT / "docs").glob("*.md"), *(ROOT / "slides").glob("*.md")]:
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
    slide_source = (ROOT / "slides/project9_exercises1_2.tex").read_text(encoding="utf-8")
    # The current deck factors its frames into section includes. Follow those
    # declared sources before checking diagram usage, rather than treating all
    # diagrams as unused merely because they moved out of the entry point.
    for name in re.findall(r"\\input\{\\sectionroot\s+([^}]+)\}", slide_source):
        slide_source += "\n" + (ROOT / "slides/sections" / (name + ".tex")).read_text(
            encoding="utf-8"
        )
    used_diagrams = set(re.findall(r"\\input\{\\diagramroot\s+([^}]+)\}", slide_source))
    used_diagrams.update(
        name + ".tex"
        for name in re.findall(r"\\flowdiagram(?:\[[^\]]+\])?\{([^}]+)\}", slide_source)
    )
    diagram_directory = ROOT / "slides/diagrams/project9"
    # Retained alternatives from earlier slide layouts; keep them available
    # without requiring an unrelated deck edit in a manuscript revision.
    retained_diagrams = {"state.tex", "reversal.tex", "nonlinear.tex"}
    require(
        used_diagrams | retained_diagrams == {p.name for p in diagram_directory.glob("*.tex")},
        "Missing or unused slide TikZ source",
    )
    output = ROOT / "output"
    if output.exists():
        require(
            {p.name for p in output.iterdir()} <= {"paper", "slides"},
            "Only output/paper and output/slides are retained",
        )
        for directory in output.iterdir():
            require(directory.is_dir(), f"Expected output directory: {directory}")
            require(
                all(p.is_file() and p.suffix.lower() == ".pdf" for p in directory.iterdir()),
                f"{directory.relative_to(ROOT)} must contain only PDFs",
            )
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
