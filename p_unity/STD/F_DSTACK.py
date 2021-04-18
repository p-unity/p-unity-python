#!/usr/bin/env python3
# -*- encoding: utf-8


__banner__ = r""" ( Copyright Intermine.com.au Pty Ltd. or its affiliates.
                    License SPDX: Programming-Unity-10.42 or as negotiated.

     _      _____     _____   _______               _____   _  __
  /\| |/\  |  __ \   / ____| |__   __|     /\      / ____| | |/ /
  \ ` ' /  | |  | | | (___      | |       /  \    | |      | ' /
 |_     _| | |  | |  \___ \     | |      / /\ \   | |      |  <
  / , . \  | |__| |  ____) |    | |     / ____ \  | |____  | . \
  \/|_|\/  |_____/  |_____/     |_|    /_/    \_\  \_____| |_|\_\



)





""" # __banner__

class LIB: # { DATA Stack Manipulation : words }

    def __init__(self, f, **kwargs):
        pass

    @staticmethod ### DUP ###
    def word_DUP__R_x_x(f, x):
        "T{ 1 DUP -> 1 1 }T"
        return (x, x)

    @staticmethod ### NIP ###
    def word_NIP__R_n2(f, n1, n2):
        ""
        return (n2,)

    @staticmethod ### ROT ###
    def word_ROT__R_x2_x3_x1(f, x1, x2, x3):
        "T{ 1 2 3 ROT -> 2 3 1 }T"
        return (x2, x3, x1)

    @staticmethod ### DROP ###
    def word_DROP__R(f, x):
        #"T{ 1 2 DROP -> 1 }T T{ 0 DROP -> }T"
        return None

    @staticmethod ### DROP:ALL ###
    def word_DROP_colon_ALL__R(f):
        #"T{ 1 2 DROP:ALL -> }T
        f.stack = []
        return None

    @staticmethod ### OVER ###
    def word_OVER__R_x1_x2_x1(f, x1, x2):
        "T{ 1 2 OVER -> 1 2 1 }T"
        return (x1, x2, x1)

    @staticmethod ### SWAP ###
    def word_SWAP__R_x2_x1(f, x1, x2):
        "T{ 1 2 SWAP -> 2 1 }T"
        return (x2, x1)

    @staticmethod ### TUCK ###
    def word_TUCK(f, n1, n2):
        ""
        return (n2, n1, n2)


