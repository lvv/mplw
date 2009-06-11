test:
	rm -f t.png
	cat in | cvs2barchart.py  -o t.png  - 
	display t.png

install:
	rm                        -f /etc/asciidoc/filters/chart/chart-filter.{py,conf}
	cp -v chart-filter.{py,conf} /etc/asciidoc/filters/chart/
	chmod   +x                   /etc/asciidoc/filters/chart/chart-filter.py

inst:
	rm                        -f /etc/asciidoc/filters/chart/chart-filter.{py,conf}
	ln -sf  -v `pwd`/chart-filter.py   /etc/asciidoc/filters/chart/
	ln -sf  -v `pwd`/chart-filter.conf /etc/asciidoc/filters/chart/
