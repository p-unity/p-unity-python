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
        assert e.root.stack == [1, 2, 3]
        assert e.root.memory == {}

    def test_engine_0001(self):
        r"""
        'Hello 'World
        """
        e = FORTH.Engine(autoexec=self.test_engine_0001.__doc__)
        assert e.root.stack == ["Hello", "World"]
        assert e.root.memory == {}

    def test_engine_0002(self):
        r"""
        123 456 !
        """
        e = FORTH.Engine(autoexec=self.test_engine_0002.__doc__)
        assert e.root.stack == []
        assert e.root.memory == {456 : 123}


    def test_engine_0003(self):
        r"""
        123 'FOO_1 !
        'Baz 'FOO_2 !
        """
        e = FORTH.Engine(autoexec=self.test_engine_0003.__doc__)
        assert e.root.stack == []
        assert e.root.memory == {"FOO_1" : 123, "FOO_2": "Baz"}


    def test_engine_1000(self):
        r"""
        T{ 'Hello 'World DROP -> ("Hello") }T
        """
        e = FORTH.Engine(autoexec=self.test_engine_1000.__doc__)
        assert e.root.f_count == 0

    def test_BASIC_ASSUMPTIONS(self):
        r"""

T{ -> }T               \ START WITH CLEAN SLATE
( TEST IF ANY BITS ARE SET; ANSWER IN BASE 1 )
T{ : BITSSET? IF 0 0 ELSE 0 THEN ; -> }T
T{  0 BITSSET? -> 0 }T      ( ZERO IS ALL BITS CLEAR )
T{  1 BITSSET? -> 0 0 }T      ( OTHER NUMBER HAVE AT LEAST ONE BIT )
T{ -1 BITSSET? -> 0 0 }T

        """
        e = FORTH.Engine(autoexec=self.test_BASIC_ASSUMPTIONS.__doc__)
        assert e.root.f_count == 0


    def test_BOOLEANS_INVERT(self):
        r"""

T{ 0 0 AND -> 0 }T
T{ 0 1 AND -> 0 }T
T{ 1 0 AND -> 0 }T
T{ 1 1 AND -> 1 }T

T{ 0 INVERT 1 AND -> 1 }T
T{ 1 INVERT 1 AND -> 0 }T

0    CONSTANT 0S
0 INVERT CONSTANT 1S

T{ 0S INVERT -> 1S }T
T{ 1S INVERT -> 0S }T

T{ 0S 0S AND -> 0S }T
T{ 0S 1S AND -> 0S }T
T{ 1S 0S AND -> 0S }T
T{ 1S 1S AND -> 1S }T

T{ 0S 0S OR -> 0S }T
T{ 0S 1S OR -> 1S }T
T{ 1S 0S OR -> 1S }T
T{ 1S 1S OR -> 1S }T

T{ 0S 0S XOR -> 0S }T
T{ 0S 1S XOR -> 1S }T
T{ 1S 0S XOR -> 1S }T
T{ 1S 1S XOR -> 0S }T

        """
        e = FORTH.Engine(autoexec=self.test_BOOLEANS_INVERT.__doc__)
        assert e.root.f_count == 0



    def test_LSHIFT_RSHIFT(self):
        r"""

0    CONSTANT 0S
0 INVERT CONSTANT 1S
1S 1 RSHIFT INVERT CONSTANT MSB
T{ : BITSSET? IF 0 0 ELSE 0 THEN ; -> }T

( )

( WE TRUST 1S, INVERT, AND BITSSET?; WE WILL CONFIRM RSHIFT LATER )
1S 1 RSHIFT INVERT CONSTANT MSB
# T{ MSB BITSSET? -> 0 0 }T

T{ 0S 2* -> 0S }T
T{ 1 2* -> 2 }T
T{ 4000 2* -> 8000 }T
T{ 1S 2* 1 XOR -> 1S }T
T{ MSB 2* -> 0S }T

T{ 0S 2/ -> 0S }T
T{ 1 2/ -> 0 }T
T{ 4000 2/ -> 2000 }T
T{ 1S 2/ -> 1S }T            \ MSB PROPOGATED
T{ 1S 1 XOR 2/ -> 1S }T
T{ MSB 2/ MSB AND -> MSB }T

T{ 1 0 LSHIFT -> 1 }T
T{ 1 1 LSHIFT -> 2 }T
T{ 1 2 LSHIFT -> 4 }T
# T{ 1 F LSHIFT -> 8000 }T         \ BIGGEST GUARANTEED SHIFT
T{ 1S 1 LSHIFT 1 XOR -> 1S }T
T{ MSB 1 LSHIFT -> 0 }T

T{ 1 0 RSHIFT -> 1 }T
T{ 1 1 RSHIFT -> 0 }T
T{ 2 1 RSHIFT -> 1 }T
T{ 4 2 RSHIFT -> 1 }T
# T{ 8000 F RSHIFT -> 1 }T         \ BIGGEST
T{ MSB 1 RSHIFT MSB AND -> 0 }T      \ RSHIFT ZERO FILLS MSBS
T{ MSB 1 RSHIFT 2* -> MSB }T

        """
        e = FORTH.Engine(autoexec=self.test_LSHIFT_RSHIFT.__doc__)
        assert e.root.f_count == 0








from p_unity import FORTH

try:
    from icecream import ic
except ImportError:  # Graceful fallback if IceCream isn't installed.
    ic = lambda *a: None if not a else (a[0] if len(a) == 1 else a)  # noqa

builtins = __import__('builtins')
setattr(builtins, 'ic', ic)

#
# \ From: John Hayes S1I
# \ Subject: core.fr
# \ Date: Mon, 27 Nov 95 13:10
#
# \ (C) 1995 JOHNS HOPKINS UNIVERSITY / APPLIED PHYSICS LABORATORY
# \ MAY BE DISTRIBUTED FREELY AS LONG AS THIS COPYRIGHT NOTICE REMAINS.
# \ VERSION 1.2
# \ THIS PROGRAM TESTS THE CORE WORDS OF AN ANS FORTH SYSTEM.
# \ THE PROGRAM ASSUMES A TWO'S COMPLEMENT IMPLEMENTATION WHERE
# \ THE RANGE OF SIGNED NUMBERS IS -2^(N-1) ... 2^(N-1)-1 AND
# \ THE RANGE OF UNSIGNED NUMBERS IS 0 ... 2^(N)-1.
# \ I HAVEN'T FIGURED OUT HOW TO TEST KEY, QUIT, ABORT, OR ABORT"...
# \ I ALSO HAVEN'T THOUGHT OF A WAY TO TEST ENVIRONMENT?...
#

