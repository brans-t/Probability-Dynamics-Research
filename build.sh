#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/paper"
mkdir -p Tmp
xelatex -output-directory=Tmp -synctex=1 -interaction=nonstopmode -halt-on-error -file-line-error main.tex
LC_ALL=C biber --input-directory=Tmp --output-directory=Tmp main
xelatex -output-directory=Tmp -synctex=1 -interaction=nonstopmode -halt-on-error -file-line-error main.tex
xelatex -output-directory=Tmp -synctex=1 -interaction=nonstopmode -halt-on-error -file-line-error main.tex
printf '\nCompiled %s/Tmp/main.pdf\n' "$PWD"
