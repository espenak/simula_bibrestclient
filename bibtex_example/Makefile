
SOURCE=main

latex:
	latex ${SOURCE}.tex
	bibtex ${SOURCE}.aux
	latex ${SOURCE}.tex
	latex ${SOURCE}.tex

clean:
	rm -f *.aux *.bbl *.toc *.log *.out *.tdo *.blg *.dvi
