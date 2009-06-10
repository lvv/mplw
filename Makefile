test:
	rm -f t.png
	cat in | cvs2barchart.py  -o t.png  - 
	display t.png

install:
	rm                        -f /etc/asciidoc/filters/chart/chart-filter.{py,conf}
	cp -v chart-filter.{py,conf} /etc/asciidoc/filters/chart/
	chmod   +x                   /etc/asciidoc/filters/chart/chart-filter.py
