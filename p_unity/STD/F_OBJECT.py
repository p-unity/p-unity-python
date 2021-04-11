#!/usr/bin/env python3
# -*- encoding: utf-8


__banner__ = """ ( Copyright Intermine.com.au Pty Ltd. or its affiliates.
                   SPDX-License-Identifier: Programming-Unity-10.42

     _       ____    ____         _   ______    _____   _______
  /\| |/\   / __ \  |  _ \       | | |  ____|  / ____| |__   __|
  \ ` ' /  | |  | | | |_) |      | | | |__    | |         | |
 |_     _| | |  | | |  _ <   _   | | |  __|   | |         | |
  / , . \  | |__| | | |_) | | |__| | | |____  | |____     | |
  \/|_|\/   \____/  |____/   \____/  |______|  \_____|    |_|



)





""" # __banner__

class LIB: # { The Object ABI : words }

    def __init__(self, **kwargs):
        pass

    @staticmethod ### LEN ###
    def word_LEN__R_x_n(f, x):
        "T{ 'Hello'World' LEN -> 'Hello'World' 11 }T"
        return (x, len(x),)

    @staticmethod ### ~ ###
    def word_tilde__R_x_b(f, x):
        return (x, not x,)

    @staticmethod ### [[ ###
    def word_lbracket_lbracket(f):
        f.__brace2 = len(f.stack)
        f.__colon2 = -1

    @staticmethod ### :: ###
    def word_colon_colon(f):
        f.__colon2 = len(f.stack)

    @staticmethod ### ]] ###
    def word_rbracket_rbracket__R_x(f):
        object = f.stack[s.__brace2-1]
        depth = len(f.stack)
        if f.__colon2 == -1:
            if f.__brace2 == depth:
                raise ForthException("[: error(-2): [[ ]] illegal")
            else:
                index = f.stack[s.__brace2]
                f.stack = f.stack[:s.__brace2]
                f.stack.append(object[index])
            return


