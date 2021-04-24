#!/usr/bin/env python3
# -*- encoding: utf-8


__banner__ = r""" ( Copyright Intermine.com.au Pty Ltd. or its affiliates.
                    License SPDX: Programming-Unity-10.42 or as negotiated.

     _                  _____    _____   _____   _____
  /\| |/\      /\      / ____|  / ____| |_   _| |_   _|
  \ ` ' /     /  \    | (___   | |        | |     | |
 |_     _|   / /\ \    \___ \  | |        | |     | |
  / , . \   / ____ \   ____) | | |____   _| |_   _| |_
  \/|_|\/  /_/    \_\ |_____/   \_____| |_____| |_____|



)





""" # __banner__

class LIB: # { ASCII Fonts : words }

    """

    T{ 'Hello'World -> 'Hello'World }T
    T{ 'Goodbye ''World + -> 'Goodbye ''World + }T

    """


    def __init__(self, e, **kwargs):
        pass

    @staticmethod ### . ###
    def word_FIGLET__R_s2(e, t, c, s1):
        from pyfiglet import Figlet
        f = Figlet(font='big')

        lines = []
        for line in f.renderText(s1).split('\n'):
            lines.append(" " + line)

        s2 = "\n".join(lines)

        print(f"{s2}")

