#!/usr/bin/env python3
# -*- encoding: utf-8


__banner__ = r""" ( Copyright Intermine.com.au Pty Ltd. or its affiliates.
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

    T{  0 IF 123 THEN ->     }T
    T{ -1 IF 123 THEN -> 123 }T
    T{  1 IF 123 THEN -> 123 }T
    T{ -1 IF 123 THEN -> 123 }T
    T{  0 IF 123 ELSE 234 THEN -> 234 }T
    T{  1 IF 123 ELSE 234 THEN -> 123 }T

    # if(0) {
    # } else {
    # }

    """

    def __init__(self, **kwargs):
        pass

    @staticmethod ### EXIT ###
    def word_EXIT__R(f):
        i = len(f.cstack) - 1
        while i >= 0:
            if f.cstack[i].get("m",None) == "CALL":
                f.cstack[i]["EXIT"] = True
                break

    @staticmethod ### <.IF ###
    def word_langle_dot_IF__R(f, b):
        c = {"m":"<.IF", "b":b, "THEN.>":[], "ELSE.>":[], "r":f.state}
        f.cstack.append(c)
        f.state = f.langle_dot_IF

    @staticmethod ### THEN.> ###
    def word_THEN_dot_rangle__R(f):
        f.raise_SyntaxException("THEN.>: error(-0): Free Standing THEN.> Not Allowed")

    @staticmethod ### ELSE.> ###
    def word_ELSE_dot_rangle__R(f):
        f.raise_SyntaxException("ELSE.>: error(-0): Free Standing ELSE.> Not Allowed")

    @staticmethod ### IF. ###
    def word_IF_dot__R(f, free_standing=True):

        """
        T{ 0 <.IF THEN.> 'YES ELSE.> 'NO IF. -> 'NO }T
        T{ <true> <.IF THEN.> 'YES ELSE.> 'NO IF. -> 'YES }T
        """

        if free_standing:
            f.raise_SyntaxException("ELSE.>: error(-0): Free Standing IF. Not Allowed")

        c = f.cstack.pop()
        f.state = c["r"]
        if ic(c["b"]):
           f.execute(c["THEN.>"])
        else:
           f.execute(c["ELSE.>"])


    @staticmethod ### BEGIN ###
    def word_BEGIN__R(f):
        c = {"m":"BEGIN", "TOKENS":[], "r":f.state}
        f.cstack.append(c)
        f.state = f.BEGIN

    @staticmethod ### REPEAT ###
    def word_REPEAT__R(f, free_standing=True):
        if free_standing:
            f.raise_SyntaxException("REPEAT: error(-0): Free Standing REPEAT Not Allowed")

        c = f.cstack.pop()
        ic(c)
        while True:
            ic(c["TOKENS"])
            f.state = f.INTERPRET
            f.execute(c["TOKENS"])
            if not f.stack.pop():
                break

        f.state = c["r"]


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
        return impl_THEN__R(f)

    @staticmethod ### END_IF ###
    def word_END_IF__R(f):
        return impl_THEN__R(f)







    @staticmethod ### < ###
    def word_langle__R_b(f, x1, x2):
        return (x1 < x2,)

    @staticmethod ### <= ###
    def word_langle_equal__R_b(f, x1, x2):
        return (x1 <= x2,)

    @staticmethod ### > ###
    def word_rangle__R_b(f, x1, x2):
        return (x1 > x2,)

    @staticmethod ### >= ###
    def word_rangle_equal__R_b(f, x1, x2):
        return (x1 >= x2,)

    @staticmethod ### <> ###
    def word_langle_rangle__R_b(f, x1, x2):
        return (x1 != x2,)

    @staticmethod ### ~= ###
    def word_tidlies_equal__R_b(f, x1, x2):
        return (x1 != x2,)

    @staticmethod ### != ###
    def word_bang_equal__R_b(f, x1, x2):
        return (x1 != x2,)

    @staticmethod ### 0= ###
    def word_0_equal__R_b(f, x):
        """
        T{ 0 0= -> <true> }T
        T{ 0.0 0= -> <true> }T
        T{ 0.0j 0= -> <true> }T
        """
        return (x == 0,)

    @staticmethod ### 0< ###
    def word_0_langle__R_b(f, x):
        return (x < 0,)

    @staticmethod ### 0> ###
    def word_0_rangle__R_b(f, x):
        return (x > 0,)

def impl_THEN__R(f):
    c = f.cstack.pop()
    f.state = c["r"]
    if c["b"]:
       f.execute(c["IF"])
    else:
       f.execute(c["ELSE"])

from collections import namedtuple

