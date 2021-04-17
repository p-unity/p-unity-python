#!/usr/bin/env python3
# -*- encoding: utf-8


__banner__ = r""" ( Copyright Intermine.com.au Pty Ltd. or its affiliates.
                   SPDX-License-Identifier: Programming-Unity-10.42

     _           _    _____    ____    _   _
  /\| |/\       | |  / ____|  / __ \  | \ | |
  \ ` ' /       | | | (___   | |  | | |  \| |
 |_     _|  _   | |  \___ \  | |  | | | . ` |
  / , . \  | |__| |  ____) | | |__| | | |\  |
  \/|_|\/   \____/  |_____/   \____/  |_| \_|



)





""" # __banner__

class LIB: # { JavaScript Object Notation : words }

    def __init__(self, **kwargs):
        pass

    @staticmethod ### JSON-SAVE ###
    def word_JSON_minus_SAVE__R_s(f, x):
        def encode(_):
            if isinstance(_, complex):
                return {'__complex__':True, 'real':_.real, 'imag':_.imag}
            raise TypeError(repr(_) + " is not JSON serializable")
        return (x, simplejson.dumps(x, default=encode),)

    @staticmethod ### JSON-LOAD ###
    def word_JSON_minus_LOAD__R_x(f, s):
        def h(_):
            if '__complex__' in _:
                return complex(_['real'], _['imag'])
            return _
        return (simplejson.loads(s, use_decimal=True, object_hook=h),)

