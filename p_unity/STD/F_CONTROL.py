#!/usr/bin/env python3
# -*- encoding: utf-8


__banner__ = """ ( Copyright Intermine.com.au Pty Ltd. or its affiliates.
                   SPDX-License-Identifier: Programming-Unity-10.42

     _       _____    ____    _   _   _______   _____     ____    _
  /\| |/\   / ____|  / __ \  | \ | | |__   __| |  __ \   / __ \  | |
  \ ` ' /  | |      | |  | | |  \| |    | |    | |__) | | |  | | | |
 |_     _| | |      | |  | | | . ` |    | |    |  _  /  | |  | | | |
  / , . \  | |____  | |__| | | |\  |    | |    | | \ \  | |__| | | |____
  \/|_|\/   \_____|  \____/  |_| \_|    |_|    |_|  \_\  \____/  |______|



)





""" # __banner__

class LIB: # { Control Flow : words }

    """

    T{ : GI1 IF 123 THEN ; -> }T
    T{ : GI2 IF 123 ELSE 234 THEN ; -> }T
    T{  0 GI1 ->     }T
    T{  1 GI1 -> 123 }T
    T{ -1 GI1 -> 123 }T
    T{  0 GI2 -> 234 }T
    T{  1 GI2 -> 123 }T
    T{ -1 GI1 -> 123 }T

    """

    def __init__(self, **kwargs):
        pass

    @staticmethod ### IF ###
    def word_IF__R(f, b):
        c = {"m":"IF", "b":b, "IF":[], "ELSE":[], "r":f.state}
        f.cstack.append(c)
        f.state = f.IF

    @staticmethod ### ELSE ###
    def word_ELSE__R(f):
        f.state = f.ELSE

    @staticmethod ### THEN ###
    def word_THEN__R(f):
        c = f.cstack.pop()
        f.state = c["r"]
        if c["b"]:
            f.execute(c["IF"])
        else:
            f.execute(c["ELSE"])


from collections import namedtuple

