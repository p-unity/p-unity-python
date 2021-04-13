#!/usr/bin/env python3
# -*- encoding: utf-8


__banner__ = """ ( Copyright Intermine.com.au Pty Ltd. or its affiliates.
                   SPDX-License-Identifier: Programming-Unity-10.42

     _      __  __              _______   _    _
  /\| |/\  |  \/  |     /\     |__   __| | |  | |
  \ ` ' /  | \  / |    /  \       | |    | |__| |
 |_     _| | |\/| |   / /\ \      | |    |  __  |
  / , . \  | |  | |  / ____ \     | |    | |  | |
  \/|_|\/  |_|  |_| /_/    \_\    |_|    |_|  |_|



)





""" # __banner__

class LIB: # { Mathematical : words }

    """

    T{ 1+0j 2+1j + -> 3+1j }T

    """

    def __init__(self, **kwargs):
        pass

    @staticmethod ### + ###
    def word_plus__R_x3(f, x1, x2):
        """
        T{ 0.1 0.2 + -> 0.3 }T ( Simple it seems, yet complex it is )
        T{ 1.4j 2.2j + -> 3.6j }T
        T{ 'Hello ''World + -> (("Hello World")) }T
        """
        if isinstance(x1, int) or isinstance(x1, Decimal):
            return (x1 + x2,)

        if isinstance(x1, complex):
            return (x1 + x2,)

        if isinstance(x1, list):
            return (x1 + [x2],)

        return (x1 + x2,)


    @staticmethod ### - ###
    def word_minus__R_x3(f, x1, x2):
        "T{ 1+0j 2+0j - -> -1+0j }T"
        if isinstance(x1, int) or isinstance(x1, Decimal):
            return (x1 - x2,)

        if isinstance(x1, complex):
            return (x1 - x2,)

        if isinstance(x1, list):
            """
            T{ ([1,2,3]) 2 - -> ([1,3]) }T"
            """
            return (list(filter((x2).__ne__, x1)),)

        if isinstance(x1, dict):
            del x1[x2]
            return (x1,)

        return (n1 - n2,)

    @staticmethod ### * ###
    def word_times__R_n3(f, n1, n2):
        ""
        return (n1 * n2,)

    @staticmethod ### ** ###
    def word_times_times__R_n3(f, n1, n2):
        ""
        return (n1 ** n2,)

    @staticmethod ### SQRT ###
    def word_SQRT__R_n2(f, n1):
        ""
        return (math.sqrt(n1),)

    @staticmethod ### / ###
    def word_divide__R_n3(f, n1, n2):
        ""
        return (n1 / n2,)

    @staticmethod ### /MOD ###
    def word_divide_MOD__R_n3_n4(f, n1, n2):
        ""
        return divmod(x, n2)[::-1]

    @staticmethod ### MOD ###
    def word_MOD__R_n3(f, n1, n2):
        ""
        return (n1 % n2,)

    @staticmethod ### ABS ###
    def word_ABS__R_n2(f, n1):
        """
        T{ -2.3 ABS -> 2.3 }T T{ 5.55 ABS -> 5.55 }T
        T{ 0 ABS -> 0 }T T{ 1 ABS -> 1 }T T{ -1 ABS -> 1 }T
        """
        return (abs(n1),)

    @staticmethod ### INVERT ###
    def word_INVERT__R_n2(f, n1):
        ""
        return (~n1,)

    @staticmethod ### NAN ###
    def word_NAN__R_n(f):
        ""
        return (Decimal("Nan"),)

    @staticmethod ### INFINITY ###
    def word_INFINITY__R_n(f):
        ""
        return (Decimal("Infinity"),)

    @staticmethod ### -INFINITY ###
    def word_minus_INFINITY__R_n(f):
        ""
        return (Decimal("-Infinity"),)

import math

from decimal import Decimal

