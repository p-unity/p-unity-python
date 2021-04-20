#!/usr/bin/env python3
# -*- encoding: utf-8


__banner__ = r""" ( Copyright Intermine.com.au Pty Ltd. or its affiliates.
                    License SPDX: Programming-Unity-10.42 or as negotiated.

         _   _            ____                _____   _____    _____
        | | (_)          |  _ \      /\      / ____| |_   _|  / ____|
   ___  | |  _           | |_) |    /  \    | (___     | |   | |
  / __| | | | |          |  _ <    / /\ \    \___ \    | |   | |
 | (__  | | | |          | |_) |  / ____ \   ____) |  _| |_  | |____
  \___| |_| |_|          |____/  /_/    \_\ |_____/  |_____|  \_____|
                 ______
                |______|

)





""" # __banner__

class IDE: # { The p-unity IDE: Intergrated Development Environment }

    def __init__(self, **kwargs):

        try:
            from icecream import ic
        except ImportError:  # Graceful fallback if IceCream isn't installed.
            ic = lambda *a: None if not a else (a[0] if len(a) == 1 else a)  # noqa

        builtins = __import__('builtins')
        setattr(builtins, 'ic', ic)

        self.e = BASIC.Engine(run_tests=2, **kwargs)

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

        import rich

        #keyboard.add_hotkey('ctrl+shift+a', print, args=('triggered', 'hotkey'))

        e = self.e

        e.running = -1
        def exit(self, v):
            self.running = v
        e.exit = exit

        e.word("Q", lambda e, t, s: e.exit(f,0))
        e.word("BYE", lambda e, t, s: e.exit(f,0))
        e.word("QUIT", lambda e, t, s: e.exit(f,0))

        e.word("S", lambda e, t, s: e.exit(f,1))
        e.word("STOP", lambda e, t, s: e.exit(f,1))

        v = ["p-unity BASIC v42.01"]
        p, f = t.root.p_count, t.root.f_count
        if p > 0:
            v.append(f"(Tests; {p} Pass, {f} Fail)")

        print("")
        print(" ".join(v))
        print("")

        while e.running == -1:

            print(" > ", end="")
            line = input("")
            line = line.strip()

            e.execute(line)

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

def ide_stdio():

    engine = BASIC.Engine(run_tests=2)

    while True:
        line = ''

        try:
            print('\nReady')

            while not line:
                line = input()

        except KeyboardInterrupt:
            print()
            break

        except EOFError:
            break

        try:
            engine.interpret(line)

        except SyntaxError as exception:
            print(type(exception).__name__ + ':', exception)

        except KeyboardInterrupt:
            if engine.running_program:
                print(f'Break in {interpreter.last_program_lineno}')


import sys

from . import BASIC


