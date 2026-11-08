"""Audit formatting, preservation, counters, and PDF navigation after revision.

Unlike check_project.py's strict formatting baseline mode, this checker permits
reviewed mathematical revisions while requiring original material/anchors/assets.
It does not prove mathematical correctness; see docs/README.md.
"""

import argparse
from collections import Counter
import json
from pathlib import Path
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
import zipfile

from check_project import ROOT, check_manuscript, check_repository, expand_notation, require


STATEMENTS = (
    "definition",
    "theorem",
    "proposition",
    "corollary",
    "lemma",
    "example",
    "exercise",
    "remark",
    "assumption",
    "Notice",
)


def groups(text):
    """Read top-level TeX brace groups, preserving nested command arguments."""
    values = []
    depth = 0
    start = None
    for i, ch in enumerate(text):
        if i and text[i - 1] == "\\":
            continue
        if ch == "{":
            if depth == 0:
                start = i + 1
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                values.append(text[start:i])
    return values


def labels_from_aux():
    aux = (ROOT / "output/paper/main.aux").read_text(encoding="utf-8")
    result = {}
    for line in aux.splitlines():
        if line.startswith("\\newlabel{"):
            outer = groups(line)
            if len(outer) == 2:
                result[outer[0]] = groups(outer[1])
    return result


def numbered_displays(text):
    count = 0
    for match in re.finditer(r"\\begin\{(equation|align)\}(.*?)\\end\{\1\}", text, re.S):
        if match[1] == "equation":
            count += 1
            continue
        rows = [""]
        depth = 0
        for token in re.split(r"(\\begin\{[^}]+\}|\\end\{[^}]+\}|\\\\(?:\[[^\]]*\])?)", match[2]):
            if token.startswith("\\begin{"):
                depth += 1
            elif token.startswith("\\end{"):
                depth -= 1
            if token.startswith("\\\\") and depth == 0:
                rows.append("")
            else:
                rows[-1] += token
        count += sum(
            bool(row.strip()) and not re.search(r"\\(?:notag|nonumber)\b", row) for row in rows
        )
    return count


def source_checks(tex):
    clean = re.sub(r"(?<!\\)%[^\n]*", "", tex)
    require(not re.search(r"(?<!\\)\\[\[\]]", clean), "Bracket display math remains")
    require(r"\begin{align*}" not in clean, "align* remains")
    require(r"\(" not in clean and r"\)" not in clean, "Non-dollar inline math remains")
    require("$$" not in clean, "Double-dollar display remains")
    require(r"\begin{defn}" not in clean, "Independent defn environment remains")
    for equation in re.findall(r"\\begin\{equation\}(.*?)\\end\{equation\}", clean, re.S):
        if r"\label{" in equation:
            require(
                re.fullmatch(r"(?:\\label\{[^}]+\}\s*)+", equation.strip().splitlines()[-1].strip()),
                "Equation labels must be on the final line before the environment ends",
            )
    stack = []
    for kind, name in re.findall(r"\\(begin|end)\{([^}]+)\}", clean):
        if kind == "begin":
            stack.append(name)
        else:
            require(bool(stack) and stack.pop() == name, f"Unbalanced environment: {name}")
    require(not stack, f"Unclosed environments: {stack}")
    first = tex.split(r"\section{State Spaces", 1)[1].split(r"\section{Dynamical Flows", 1)[0]
    for forbidden in [
        r"\mathcal B(E)",
        r"\mathcal P(E)",
        r"\int_E",
        r"\label{eq:generator-definition}",
        r"\label{eq:pushforward-test}",
    ]:
        require(forbidden not in first, f"Foundation scope violation: {forbidden}")
    for m in re.finditer(r"[UT]_(?:F|G|\{G\\circ F\})|P_\{(?:s,t|t,t\+h)\}", clean):
        require(
            clean[max(0, m.start() - 8) : m.start()].endswith("\\mathsf "),
            f"Bare evolution operator: {m[0]}",
        )
    aligns = re.findall(r"\\begin\{align\}(.*?)\\end\{align\}", clean, re.S)
    require(not aligns, "Use equation/equation* with aligned for grouped formulas")
    formula_refs = set(re.findall(r"\\(?:eqref|ref|pageref\*?|autoref|nameref)\{([^}]+)\}", clean))
    formula_refs.update(re.findall(r"\\hyperref\[([^\]]+)\]", clean))
    for environment, body in re.findall(
        r"\\begin\{(equation\*?)\}(.*?)\\end\{\1\}", clean, re.S
    ):
        labels = set(re.findall(r"\\label\{([^}]+)\}", body))
        if environment == "equation*":
            require(not labels, "Unnumbered equation must not contain labels")
        else:
            require(bool(labels), "Unreferenced display must use equation*")
            require(labels <= formula_refs, f"Unused formula labels: {labels-formula_refs}")
    print(
        "Source: display conventions, operator spelling, environment balance, and foundational scope OK"
    )


def preservation(tex, baseline):
    # The approved notation chapter adds only unnumbered reference tables.
    # Exclude precisely that marked block when checking the original displays;
    # all original statements, tables, labels, citations and assets stay checked.
    core_tex = tex
    notation_start = "% BEGIN GLOBAL NOTATION"
    notation_end = "% END GLOBAL NOTATION"
    if notation_start in tex or notation_end in tex:
        require(tex.count(notation_start) == tex.count(notation_end) == 1,
                "Notation chapter markers must be unique and paired")
        first = tex.index(notation_start)
        last = tex.index(notation_end, first) + len(notation_end)
        notation = tex[first:last]
        require(r"\chapter*{Notation and Conventions}" in notation,
                "Notation block must be the unnumbered notation chapter")
        require(not re.search(r"\\begin\{(?:equation|theorem|proof|table|figure)\}", notation),
                "Notation block may not hide original scientific displays")
        require(not re.search(r"\\(?:sourcecredit|sourceindexrow|cite)\{", notation),
                "Notation block may not hide source identifiers or citations")
        core_tex = tex[:first] + tex[last:]
    with zipfile.ZipFile(baseline) as archive:
        old = expand_notation(
            archive.read("paper/main.tex").decode("utf-8"),
            lambda name: archive.read(name).decode("utf-8"),
        )
        old_labels = set(re.findall(r"\\label\{([^}]+)\}", old))
        new_labels = set(re.findall(r"\\label\{([^}]+)\}", tex))
        require(old_labels <= new_labels, f"Original labels removed: {old_labels-new_labels}")
        for pattern in [
            r"\\sourcecredit\{[^}]+\}\{[^}]+\}",
            r"\\sourceindexrow\{[^}]+\}\{[^}]+\}\{[^}]+\}\{[^}]+\}",
            r"\\cite\{[^}]+\}",
        ]:
            require(
                Counter(re.findall(pattern, old)) == Counter(re.findall(pattern, tex)),
                f"Original citations/source identifiers changed: {pattern}",
            )
        for env in [*STATEMENTS, "proof", "solution", "figure", "table", "longtable"]:
            before = old.count("\\begin{" + env + "}")
            if env == "definition":
                before += old.count(r"\begin{defn}")
            require(before == core_tex.count("\\begin{" + env + "}"), f"Material count changed: {env}")
        require(
            numbered_displays(old) == numbered_displays(tex),
            "Original numbered formula count changed",
        )
        for env in ["Notice", "figure", "table", "longtable"]:
            pattern = r"\\begin\{" + env + r"\}(?:\[([^\n]*)\])?"
            old_options = [m[1] for m in re.finditer(pattern, old)]
            new_options = [m[1] for m in re.finditer(pattern, core_tex)]
            # Thematic regrouping can move a Notice with its proposition.
            # Require the same complete collection instead of its old order.
            if env == "Notice":
                old_options, new_options = Counter(old_options), Counter(new_options)
            require(
                old_options == new_options, f"Original environment title/options changed: {env}"
            )
        unchanged = 0
        for name in archive.namelist():
            if name.startswith(
                ("results/benchmarks/", "paper/figures/", "src/", "tests/")
            ) or name in {
                "paper/ref.bib",
                "docs/StudentAssessmentExercise_unlocked.pdf",
                "docs/source_index.tsv",
            }:
                require(
                    (ROOT / name).read_bytes() == archive.read(name),
                    f"Protected file changed: {name}",
                )
                unchanged += 1
        sections = re.findall(r"\\section\{([^\n]+)\}", old)
        require(
            sections == re.findall(r"\\section\{([^\n]+)\}", tex),
            "Main/appendix section framework changed",
        )
    print(
        f"Preservation: {len(old_labels)} old labels, all statements/proofs/Notices/displays, {unchanged} protected files OK"
    )
    return {
        "original_labels": len(old_labels),
        "protected_files": unchanged,
        "numbered_formulas": numbered_displays(tex),
    }


def pdf_checks(tex):
    pdf = ROOT / "output/paper/main.pdf"
    aux = labels_from_aux()
    destinations = subprocess.check_output(
        ["pdfinfo", "-dests", str(pdf)], encoding="utf-8", errors="replace"
    )
    dest = {}
    for line in destinations.splitlines():
        m = re.match(r'\s*(\d+)\s+\[.*?\]\s+"([^"]+)"', line)
        if m:
            require(m[2] not in dest, f"Duplicate PDF destination: {m[2]}")
            dest[m[2]] = int(m[1])
    for label in [
        "sec:flows-transport",
        "sec:conditional-dynamics",
        "sec:learnedflows",
        "sec:benchmark",
        "subsec:entropy",
        "subsec:effective",
        "subsec:numerical",
        "subsec:hamiltonian-application",
    ]:
        require(label in aux, f"Unresolved hierarchy label: {label}")
        expected = "subsection." if label.startswith("subsec:") else "section."
        require(
            aux[label][3].startswith(expected), f"Wrong counter/anchor for {label}: {aux[label]}"
        )
    for source, statement in [
        ("src:p9q6", "ex:weightedaction"),
        ("src:p9q13", "thm:flow-kl-variation"),
    ]:
        require(
            aux[source][3] == aux[statement][3],
            f"Cross-page source target detached from statement heading: {source}",
        )
    xml_bytes = subprocess.check_output(
        ["pdftohtml", "-xml", "-hidden", "-i", "-stdout", str(pdf)], stderr=subprocess.DEVNULL
    )
    document = ET.fromstring(xml_bytes)
    source_links = [
        a for a in document.findall(".//a") if "".join(a.itertext()).startswith("Project ")
    ]
    rows = re.findall(r"\\sourceindexrow\{[^}]+\}\{[^}]+\}\{([^}]+)\}\{[^}]+\}", tex)
    require(len(source_links) == len(rows) == 45, "PDF source-entry link count is not 45")
    for label, link in zip(rows, source_links):
        require(label in aux and aux[label][3] in dest, f"No live PDF destination for {label}")
        require(
            link.get("href", "").rsplit("#", 1)[-1] == str(dest[aux[label][3]]),
            f"Source link jumps to wrong page: {label}",
        )
    nav = [
        a
        for a in document.findall(".//a")
        if re.match(r"Overview: HNN|S[1-6]\s", "".join(a.itertext()))
    ]
    require(not nav, "Removed HNN appendix still has supplementary navigation")
    require(not any(label.startswith("app:hnn") for label in aux),
            "Removed HNN appendix still has compiled labels")
    require(aux["app:ode-foundations"][0] == "A", "ODE foundations must be Appendix A")
    text = subprocess.check_output(["pdftotext", "-layout", str(pdf), "-"], encoding="utf-8")
    headings = re.findall(
        r"^\s*(Definition|Theorem|Proposition|Corollary|Lemma|Example|Exercise|Remark|Assumption)\s+((?:\d+|[A-Z])\.\d+)(?=[ \t]*\(|\.[ \t]+\S)",
        text,
        re.M,
    )
    # Statement counters reset at each numbered chapter, including appendices.
    # Read the chapter order from the source instead of assuming chapter 1.
    statement_envs = "|".join(env for env in STATEMENTS if env != "Notice")
    tokens = re.finditer(
        r"\\appendix\b|\\chapter\{|\\begin\{(" + statement_envs + r")\}",
        re.sub(r"(?<!\\)%[^\n]*", "", tex),
    )
    appendix = False
    chapter = 0
    statement = 0
    expected_numbers = set()
    for token in tokens:
        if token[0] == r"\appendix":
            appendix = True
            chapter = 0
        elif token[0] == r"\chapter{":
            chapter += 1
            statement = 0
        else:
            statement += 1
            prefix = chr(ord("A") + chapter - 1) if appendix else str(chapter)
            expected_numbers.add(f"{prefix}.{statement}")
    counts = Counter(number for _, number in headings)
    require(
        set(counts) == expected_numbers and all(n == 1 for n in counts.values()),
        f"Statement numbers not unique/complete: missing={expected_numbers-set(counts)}, duplicates={[k for k,v in counts.items() if v>1]}",
    )
    log = (ROOT / "output/paper/main.log").read_text(errors="replace")
    require(
        not re.search(
            r"Overfull|undefined|LaTeX Warning:|multiply defined|Missing character:", log
        ),
        "Inspect LaTeX warnings/errors before accepting this PDF",
    )
    require("??" not in text, "Unresolved markers in PDF text")
    print(
        f"PDF: {len(headings)} unique chapter-based statements, 45 assessment links, hierarchy and references OK"
    )
    return {
        "pdf_pages": len(document.findall("page")),
        "statements": len(headings),
        "assessment_links": 45,
        "supplementary_links": 0,
        "underfull_boxes": log.count("Underfull"),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    tex = check_manuscript()
    check_repository()
    source_checks(tex)
    report = {}
    if args.baseline:
        report.update(preservation(tex, args.baseline))
    report.update(pdf_checks(tex))
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2), encoding="utf-8")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, zipfile.BadZipFile, subprocess.SubprocessError) as exc:
        print("FAIL:", exc, file=sys.stderr)
        sys.exit(1)
