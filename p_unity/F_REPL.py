#!/usr/bin/env python3
# -*- encoding: utf-8


__banner__ = """ ( Copyright Intermine.com.au Pty Ltd. or its affiliates.
                   SPDX-License-Identifier: Programming-Unity-10.42

     _      _____    ______   _____    _
  /\| |/\  |  __ \  |  ____| |  __ \  | |
  \ ` ' /  | |__) | | |__    | |__) | | |
 |_     _| |  _  /  |  __|   |  ___/  | |
  / , . \  | | \ \  | |____  | |      | |____
  \/|_|\/  |_|  \_\ |______| |_|      |______|



)





""" # __banner__

class P_UNITY: # { By the Power of Introspection : words }

    def __init__(self):
        pass

    @staticmethod ### . ###
    def word_dot__R(f, x):
        print(f" {x}")

    @staticmethod ### .. ###
    def word_dot_dot__R_x(f, x):
        print(x)
        return (x,)

    @staticmethod ### DIR ###
    def word_DIR__R_x(f, x):
        d = []
        for k in dir(x):
            if not k[0] == '_': d.append(k)
        print(str(d))
        return (x,)

    @staticmethod ### DIR:ALL ###
    def word_DIR_colon_ALL__R_x(f, x):
        print(str(dir(x)))
        return (x,)

    @staticmethod ### SEE ###
    def word_SEE(f):
        f.state = f.SEE

    @staticmethod ### SEE:MEM ###
    def word_SEE_colon_MEM(f):
        print(str(f.memory))

    @staticmethod ### SEE:ALL ###
    def word_SEE_colon_ALL(f):
        show = {}
        for name in f.words:
            if not callable(f.words[name]):
                show[name] = f.words[name]
        print(str(show))

    @staticmethod ### SEE:ALL+ ###
    def word_SEE_colon_ALL_plus(f):
        show = {}
        for name in f.words:
            if not callable(f.words[name]):
                show[name] = f.words[name]
            else:
                show[name] = (f.words_argc.get(name,0))
        print(str(show))
        show = {}
        for name in f.sigils:
            show[name] = ('SIGIL')
        print(str(show))

    @staticmethod ### SEE:ALL++ ###
    def word_SEE_colon_ALL_plus_plus(f):
        print(str(f.words))
        print(str(f.sigils))


