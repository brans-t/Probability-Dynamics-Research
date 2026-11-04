"""Build the manuscript with XeLaTeX and Biber on Windows, macOS, or Linux."""

import os
from pathlib import Path
import shutil
import subprocess

PAPER = Path(__file__).resolve().parents[1] / "paper"


def main() -> None:
    for tool in ("xelatex", "biber"):
        if shutil.which(tool) is None:
            raise SystemExit(f"Required tool not found: {tool}. Install TeX Live or MiKTeX.")
    (PAPER / "Tmp").mkdir(exist_ok=True)
    tex = [
        "xelatex",
        "-output-directory=Tmp",
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
        ["biber", "--input-directory=Tmp", "--output-directory=Tmp", "main"],
        cwd=PAPER,
        env=environment,
        check=True,
    )
    for _ in range(2):
        subprocess.run(tex, cwd=PAPER, check=True)
    print(f"Compiled {PAPER / 'Tmp/main.pdf'}")


if __name__ == "__main__":
    main()
