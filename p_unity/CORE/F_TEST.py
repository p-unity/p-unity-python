#!/usr/bin/env python3
# -*- encoding: utf-8


__banner__ = r""" ( Copyright Intermine.com.au Pty Ltd. or its affiliates.
                    License SPDX: Programming-Unity-10.42 or as negotiated.

     _      _______ __       __      _________
  /\| |/\  |__   __/ /       \ \    |__   __\ \
  \ ` ' /     | | | |    _____\ \      | |   | |
 |_     _|    | |/ /    |______> >     | |    \ \
  / , . \     | |\ \          / /      | |    / /
  \/|_|\/     |_| | |        /_/       |_|   | |
                   \_\                      /_/


)





""" # __banner__

class LIB: # { Testing, TESTING, 123 : words }

    def __init__(self, e, **kwargs):
        self.p_count = 0
        self.f_count = 0

    @staticmethod ### T{ ###
    def word_T_lbrace(e, t, c):
        stack = copy.deepcopy(t.stack)
        c.stack.append({"m":"TEST", "STACK":t.stack})
        t.stack = stack

    @staticmethod ### T{! ###
    def word_T_lbrace_bang(e, t, c):
        stack = copy.deepcopy(t.stack)
        c.stack.append({"m":"TEST!", "STACK":t.stack})
        t.stack = stack

    @staticmethod ### -> ###
    def word_minus_rangle(e, t, c):
        block = c.stack[-1]
        block["HAVE"] = t.stack[len(block["STACK"]):]
        t.stack = copy.deepcopy(block["STACK"])

    @staticmethod ### }T ###
    def word_rbrace_T(e, t, c):
        block = c.stack.pop()
        block["NEED"] = t.stack[len(block["STACK"]):]
        if block["HAVE"] == block["NEED"]:
            e.TEST.p_count += 1
        else:
            e.TEST.f_count += 1
            have = repr(block["HAVE"])
            need = repr(block["NEED"])
            print(f"INCORRECT RESULT: {have} ~= {need}")

        t.stack = block["STACK"]

import copy

