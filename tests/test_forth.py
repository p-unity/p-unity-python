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

    options = {}

    def test_0000(self):
        r"""
        1 2 3
        """
        e = FORTH.Engine(self.test_0000.__doc__, **self.options)
        assert e.root.stack == [1, 2, 3]
        assert e.root.memory == {}

    def test_0001(self):
        r"""
        'Hello 'World
        """
        e = FORTH.Engine(self.test_0001.__doc__, **self.options)
        assert e.root.stack == ["Hello", "World"]
        assert e.root.memory == {}

    def test_0002(self):
        r"""
        123 456 !
        """
        e = FORTH.Engine(self.test_0002.__doc__, **self.options)
        assert e.root.stack == []
        assert e.root.memory == {456 : 123}


    def test_0003(self):
        r"""
        123 'FOO_1 !
        'Baz 'FOO_2 !
        """
        e = FORTH.Engine(self.test_0003.__doc__, **self.options)
        assert e.root.stack == []
        assert e.root.memory == {"FOO_1" : 123, "FOO_2": "Baz"}


    def test_1000(self):
        r"""
        T{ 'Hello 'World DROP -> ("Hello") }T
        """
        e = FORTH.Engine(self.test_1000.__doc__, **self.options)
        assert e.root.test["f"] == 0

    def test_BASIC_ASSUMPTIONS(self):
        e = FORTH.Engine(self.BASIC_ASSUMPTIONS, **self.options)
        assert e.root.test["f"] == 0

    BASIC_ASSUMPTIONS = r"""

T{ -> }T               \ START WITH CLEAN SLATE
( TEST IF ANY BITS ARE SET; ANSWER IN BASE 1 )
T{ : BITSSET? IF 0 0 ELSE 0 THEN ; -> }T
T{  0 BITSSET? -> 0 }T      ( ZERO IS ALL BITS CLEAR )
T{  1 BITSSET? -> 0 0 }T      ( OTHER NUMBER HAVE AT LEAST ONE BIT )
T{ -1 BITSSET? -> 0 0 }T

    """

    def test_BOOLEANS_INVERT(self):
        e = FORTH.Engine(self.BOOLEANS_INVERT, **self.options)
        assert e.root.test["f"] == 0

    BOOLEANS_INVERT = r"""

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


    def test_LSHIFT_RSHIFT(self):
        e = FORTH.Engine(self.LSHIFT_RSHIFT, **self.options)
        assert e.root.test["f"] == 0

    LSHIFT_RSHIFT = r"""

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


    def test_COMPARISONS(self):
        e = FORTH.Engine(self.COMPARISONS, **self.options)
        assert e.root.test["f"] == 0

    COMPARISONS = r"""

0    CONSTANT 0S
0 INVERT CONSTANT 1S
1S 1 RSHIFT INVERT CONSTANT MSB
T{ : BITSSET? IF 0 0 ELSE 0 THEN ; -> }T

( )

T{ 0 0= -> <TRUE> }T
T{ 1 0= -> <FALSE> }T
T{ 2 0= -> <FALSE> }T
T{ -1 0= -> <FALSE> }T

T{ 0 0 = -> <TRUE> }T
T{ 1 1 = -> <TRUE> }T
T{ -1 -1 = -> <TRUE> }T
T{ 1 0 = -> <FALSE> }T
T{ -1 0 = -> <FALSE> }T
T{ 0 1 = -> <FALSE> }T
T{ 0 -1 = -> <FALSE> }T

T{ 0 0< -> <FALSE> }T
T{ -1 0< -> <TRUE> }T
T{ 1 0< -> <FALSE> }T

T{ 0 1 < -> <TRUE> }T
T{ 1 2 < -> <TRUE> }T
T{ -1 0 < -> <TRUE> }T
T{ -1 1 < -> <TRUE> }T
T{ 0 0 < -> <FALSE> }T
T{ 1 1 < -> <FALSE> }T
T{ 1 0 < -> <FALSE> }T
T{ 2 1 < -> <FALSE> }T
T{ 0 -1 < -> <FALSE> }T
T{ 1 -1 < -> <FALSE> }T

T{ 0 1 > -> <FALSE> }T
T{ 1 2 > -> <FALSE> }T
T{ -1 0 > -> <FALSE> }T
T{ -1 1 > -> <FALSE> }T
T{ 0 0 > -> <FALSE> }T
T{ 1 1 > -> <FALSE> }T
T{ 1 0 > -> <TRUE> }T
T{ 2 1 > -> <TRUE> }T
T{ 0 -1 > -> <TRUE> }T
T{ 1 -1 > -> <TRUE> }T

T{ 0 1 U< -> <TRUE> }T
T{ 1 2 U< -> <TRUE> }T
T{ 0 0 U< -> <FALSE> }T
T{ 1 1 U< -> <FALSE> }T
T{ 1 0 U< -> <FALSE> }T
T{ 2 1 U< -> <FALSE> }T

T{ 0 1 MIN -> 0 }T
T{ 1 2 MIN -> 1 }T
T{ -1 0 MIN -> -1 }T
T{ -1 1 MIN -> -1 }T
T{ 0 0 MIN -> 0 }T
T{ 1 1 MIN -> 1 }T
T{ 1 0 MIN -> 0 }T
T{ 2 1 MIN -> 1 }T
T{ 0 -1 MIN -> -1 }T
T{ 1 -1 MIN -> -1 }T

T{ 0 1 MAX -> 1 }T
T{ 1 2 MAX -> 2 }T
T{ -1 0 MAX -> 0 }T
T{ -1 1 MAX -> 1 }T
T{ 0 0 MAX -> 0 }T
T{ 1 1 MAX -> 1 }T
T{ 1 0 MAX -> 1 }T
T{ 2 1 MAX -> 2 }T
T{ 0 -1 MAX -> 0 }T
T{ 1 -1 MAX -> 1 }T

        """


    def test_STACK_OPS(self):
        e = FORTH.Engine(self.STACK_OPS, **self.options)
        assert e.root.test["f"] == 0

    STACK_OPS = r"""

T{ 1 2 2DROP -> }T
T{ 1 2 2DUP -> 1 2 1 2 }T
T{ 1 2 3 4 2OVER -> 1 2 3 4 1 2 }T
T{ 1 2 3 4 2SWAP -> 3 4 1 2 }T
T{ 0 ?DUP -> 0 }T
T{ 1 ?DUP -> 1 1 }T
T{ -1 ?DUP -> -1 -1 }T
T{ DEPTH -> 0 }T
T{ 0 DEPTH -> 0 1 }T
T{ 0 1 DEPTH -> 0 1 2 }T
T{ 0 DROP -> }T
T{ 1 2 DROP -> 1 }T
T{ 1 DUP -> 1 1 }T
T{ 1 2 OVER -> 1 2 1 }T
T{ 1 2 3 ROT -> 2 3 1 }T
T{ 1 2 SWAP -> 2 1 }T

    """


    def test_RETURN_STACK(self):
        e = FORTH.Engine(self.RETURN_STACK, **self.options)
        assert e.root.test["f"] == 0

    RETURN_STACK = r"""

0 CONSTANT 0S
0 INVERT CONSTANT 1S

( )

T{ : GR1 >R R> ; -> }T
T{ : GR2 >R R@ R> DROP ; -> }T
T{ 123 GR1 -> 123 }T
T{ 123 GR2 -> 123 }T
T{ 1S GR1 -> 1S }T   ( RETURN STACK HOLDS CELLS )

    """

    def test_ADD_SUBTRACT(self):
        e = FORTH.Engine(self.ADD_SUBTRACT, **self.options)
        assert e.root.test["f"] == 0

    ADD_SUBTRACT = r"""

T{ 0 5 + -> 5 }T
T{ 5 0 + -> 5 }T
T{ 0 -5 + -> -5 }T
T{ -5 0 + -> -5 }T
T{ 1 2 + -> 3 }T
T{ 1 -2 + -> -1 }T
T{ -1 2 + -> 1 }T
T{ -1 -2 + -> -3 }T
T{ -1 1 + -> 0 }T
# T{ MID-UINT 1 + -> MID-UINT+1 }T

T{ 0 5 - -> -5 }T
T{ 5 0 - -> 5 }T
T{ 0 -5 - -> 5 }T
T{ -5 0 - -> -5 }T
T{ 1 2 - -> -1 }T
T{ 1 -2 - -> 3 }T
T{ -1 2 - -> -3 }T
T{ -1 -2 - -> 1 }T
T{ 0 1 - -> -1 }T
# T{ MID-UINT+1 1 - -> MID-UINT }T

T{ 0 1+ -> 1 }T
T{ -1 1+ -> 0 }T
T{ 1 1+ -> 2 }T
# T{ MID-UINT 1+ -> MID-UINT+1 }T

T{ 2 1- -> 1 }T
T{ 1 1- -> 0 }T
T{ 0 1- -> -1 }T
# T{ MID-UINT+1 1- -> MID-UINT }T

T{ 0 NEGATE -> 0 }T
T{ 1 NEGATE -> -1 }T
T{ -1 NEGATE -> 1 }T
T{ 2 NEGATE -> -2 }T
T{ -2 NEGATE -> 2 }T

T{ 0 ABS -> 0 }T
T{ 1 ABS -> 1 }T
T{ -1 ABS -> 1 }T
# T{ MIN-INT ABS -> MID-UINT+1 }T

    """

    def test_MULTIPLY(self):
        e = FORTH.Engine(self.MULTIPLY, **self.options)
        assert e.root.test["f"] == 0

    MULTIPLY = r"""

# T{ 0 S>D -> 0 0 }T
# T{ 1 S>D -> 1 0 }T
# T{ 2 S>D -> 2 0 }T
# T{ -1 S>D -> -1 -1 }T
# T{ -2 S>D -> -2 -1 }T
# T{ MIN-INT S>D -> MIN-INT -1 }T
# T{ MAX-INT S>D -> MAX-INT 0 }T

# T{ 0 0 M* -> 0 S>D }T
# T{ 0 1 M* -> 0 S>D }T
# T{ 1 0 M* -> 0 S>D }T
# T{ 1 2 M* -> 2 S>D }T
# T{ 2 1 M* -> 2 S>D }T
# T{ 3 3 M* -> 9 S>D }T
# T{ -3 3 M* -> -9 S>D }T
# T{ 3 -3 M* -> -9 S>D }T
# T{ -3 -3 M* -> 9 S>D }T
# T{ 0 MIN-INT M* -> 0 S>D }T
# T{ 1 MIN-INT M* -> MIN-INT S>D }T
# T{ 2 MIN-INT M* -> 0 1S }T
# T{ 0 MAX-INT M* -> 0 S>D }T
# T{ 1 MAX-INT M* -> MAX-INT S>D }T
# T{ 2 MAX-INT M* -> MAX-INT 1 LSHIFT 0 }T
# T{ MIN-INT MIN-INT M* -> 0 MSB 1 RSHIFT }T
# T{ MAX-INT MIN-INT M* -> MSB MSB 2/ }T
# T{ MAX-INT MAX-INT M* -> 1 MSB 2/ INVERT }T

T{ 0 0 * -> 0 }T            \ TEST IDENTITIES
T{ 0 1 * -> 0 }T
T{ 1 0 * -> 0 }T
T{ 1 2 * -> 2 }T
T{ 2 1 * -> 2 }T
T{ 3 3 * -> 9 }T
T{ -3 3 * -> -9 }T
T{ 3 -3 * -> -9 }T
T{ -3 -3 * -> 9 }T

# T{ MID-UINT+1 1 RSHIFT 2 * -> MID-UINT+1 }T
# T{ MID-UINT+1 2 RSHIFT 4 * -> MID-UINT+1 }T
# T{ MID-UINT+1 1 RSHIFT MID-UINT+1 OR 2 * -> MID-UINT+1 }T

# T{ 0 0 UM* -> 0 0 }T
# T{ 0 1 UM* -> 0 0 }T
# T{ 1 0 UM* -> 0 0 }T
# T{ 1 2 UM* -> 2 0 }T
# T{ 2 1 UM* -> 2 0 }T
# T{ 3 3 UM* -> 9 0 }T

# T{ MID-UINT+1 1 RSHIFT 2 UM* -> MID-UINT+1 0 }T
# T{ MID-UINT+1 2 UM* -> 0 1 }T
# T{ MID-UINT+1 4 UM* -> 0 2 }T
# T{ 1S 2 UM* -> 1S 1 LSHIFT 1 }T
# T{ MAX-UINT MAX-UINT UM* -> 1 1 INVERT }T

    """

    def test_HERE(self):
        e = FORTH.Engine(self.HERE, **self.options)
        assert e.root.test["f"] == 0

    HERE = r"""

0 CONSTANT 0S
0 INVERT CONSTANT 1S

( )

HERE 1 ALLOT
HERE
CONSTANT 2NDA
CONSTANT 1STA
T{ 1STA 2NDA U< -> <TRUE> }T      \ HERE MUST GROW WITH ALLOT
T{ 1STA 1+ -> 2NDA }T         \ ... BY ONE ADDRESS UNIT
( MISSING TEST: NEGATIVE ALLOT )

\ Added by GWJ so that ALIGN can be used before , (comma) is tested
1 ALIGNED CONSTANT ALMNT   \ -- 1|2|4|8 for 8|16|32|64 bit alignment
ALIGN
T{ HERE 1 ALLOT ALIGN HERE SWAP - ALMNT = -> <TRUE> }T
\ End of extra test

HERE 1 ,
HERE 2 ,
CONSTANT 2ND
CONSTANT 1ST
T{ 1ST 2ND U< -> <TRUE> }T         \ HERE MUST GROW WITH ALLOT
T{ 1ST CELL+ -> 2ND }T         \ ... BY ONE CELL
T{ 1ST 1 CELLS + -> 2ND }T
T{ 1ST @ 2ND @ -> 1 2 }T
T{ 5 1ST ! -> }T
T{ 1ST @ 2ND @ -> 5 2 }T
T{ 6 2ND ! -> }T
T{ 1ST @ 2ND @ -> 5 6 }T
# T{ 1ST 2@ -> 6 5 }T
# T{ 2 1 1ST 2! -> }T
# T{ 1ST 2@ -> 2 1 }T
# T{ 1S 1ST !  1ST @ -> 1S }T      \ CAN STORE CELL-WIDE VALUE

    """


    def test_COMPILE(self):
        e = FORTH.Engine(self.COMPILE, **self.options)
        assert e.root.test["f"] == 0

    COMPILE = r"""

T{ : GT1 123 ; -> }T
T{ ' GT1 EXECUTE -> 123 }T
T{ : GT2 ['] GT1 ; IMMEDIATE -> }T
T{ GT2 EXECUTE -> 123 }T
HERE 3 C, CHAR G C, CHAR T C, CHAR 1 C, CONSTANT GT1STRING
HERE 3 C, CHAR G C, CHAR T C, CHAR 2 C, CONSTANT GT2STRING
T{ GT1STRING FIND -> ' GT1 -1 }T
T{ GT2STRING FIND -> ' GT2 1 }T
( HOW TO SEARCH FOR NON-EXISTENT WORD? )
( T{ : GT3 GT2 LITERAL ; -> }T )
( T{ GT3 -> ' GT1 }T )
( T{ GT1STRING COUNT -> GT1STRING CHAR+ 3 }T )

    """




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

