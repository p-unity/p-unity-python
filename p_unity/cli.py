#!/usr/bin/env python3
# -*- encoding: utf-8


__banner__ = """ ( Copyright Intermine.com.au Pty Ltd. or its affiliates.
                   SPDX-License-Identifier: Programming-Unity-10.42

         _   _
        | | (_)
   ___  | |  _       _ __    _   _
  / __| | | | |     | '_ \  | | | |
 | (__  | | | |  _  | |_) | | |_| |
  \___| |_| |_| (_) | .__/   \__, |
                    | |       __/ |
                    |_|      |___/

)





""" # __banner__

class IDE: # { The p-unity IDE: Intergrated Development Environment }

    def __init__(self, **kwargs):

        self.e = FORTH.Engine(**kwargs)

        self.c = None
        if 'stdscr' in kwargs:
            self.c = kwargs['stdscr']


    def run_curses(self):

        from curses import wrapper

        #win1 = scr.new_win(orig=(0, 0), size=(80, 20))
        #win2 = scr.new_win(orig=(0, 20), size=(80, 4))
        #win3 = scr.new_win(orig=(0, 24), size=(80, 1))
        dir(self.c)
        win3 = self.c.newwin(0, 0, 80, 1)
        #win1.border()
        #win2.border()
        #win1.background('+', color='red')
        #win2.background('.', color=('green', 'blue'))
        win3.background(' ', color=('green', 'red'))
        #win1.refresh()
        #win2.refresh()
        win3.refresh()
        s = win3.getstr((0, 0), echo=True)
        #win2.write(s, (1, 1), color=('red', 'black'))
        #win2.refresh()
        #win1.write('Press q to quit', (1, 1), color=('black', 'red'))
        #while win1.getkey() != 'q':
        #    pass


    def run_stdio(self):

        from icecream import ic, install
        install()

        e = self.e

        e.running = -1
        def exit(self, v):
            self.running = v
        e.exit = exit

        e.word("Q", lambda f: f.exit(f,0))
        e.word("BYE", lambda f: f.exit(f,0))
        e.word("QUIT", lambda f: f.exit(f,0))

        e.word("S", lambda f: f.exit(f,1))
        e.word("STOP", lambda f: f.exit(f,1))

        print("")
        p, f = e.TEST.p_count, e.TEST.f_count
        print(f"p-unity FORTH v42.01 (Sanity Tests; {p} Pass, {f} Fail)")
        print("")

        while e.running == -1:

            print(" > ", end="")
            line = input("")
            line = line.strip()

            #try:
            e.execute(line.split(), rollback=True)
            #except Exception as ex:
            #    details = str(ic(ex))
            #    rich.print(f"[bold red]{details}[/]")

            print("=> ", end="")
            for object in e.stack:
                object = repr(object)
                print(f"{object}", end=" ")

            print("")

        print("")
        sys.exit(e.running)


def __ide_curses(stdscr):
    ide = IDE(stdscr=stdscr)
    ide.run_curses()
    del ide

def ide_curses():
    wrapper(__ide_curses)

def ide_stdio():
    ide = IDE()
    ide.run_stdio()
    del ide

import sys

from . import FORTH


