"""Compile the Project 9.1 Beamer slides with XeLaTeX (no Biber required)."""

from pathlib import Path
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'slides/project9_exercise1.tex'
OUTPUT = ROOT / 'output/slides'


def main():
    if shutil.which('xelatex') is None:
        raise SystemExit('XeLaTeX not found. Install TeX Live or MiKTeX.')
    OUTPUT.mkdir(parents=True, exist_ok=True)
    command = [
        'xelatex', '-interaction=nonstopmode', '-halt-on-error',
        '-file-line-error', '-synctex=1', f'-output-directory={OUTPUT}', str(SOURCE),
    ]
    for _ in range(2):
        subprocess.run(command, cwd=ROOT, check=True)
    print(f"Compiled {OUTPUT / 'project9_exercise1.pdf'}")


if __name__ == '__main__':
    main()
