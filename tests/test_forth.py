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

    def test_engine_0000(self):
        r"""
        1 2 3
        """
        e = FORTH.Engine(autoexec=self.test_engine_0000.__doc__)
        assert e.stack == [1, 2, 3]
        assert e.memory == {}

    def test_engine_0001(self):
        r"""
        'Hello 'World
        """
        e = FORTH.Engine(autoexec=self.test_engine_0001.__doc__)
        assert e.stack == ["Hello", "World"]
        assert e.memory == {}

    def test_engine_0002(self):
        r"""
        123 456 !
        """
        e = FORTH.Engine(autoexec=self.test_engine_0002.__doc__)
        assert e.stack == []
        assert e.memory == {456 : 123}


    def test_engine_0003(self):
        r"""
        123 'FOO_1 !
        'Baz 'FOO_2 !
        """
        e = FORTH.Engine(autoexec=self.test_engine_0003.__doc__)
        assert e.stack == []
        assert e.memory == {"FOO_1" : 123, "FOO_2": "Baz"}


    def test_engine_1000(self):
        r"""
        T{ 'Hello 'World DROP -> ("Hello") }T
        """
        e = FORTH.Engine(autoexec=self.test_engine_1000.__doc__)
        assert e.TEST.f_count == 0

from p_unity import FORTH

try:
    from icecream import ic
except ImportError:  # Graceful fallback if IceCream isn't installed.
    ic = lambda *a: None if not a else (a[0] if len(a) == 1 else a)  # noqa

builtins = __import__('builtins')
setattr(builtins, 'ic', ic)
