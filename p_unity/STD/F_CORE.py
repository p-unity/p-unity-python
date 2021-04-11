#!/usr/bin/env python3
# -*- encoding: utf-8


__banner__ = """ ( Copyright Intermine.com.au Pty Ltd. or its affiliates.
                   SPDX-License-Identifier: Programming-Unity-10.42

     _       _____    ____    _____    ______
  /\| |/\   / ____|  / __ \  |  __ \  |  ____|
  \ ` ' /  | |      | |  | | | |__) | | |__
 |_     _| | |      | |  | | |  _  /  |  __|
  / , . \  | |____  | |__| | | | \ \  | |____
  \/|_|\/   \_____|  \____/  |_|  \_\ |______|



)





""" # __banner__

class LIB: # { CORE FORTH : words }

    """

    T{ -> }T

    """

    def __init__(self, **kwargs):
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

    @staticmethod ### HERE ###
    def word_HERE__R_a(f):
        return (f.here,)

    @staticmethod ### ALLOT ###
    def word_ALLOT__R(f, n):
        f.here = f.here + n

    @staticmethod ### ! ###
    def word_bang(f, v, a):
        f.memory[a] = v

    @staticmethod ### @ ###
    def word_at(f, a):
        f.stack.append(f.memory.get(a,0))



