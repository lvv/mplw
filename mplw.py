#!/usr/bin/env python

import os, sys
from optparse import *

#from matplotlib.pyplot import barh, title, grid , savefig, yticks, xlabel

from matplotlib.pyplot import *
from numpy  import *

import csv
import string

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

    -v, --verbose
        Verbosely print processing information to stderr.

    -h, --help
        Print this documentation.

    -V, --version
        Print program version number.

SEE ALSO
    matplotlib.com

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
        '''Convert Graphviz notation in file infile to PNG file named outfile.'''

        outfile = os.path.abspath(outfile)
        outdir = os.path.dirname(outfile)

        if not os.path.isdir(outdir):
            raise EApp, 'directory does not exist: %s' % outdir

        basefile = os.path.splitext(outfile)[0]
        saved_cwd = os.getcwd()
        os.chdir(outdir)


        try:
            #########################################################  lvv

            ####  READ PY CODE

            eval_lines=''
            embeded_data = False

            for  line in infile:
                if   line.startswith('___'): 
                    embeded_data = True
                    break
                eval_lines += line


            ####  READ DATA

            if  embeded_data: 
                m = []  # matrix

                #  TODO replace csv with  http://matplotlib.sourceforge.net/api/mlab_api.html#matplotlib.mlab.csv2rec
                # aslo see http://matplotlib.sourceforge.net/api/mlab_api.html
                for row in csv.reader(infile, delimiter=',', quotechar="'", skipinitialspace=True):
                    if row:    # if not blank line
                        m.append(row)  

                    # convert to float if it look like number
                    for i in range(len(m[-1])):
                        if   len(m[-1][i].translate(string.maketrans('',''),' +-0123456789eE.')) == 0:
                            m[-1][i] = float(m[-1][i])

                c = [[row[i] for row in m] for i in range(len(m[0]))]   # transpose

            infile.close()


            ####  EVAL

            exec eval_lines

            lvv_style = True
            if lvv_style:
                auto_adjust(gcf())

                grid(True, color='0.7')
                ### TODO GRIDS
                #rcParams['grid.color'] = 'g'  # does not work
                #grid.color       :   black   # grid color
                #grid.linestyle   :   :       # dotted
                #grid.linewidth   :   0.5     # in points

                savefig(outfile, facecolor='0.95', edgecolor='0.8') # MPL bug? not all borders are drawn
                # TODO axes.linewidth      : 1.0     # edge linewidth
            else:
                savefig(outfile)
            #########################################################

        finally:
            os.chdir(saved_cwd)

    def run(self):
        if self.options.infile == '-':
            sys.stdout.write(' ')       # To suppress asciidoc 'no output from filter' warnings.

            if self.options.outfile is None:
                sys.stderr.write('OUTFILE must be specified')
                sys.exit(1)
            infile = sys.stdin

        else:
            if not os.path.isfile(self.options.infile):
                raise EApp, 'input file does not exist: %s' % self.options.infile
            infile = open(self.options.infile)

        if self.options.outfile is None:
            outfile = os.path.splitext(self.options.infile)[0] + '.png'
        else:
            outfile = self.options.outfile

        self.run_for_real(infile, outfile)


def benchmark(label, val, label_part=-1):
    bar_width = 0.35
    ytick_pos = arange(len(val))+.5
    label.reverse()
    val.reverse()
    # 
    fontsize = rcParams['font.size']
    fixed_part = fontsize/72 * 3  

    h = (len(val)+1.4)*bar_width + fixed_part
    gcf().set_figheight(h)

    #step = ytick_pos[1] - ytick_pos[0]
    #gca().set_ylim(ytick_pos[0]-1, ytick_pos[-1]+1)

    yticks(ytick_pos, label, fontsize='large')
    barh(ytick_pos, val, align="center", height=0.6)
    gca().set_ybound(lower=ytick_pos[0]-0.7, upper=ytick_pos[-1]+0.7)
    gca().set_xbound(upper=max(val)*1.1)
    rcParams['axes.labelsize'] = 'large'

def auto_adjust(fig):
    axes =  getp(fig,property='axes')

    h = getp(fig, property='figheight') # inch
    w = getp(fig, property='figwidth')  # inch
    fontsize = rcParams['font.size']    # point
    dpi = rcParams['savefig.dpi']       # point / inch

    # top,  title
    top_space = 1.7   # em

    #if  len(getp(axes[0],property='title')) != 0:  # if there is a title
    if  getp(axes[0],property='title'):  # if there is a title  # FIXME: always true
        title_fontsize = matplotlib.font_manager.font_scalings[rcParams['axes.titlesize']] * fontsize
        top_adjust = 1.0 - title_fontsize/72 * top_space  /h 
        fig.subplots_adjust(top=top_adjust)

    # bottom,  xlabel
    bottom_space = 1.3  # em

    xtick_fontsize = matplotlib.font_manager.font_scalings[rcParams['xtick.labelsize']] * fontsize
    bottom_adjust = xtick_fontsize/72 /h * bottom_space
    if  len(getp(axes[0],property='xlabel')) != 0:  #  xlabel
        xlabel_fontsize = matplotlib.font_manager.font_scalings[rcParams['axes.labelsize']] * fontsize
        bottom_adjust += xlabel_fontsize/72 /h

    fig.subplots_adjust(bottom=bottom_adjust)

    # left labels
    char_width = 0.8    # em

    current = getp(getp(gca(),property='position'),property='points')
    ll = getp(gca(),property='yticklabels')
    max_ytick_length = max([len(getp(l,property='text')) for l in ll])
    max_ytick_length = max(6, max_ytick_length)
    ytick_fontsize = matplotlib.font_manager.font_scalings[rcParams['ytick.labelsize']] * fontsize
    left_adjust = max_ytick_length * char_width * ytick_fontsize/72 /w
    if  len(getp(axes[0],property='ylabel')) > 0:   # ylable   # FIXME: always true
        ylabel_fontsize = matplotlib.font_manager.font_scalings[rcParams['axes.labelsize']] * fontsize
        left_adjust += ylabel_fontsize/72 /w
    fig.subplots_adjust(left=left_adjust)

    # righ margin
    right_margin = 1.5  # em
    fig.subplots_adjust(right=1-fontsize/72/w * right_margin)


if __name__ == "__main__":
    app = Application()
    app.run()

# vim:ts=4 et sw=4 ft=python:
