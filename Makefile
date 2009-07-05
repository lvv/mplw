
HOMEDIR ?= /home/lvv/p/volnitsky.com/
include $(HOMEDIR)/include.mk

t.html:  t.ad *.py *.conf 
	rm -f .*.png
	asciidoc --unsafe  $<   &&   firefox  $@

mplw:
	rm -f .t.png
	cat t.mplw  |  mplw.py -o .t.png  - 
	display .t.png



install:
	mkdir -p		/etc/asciidoc/filters/mpl/
	rm                   -f /etc/asciidoc/filters/mpl/{mplw.py,mpl.conf}
	cp -v   mplw.py   	/etc/asciidoc/filters/mpl/
	cp -v   mpl.conf	/etc/asciidoc/filters/mpl/
	chmod  +x              	/etc/asciidoc/filters/mpl/mplw.py

debug_install:
	mkdir -p                   /etc/asciidoc/filters/mpl/
	rm                      -f /etc/asciidoc/filters/mpl/{mplw.py,mpl.conf}
	ln -sf  -v `pwd`/mplw.py   /etc/asciidoc/filters/mpl/
	ln -sf  -v `pwd`/mpl.conf  /etc/asciidoc/filters/mpl/

