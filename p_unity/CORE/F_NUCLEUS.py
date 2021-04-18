#!/usr/bin/env python3
# -*- encoding: utf-8


__banner__ = r""" ( Copyright Intermine.com.au Pty Ltd. or its affiliates.
                    License SPDX: Programming-Unity-10.42 or as negotiated.

     _      _   _   _    _    _____   _        ______   _    _    _____
  /\| |/\  | \ | | | |  | |  / ____| | |      |  ____| | |  | |  / ____|
  \ ` ' /  |  \| | | |  | | | |      | |      | |__    | |  | | | (___
 |_     _| | . ` | | |  | | | |      | |      |  __|   | |  | |  \___ \
  / , . \  | |\  | | |__| | | |____  | |____  | |____  | |__| |  ____) |
  \/|_|\/  |_| \_|  \____/   \_____| |______| |______|  \____/  |_____/



)





""" # __banner__

class LIB: # { Nucleus : words }

    """

    T{ -> }T

    """

    def __init__(self, f, **kwargs):
        pass


    @staticmethod ### WORDS ###
    def word_WORDS(f):
        words = []
        for name in f.words.keys():
            words.append(name)
        for name in f.sigils.keys():
            words.append(name)
        words.sort()
        print(" ".join(words))


    @staticmethod ### ! ### ( x a-addr -- )
    def word_bang__M__R(f, x, a): # Store x at a-addr.
        ""
        f.memory[a] = x


    @staticmethod ### @ ###
    def word_at__R_x(f, a):
        f.stack.append(f.memory.get(a,0))


    @staticmethod ### @NONE ###
    def word_at_NONE__R_x(f, a):
        f.stack.append(f.memory.get(a,None))


    # ( x "<spaces>name" -- )
    @staticmethod ### VARIABLE ###
    def word_VARIABLE__V__R_a(f):
        """
        T{ VARIABLE V1 ->     }T
        T{    123 V1 ! ->     }T
        T{        V1 @ -> 123 }T
        """
        f.state = f.VARIABLE


    # ( x "<spaces>name" -- )
    @staticmethod ### CONSTANT ###
    def word_CONSTANT__R(f, x):
        """
        T{ 123 CONSTANT X123 ->     }T
        T{ X123              -> 123 }T
        T{ : EQU CONSTANT ;  ->     }T
        T{ X123 EQU Y123     ->     }T
        T{ Y123              -> 123 }T
        """
        f.constant__ = x
        f.state = f.CONSTANT

    @staticmethod ### 1+ ###
    def word_1_plus__R_n2(f, n1):
        return (n1 + 1,)

    @staticmethod ### 1- ###
    def word_1_minus__R_n2(f, n1):
        return (n1 - 1,)

    @staticmethod ### 2+ ###
    def word_2_plus__R_n2(f, n1):
        return (n1 + 2,)

    @staticmethod ### 2- ###
    def word_2_minus__R_n2(f, n1):
        return (n1 - 2,)

    @staticmethod ### HERE ###
    def word_HERE__R_a(f):
        return (f.here,)

    @staticmethod ### ALLOT ###
    def word_ALLOT__R(f, n):
        f.here = f.here + n

    @staticmethod ### <TRUE> ###
    def word_langle_TRUE_rangle__R_b(f):
        return (True,)

    @staticmethod ### <FALSE> ###
    def word_langle_FALSE_rangle__R_b(f):
        return (False,)




