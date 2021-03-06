#!/usr/bin/env python

import os, sys
from optparse import *

#from matplotlib.pyplot import barh, title, grid , savefig, yticks, xlabel
from matplotlib.pyplot import *
import numpy as np

__AUTHOR__ = "Gouichi Iisaka <iisaka51@gmail.com>"
__VERSION__ = '1.1.3'

class EApp(Exception):
    '''Application specific exception.'''
    pass

class Application():
    '''
NAME
    graphviz2png - Converts textual graphviz notation to PNG file

SYNOPSIS
    graphviz2png [options] INFILE

DESCRIPTION
    This filter reads Graphviz notation text from the input file
    INFILE (or stdin if INFILE is -), converts it to a PNG image file.


OPTIONS
    -o OUTFILE, --outfile=OUTFILE
        The file name of the output file. If not specified the output file is
        named like INFILE but with a .png file name extension.

    -L LAYOUT, --layout=LAYOUT
        Graphviz layout: dot, neato, twopi, circo, fdp
        Default is 'dot'.

    -v, --verbose
        Verbosely print processing information to stderr.

    -h, --help
        Print this documentation.

    -V, --version
        Print program version number.

SEE ALSO
    graphviz(1)

AUTHOR
    Written by Gouichi Iisaka, <iisaka51@gmail.com>

THANKS
    Stuart Rackham, <srackham@gmail.com>
    This script was inspired by his music2png.py and AsciiDoc

LICENSE
    Copyright (C) 2008-2009 Gouichi Iisaka.
    Free use of this software is granted under the terms of
    the GNU General Public License (GPL).
    '''

    def __init__(self, argv=None):
        if not argv:
            argv = sys.argv

        self.usage = '%prog [options] inputfile'
        self.version = 'Version: %s\n' % __VERSION__
        self.version += 'Copyright(c) 2008-2009: %s\n' % __AUTHOR__

        self.option_list = [
            Option("-o", "--outfile", action="store",
		    dest="outfile",
		    help="Output file"),
            Option("-L", "--layout", action="store",
                    dest="layout", default="dot", type="choice",
                    choices=['dot','neato','twopi','circo','fdp'],
		    help="Layout type. LAYOUT=<dot|neato|twopi|circo|fdp>"),
            Option("--debug", action="store_true",
		    dest="do_debug",
		    help=SUPPRESS_HELP),
            Option("-v", "--verbose", action="store_true",
		    dest="do_verbose", default=False,
		    help="verbose output"),
	    ]

        self.parser = OptionParser( usage=self.usage, version=self.version,
                                    option_list=self.option_list)
        (self.options, self.args) = self.parser.parse_args()

	if len(self.args) != 1:
            self.parser.print_help()
            sys.exit(1)

        self.options.infile = self.args[0]

    def systemcmd(self, cmd):
        if self.options.do_verbose:
            msg = 'Execute: %s' % cmd
            sys.stderr.write(msg + os.linesep)
        else:
            cmd += ' 2>/dev/null'
        if os.system(cmd):
            raise EApp, 'failed command: %s' % cmd

    def run_for_real(self, infile, outfile):
        '''Convert Graphviz notation in file infile to
           PNG file named outfile.'''

        outfile = os.path.abspath(outfile)
        outdir = os.path.dirname(outfile)

        if not os.path.isdir(outdir):
            raise EApp, 'directory does not exist: %s' % outdir

        basefile = os.path.splitext(outfile)[0]
        saved_cwd = os.getcwd()
        os.chdir(outdir)
        try:
		#cmd = '%s -Tpng "%s" > "%s"' % (self.options.layout, infile, outfile)
		#self.systemcmd(cmd)



		#########################################################
		# 'figure.edgecolor'

		in_file = open(infile, "r")
		in_val = []
		in_label = []

		# header
		in_title = in_file.readline()
		in_title.strip()
		while True:
			in_line = in_file.readline()
			if not in_line: 
				print "chart-filter error: premature EOF"
				exit
			in_line.strip()
			if  len(in_line) == 1 :  break
			sp_pos =  in_line.index(' ')
			option = in_line[0:sp_pos]
			if  option == 'xlabel' :  
				xlabel(in_line[sp_pos+1:])
			#else :
			#	print 'chart-filter error:  unrecognised line:  ' +  in_line

			#             if self.left>=self.right:
			#                reset()
			#                raise ValueError('left cannot be >= right')



		# read data
		for in_line in in_file:
			in_line.strip()
			if  len(in_line) == 1 :  break
			in_line = in_line[:-1]
			sp_pos =  in_line.index(' ')
			in_val.append(int(in_line[0:sp_pos]))
			in_label.append(in_line[sp_pos+1:].strip())	

		in_file.close()

		pos = np.arange(len(in_val))+.5  
		in_label.reverse()
		in_val.reverse()
		fig_hight = 4.8 + len(in_val)*0.3

		rcParams['figure.figsize'] = (11, 11)
		fig = figure()
		#fig = figure(figsize=(5,fig_hight))  # default 8, 6

		## l, b, w, h
		rect = 0.3, 0.17, 0.6, 0.5  # default position: 0.125,  0.1,    0.9  ,  0.9
		ax = fig.add_subplot(111, position=rect) 

		yticks(pos, tuple(in_label))
		rcParams['figure.edgecolor'] = 'g'
		barh(pos,in_val, align='center')
			#ax.barh(pos,in_val, align='center')
		ax.grid(True)
			#w = 5
			#h = 1
			#set_figsize_inches( (w,h) )
		ax.set_title(in_title)
		fig.savefig(outfile)
		#########################################################
        finally:
            os.chdir(saved_cwd)

        if not self.options.do_debug:
            os.unlink(infile)

    def run(self):
        if self.options.infile == '-':
            if self.options.outfile is None:
                sys.stderr.write('OUTFILE must be specified')
                sys.exit(1)
            infile = os.path.splitext(self.options.outfile)[0] + '.txt'
            lines = sys.stdin.readlines()
            open(infile, 'w').writelines(lines)

        if not os.path.isfile(infile):
            raise EApp, 'input file does not exist: %s' % infile

        if self.options.outfile is None:
            outfile = os.path.splitext(infile)[0] + '.png'
        else:
            outfile = self.options.outfile

        self.run_for_real(infile, outfile)

        # To suppress asciidoc 'no output from filter' warnings.
        if self.options.infile == '-':
            sys.stdout.write(' ')

if __name__ == "__main__":
    app = Application()
    app.run()
