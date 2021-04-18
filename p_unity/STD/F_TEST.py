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

    def __init__(self, f, **kwargs):
        self.p_count = 0
        self.f_count = 0

    @staticmethod ### T{ ###
    def word_T_lbrace(f):
        f.__test_bang = False
        f.__test = f.stack
        f.stack = copy.deepcopy(f.__test)

    @staticmethod ### T{! ###
    def word_T_lbrace_bang(f):
        f.__test_bang = True
        f.__test = f.stack
        f.stack = copy.deepcopy(f.__test)

    @staticmethod ### -> ###
    def word_minus_rangle(f):
        f.__test_need = f.stack[len(f.__test):]
        f.stack = copy.deepcopy(f.__test)

    @staticmethod ### }T ###
    def word_rbrace_T(f):
        have = f.stack[len(f.__test):]
        need = f.__test_need
        ic(have, need)
        if have == need:
            f.TEST.p_count += 1
        else:
            f.TEST.f_count += 1
            need = repr(need)
            have = repr(have)
            print(f"INCORRECT RESULT: {need} ~= {have}")
        f.stack = f.__test


import copy

