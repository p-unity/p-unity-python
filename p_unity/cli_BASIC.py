#!/usr/bin/env python3
# -*- encoding: utf-8
# SPDX-License-Identifier: MIT
# Copyright (c) 2021 - 2021, Scott.McCallum@HQ.UrbaneINTER.NET

__banner__ = r""" (

         _   _            ____                _____   _____    _____
        | | (_)          |  _ \      /\      / ____| |_   _|  / ____|
   ___  | |  _           | |_) |    /  \    | (___     | |   | |
  / __| | | | |          |  _ <    / /\ \    \___ \    | |   | |
 | (__  | | | |          | |_) |  / ____ \   ____) |  _| |_  | |____
  \___| |_| |_|          |____/  /_/    \_\ |_____/  |_____|  \_____|
                 ______
                |______|

)







"""  # __banner__

class IDE: # { The p-unity IDE: Intergrated Development Environment }

    def __init__(self, **kwargs):

        try:
            from icecream import ic
        except ImportError:  # Graceful fallback if IceCream isn't installed.
            ic = lambda *a: None if not a else (a[0] if len(a) == 1 else a)  # noqa

        builtins = __import__('builtins')
        setattr(builtins, 'ic', ic)

        self.engine = BASIC.Engine(run_tests=2, **kwargs)

    def run_stdio(self, run=None, debug=False):

        if run:
            for line in run.split('\n'):
                self.engine.interpret(line)

            self.engine.interpret("RUN")

            if not debug: return

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
                self.engine.interpret(line)

            except SyntaxError as exception:
                print(type(exception).__name__ + ':', exception)

            except KeyboardInterrupt:
                if engine.running_program:
                    print(f'Break in {interpreter.last_program_lineno}')

def ide_stdio(run=None,debug=True):
    ide = IDE()
    ide.run_stdio(run=run,debug=debug)

import sys

from . import BASIC


