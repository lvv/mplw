
ifeq ($(USER),lvv)
	HOMEDIR := /home/lvv/p/volnitsky.com/
	INCLUDE := $(HOMEDIR)/include.mk 
else
	INCLUDE := /dev/null
endif

include $(INCLUDE)

CLEAN_LIST += *.png

mplw:
	rm -f t.png
	cat t.mplw  |  mplw.py -o t.png  - 
	display t.png

inedex.html: example*.txt force-rebuild

%.png : %.mplw
	cat $< | mplw.py - -o $@

t.html:  t.ad *.py *.conf 
	rm -f .*.png
	asciidoc --unsafe  $<   &&   firefox  $@


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


