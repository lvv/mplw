
ASCIIDOC_FILTERS ?= /usr/share/asciidoc/filters


ifeq ($(USER),lvv)
	HOMEDIR := /home/lvv/p/volnitsky.com/
	INCLUDE := $(HOMEDIR)/include.mk 
else
	INCLUDE := /dev/null
endif


include $(INCLUDE)

CLEAN_LIST += $(wildcard *.png)
COPY_LIST += $(wildcard *.png)


mplw:
	rm -f t.png
	cat t.mplw  |  mplw.py -o t.png  - 
	display t.png


%.png : %.mplw
	cat $< | mplw.py - -o $@

#index.html: example-data.png example-sin.png
#index.html: 

localweb: example-data.png example-sin.png

t.html:  t.ad *.py *.conf 
	rm -f .*.png
	asciidoc --unsafe  $<   &&   firefox  $@



install:
	[[  -d "$(ASCIIDOC_FILTERS)" ]]  ||  { echo "*** asciidoc's filters directory not found ***";  exit 33; }
	mkdir -p		$(ASCIIDOC_FILTERS)/mpl/
	rm                   -f $(ASCIIDOC_FILTERS)/mpl/{mplw.py,mpl.conf}
	cp -v   mplw.py   	$(ASCIIDOC_FILTERS)/mpl/
	cp -v   mpl.conf	$(ASCIIDOC_FILTERS)/mpl/
	chmod  +x              	$(ASCIIDOC_FILTERS)/mpl/mplw.py

debug_install:
	mkdir -p                   $(ASCIIDOC_FILTERS)/mpl/
	rm                      -f $(ASCIIDOC_FILTERS)/mpl/{mplw.py,mpl.conf}
	ln -sf  -v `pwd`/mplw.py   $(ASCIIDOC_FILTERS)/mpl/
	ln -sf  -v `pwd`/mpl.conf  $(ASCIIDOC_FILTERS)/mpl/


