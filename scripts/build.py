"""Build the manuscript and copy its PDF to output/paper."""

import argparse
import os
from pathlib import Path
import shutil
import subprocess

PAPER = Path(__file__).resolve().parents[1] / "paper"
BUILD = PAPER.parent / "build/paper"
OUTPUT = PAPER.parent / "output/paper"


def publish_pdf() -> None:
    pdf = BUILD / "main.pdf"
    if not pdf.is_file():
        raise SystemExit(f"Compiled manuscript PDF not found: {pdf}")
    OUTPUT.mkdir(parents=True, exist_ok=True)
    destination = OUTPUT / pdf.name
    shutil.copy2(pdf, destination)
    print(f"Copied {destination}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--publish-only", action="store_true",
        help="Copy the compiled PDF from build/paper (used by LaTeX Workshop).",
    )
    args = parser.parse_args()
    if args.publish_only:
        publish_pdf()
        return
    for tool in ("xelatex", "biber"):
        if shutil.which(tool) is None:
            raise SystemExit(f"Required tool not found: {tool}. Install TeX Live or MiKTeX.")
    BUILD.mkdir(parents=True, exist_ok=True)
    tex = [
        "xelatex",
        f"-output-directory={BUILD}",
        "-synctex=1",
        "-interaction=nonstopmode",
        "-halt-on-error",
        "-file-line-error",
        "main.tex",
    ]
    subprocess.run(tex, cwd=PAPER, check=True)
    # Biber/Perl can inherit an unsupported desktop locale. Scope this override
    # to the child process so the shell and subsequent TeX calls are unaffected.
    environment = dict(os.environ, LC_ALL="C")
    subprocess.run(
        ["biber", f"--input-directory={BUILD}", f"--output-directory={BUILD}", "main"],
        cwd=PAPER,
        env=environment,
        check=True,
    )
    for _ in range(2):
        subprocess.run(tex, cwd=PAPER, check=True)
    print(f"Compiled {BUILD / 'main.pdf'}")
    publish_pdf()


if __name__ == "__main__":
    main()
