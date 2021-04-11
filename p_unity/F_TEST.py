#!/usr/bin/env python3
# -*- encoding: utf-8


__banner__ = """ ( Copyright Intermine.com.au Pty Ltd. or its affiliates.
                   SPDX-License-Identifier: Programming-Unity-10.42

     _      _______ __       __      _________
  /\| |/\  |__   __/ /       \ \    |__   __\ \
  \ ` ' /     | | | |    _____\ \      | |   | |
 |_     _|    | |/ /    |______> >     | |    \ \
  / , . \     | |\ \          / /      | |    / /
  \/|_|\/     |_| | |        /_/       |_|   | |
                   \_\                      /_/


)





""" # __banner__

class P_UNITY: # { TEST : words }

    def __init__(self):
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
        #ic(f.__test, have, need)
        if have == need:
            f.TEST.p_count += 1
        else:
            f.TEST.f_count += 1
            print(f"INCORRECT RESULT: {need} ~= {have}")
        f.stack = f.__test


import copy

