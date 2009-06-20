mplw:
	rm -f .t.png
	cat t.mplw  |  mplw.py -o .t.png  - 
	display .t.png

t.html:  t.ad *.py *.conf 
	rm -f .*.png
	asciidoc --unsafe  $<   &&   firefox  $@

test:
	rm -f .t.png
	cat in | chart-filter.py  -o .t.png  - 
	display .t.png

install:
	mkdir -p                     /etc/asciidoc/filters/mpl/
	rm                        -f /etc/asciidoc/filters/chart/chart-filter.{py,conf}
	cp -v chart-filter.{py,conf} /etc/asciidoc/filters/chart/
	chmod   +x                   /etc/asciidoc/filters/chart/chart-filter.py

debug_install:
	mkdir -p                   /etc/asciidoc/filters/mpl/
	rm                      -f /etc/asciidoc/filters/mpl/{mplw.py,mpl.conf}
	ln -sf  -v `pwd`/mplw.py   /etc/asciidoc/filters/mpl/
	ln -sf  -v `pwd`/mpl.conf  /etc/asciidoc/filters/mpl/

clean:
	rm -f .*.png  *.html
