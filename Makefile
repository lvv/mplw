mplw:
	rm -f .t.png
	cat in.mplw | mplw.py  -o .t.png  - 
	display .t.png

t.html:  t.ad *.py *.conf t.ad in 
	rm -f .*.png
	asciidoc --unsafe --attribute icons --attribute iconsdir=/images/icons $< && firefox  $@

test:
	rm -f .t.png
	cat in | chart-filter.py  -o .t.png  - 
	display .t.png

install:
	rm                        -f /etc/asciidoc/filters/chart/chart-filter.{py,conf}
	cp -v chart-filter.{py,conf} /etc/asciidoc/filters/chart/
	chmod   +x                   /etc/asciidoc/filters/chart/chart-filter.py

debug_install:
	rm                        -f /etc/asciidoc/filters/chart/chart-filter.{py,conf}
	ln -sf  -v `pwd`/chart-filter.py   /etc/asciidoc/filters/chart/
	ln -sf  -v `pwd`/chart-filter.conf /etc/asciidoc/filters/chart/

clean:
	rm -f .*.png  *.html
