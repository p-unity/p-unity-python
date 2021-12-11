#!/usr/bin/env python3
# -*- encoding: utf-8
# SPDX-License-Identifier: MIT
# Copyright (c) 2021 - 2021, Scott.McCallum@HQ.UrbaneINTER.NET

__banner__ = r""" (

         _   _            ______    ____    _____    _______    _    _
        | | (_)          |  ____|  / __ \  |  __ \  |__   __|  | |  | |
   ___  | |  _           | |__    | |  | | | |__) |    | |     | |__| |
  / __| | | | |          |  __|   | |  | | |  _  /     | |     |  __  |
 | (__  | | | |          | |      | |__| | | | \ \     | |     | |  | |
  \___| |_| |_|          |_|       \____/  |_|  \_\    |_|     |_|  |_|
                 ______
                |______|

)







"""  # __banner__

__version__ = "1.1.20210725000000"

class IDE:  # { The p-unity IDE: Intergrated Development Environment }
    def __init__(self, run=None, **kwargs):

        try:
            from icecream import ic
        except ImportError:  # Graceful fallback if IceCream isn't installed.
            ic = lambda *a: None if not a else (a[0] if len(a) == 1 else a)  # noqa

        builtins = __import__("builtins")
        setattr(builtins, "ic", ic)

        self.e = UNITY.Engine(run, **kwargs)

    def run_stdio(self, run=None, debug=False):

        e = self.e

        e.running = -1

        if run:
            e.execute(run)
            return

        v = ["cubed4th " + __version__]
        p, f = e.root.test["p"], e.root.test["f"]
        if p > 0:
            v.append(f"(Sanity Tests; {p} Pass, {f} Fail)")

        if __run__:
            print(__run__.strip())
            e.execute(__run__)

        print("")
        print(" ".join(v))
        print("")

        while e.running == -1:

            print(" > ", end="")
            line = input("")
            line = line.strip()

            e.execute(line)

            print("=>", end="")
            for object in e.root.stack:
                object = repr(object)
                print(f" {object}", end="")

            print()

        print()
        sys.exit(e.running)


def __ide_curses(stdscr):
    ide = IDE(stdscr=stdscr)
    ide.run_curses()
    del ide


def ide_curses():
    wrapper(__ide_curses)


def ide_stdio(run=None,debug=False):
    ide = IDE()
    ide.run_stdio(run=run, debug=debug)
    del ide


import sys

from . import UNITY

__run__ = """

T{ : GD2 DO I -1 +LOOP ; -> }T
T{ 1 4 GD2 -> 4 3 2 1 }T
T{ -1 2 GD2 -> 2 1 0 -1 }T

"""

__run__ = None
