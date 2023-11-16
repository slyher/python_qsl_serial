#!/bin/bash
cd dist/$( echo $1 | tr -d "\r")
pdflatex -interaction=nonstopmode  qsl_r.tex
pdflatex -interaction=nonstopmode qsl.tex
