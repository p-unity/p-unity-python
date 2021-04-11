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

class LIB: # { Mathamitcal : words }

    """

    T{ 0.1 0.2 + -> 0.3 }T # WOO HOO!
    T{ 1.1 2.2 + -> 3.3 }T # WOO HOO!

    T{ 1+0j 2+0j + -> 3+0j }T
    T{ 1+0j 2+1j + -> 3+1j }T

    """

    def __init__(self, **kwargs):
        pass

    @staticmethod ### + ###
    def word_plus__R_n3(f, n1, n2):
        ""
        return (n1 + n2,)

    @staticmethod ### - ###
    def word_minus__R_n3(f, n1, n2):
        ""
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

    @staticmethod ### INVERT ###
    def word_INVERT__R_n2(f, n1):
        ""
        return (~n1,)

    @staticmethod ### NAN ###
    def word_NAN(f):
        ""
        return (Decimal("Nan"),)

    @staticmethod ### INFINITY ###
    def word_INFINITY(f):
        ""
        return (Decimal("Infinity"),)

    @staticmethod ### -INFINITY ###
    def word_minus_INFINITY(f):
        ""
        return (Decimal("-Infinity"),)

import math

from decimal import Decimal

