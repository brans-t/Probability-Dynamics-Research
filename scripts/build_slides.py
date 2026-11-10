"""Compile Beamer slides, publishing only the PDF to output/slides."""

import argparse
from pathlib import Path
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'slides/project9_exercises1_2.tex'
OUTPUT = ROOT / 'output/slides'
BUILD = ROOT / 'build/slides'


def publish_pdf():
    pdf = BUILD / SOURCE.with_suffix('.pdf').name
    if not pdf.is_file():
        raise SystemExit(f'Compiled slide PDF not found: {pdf}')
    OUTPUT.mkdir(parents=True, exist_ok=True)
    destination = OUTPUT / pdf.name
    shutil.copy2(pdf, destination)
    print(f'Compiled {destination}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--publish-only', action='store_true',
        help='Copy the compiled PDF from build/slides (used by LaTeX Workshop).',
    )
    args = parser.parse_args()
    if args.publish_only:
        publish_pdf()
        return
    if shutil.which('xelatex') is None:
        raise SystemExit('XeLaTeX not found. Install TeX Live or MiKTeX.')
    BUILD.mkdir(parents=True, exist_ok=True)
    command = [
        'xelatex', '-interaction=nonstopmode', '-halt-on-error',
        '-file-line-error', f'-output-directory={BUILD}', str(SOURCE),
    ]
    for _ in range(2):
        subprocess.run(command, cwd=ROOT, check=True)
    publish_pdf()


if __name__ == '__main__':
    main()
