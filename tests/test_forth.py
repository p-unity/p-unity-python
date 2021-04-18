#!/usr/bin/env python3
# -*- encoding: utf-8


__banner__ = r""" ( Copyright Intermine.com.au Pty Ltd. or its affiliates.
                    License SPDX: Programming-Unity-10.42 or as negotiated.

  _            _              ______ ____  _____ _______ _    _
 | |          | |            |  ____/ __ \|  __ \__   __| |  | |
 | |_ ___  ___| |_           | |__ | |  | | |__) | | |  | |__| |
 | __/ _ \/ __| __|          |  __|| |  | |  _  /  | |  |  __  |
 | ||  __/\__ \ |_           | |   | |__| | | \ \  | |  | |  | |
  \__\___||___/\__|          |_|    \____/|_|  \_\ |_|  |_|  |_|
                     ______
                    |______|

)





""" # __banner__

class TestFORTH:

    def test_engine(self):

        from p_unity import FORTH

        e = FORTH.Engine()

        e.execute("1 2 3".split())

        assert e.stack == [1, 2, 3]

