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
# : ; ' ." ! @ @NONE CREATE HERE ALLOT
# VARIABLE CONSTANT VALUE TO LOCALS| |
# 1+ 1- 2+ 2- <TRUE> <FALSE>


""" # __banner__

class LIB: # { Nucleus : words }

    """

0 999999 !

: TEN 10 ;

T{ TEN -> 10 }T

    """

    def __init__(self, e, **kwargs):
        pass

    @staticmethod ### ( ###
    def sigil_lparen(e, t, c, token, start=False):
        end = token[-1] == ")"
        if end:
            t.state = e.state_INTERPRET
            return

        t.state = e.NUCLEUS.sigil_lparen


    @staticmethod ### \ ###
    def sigil_slash(e, t, c, token, start=False):
        c.stack.append({"?":"SLASH", "LINE":t.line, "r":t.state})
        t.state = e.NUCLEUS.state_slash

    @staticmethod
    def state_slash(e, t, c, token):
        struct = c.stack[-1]
        if struct["LINE"] == t.line:
            return

        c.stack.pop()
        t.state = struct["r"]
        t.state(e, t, c, token)


    @staticmethod ### T{ ###
    def word_T_lbrace(e, t, c):
        stack = copy.deepcopy(t.stack)
        c.stack.append({"?":"TEST", "STACK":t.stack})
        t.stack = stack

    @staticmethod ### T{! ###
    def word_T_lbrace_bang(e, t, c):
        stack = copy.deepcopy(t.stack)
        c.stack.append({"?":"TEST!", "STACK":t.stack})
        t.stack = stack

    @staticmethod ### -> ###
    def word_minus_rangle(e, t, c):
        block = c.stack[-1]
        block["HAVE"] = t.stack[len(block["STACK"]):]
        t.stack = copy.deepcopy(block["STACK"])

    @staticmethod ### }T ###
    def word_rbrace_T(e, t, c):
        block = c.stack.pop()
        block["NEED"] = t.stack[len(block["STACK"]):]
        if block["HAVE"] == block["NEED"]:
            t.p_count += 1
        else:
            t.f_count += 1
            have = repr(block["HAVE"])
            need = repr(block["NEED"])
            line = t.lines.get(t.line, "")
            print(f"INCORRECT RESULT: {have} ~= {need} {line}")

        t.stack = block["STACK"]


    @staticmethod ### <TRUE> ###
    def word_langle_TRUE_rangle__R_b(e, t, c):
        return (True,)

    @staticmethod ### <FALSE> ###
    def word_langle_FALSE_rangle__R_b(e, t, c):
        "T{ <FALSE> -> <FALSE> }T"
        return (False,)


    @staticmethod ### <NONE> ###
    def word_langle_NONE_rangle__R_b(e, t, c):
        return (None,)

    @staticmethod ### <NULL> ###
    def word_langle_NULL_rangle__R_b(e, t, c):
        return (None,)

    @staticmethod ### <NIL> ###
    def word_langle_NULL_rangle__R_b(e, t, c):
        return (None,)


    @staticmethod ### DECIMAL ###
    def word_DECIMAL__R(e, t, c):
        pass

    @staticmethod ### HEX ###
    def word_HEX__R(e, t, c):
        pass


    @staticmethod ### TESTING ###
    def word_TESTING__R(e, t, c):
        c.stack.append({"?":"TESTING", "LINE":t.line, "r":t.state})
        t.state = e.NUCLEUS.state_TESTING

    @staticmethod
    def state_TESTING(e, t, c, token):
        struct = c.stack[-1]
        if t.line == struct["LINE"]:
            print(token, end=" ")
            return

        c.stack.pop()
        t.state = struct["r"]
        t.state(e, t, c, token)


    @staticmethod ### = ###
    def word_equal__R_b(e, t, c, x1, x2):
        """
        T{  0  0 = -> <TRUE>  }T
        T{  1  1 = -> <TRUE>  }T
        T{ -1 -1 = -> <TRUE>  }T
        T{  1  0 = -> <FALSE> }T
        T{ -1  0 = -> <FALSE> }T
        T{  0  1 = -> <FALSE> }T
        T{  0 -1 = -> <FALSE> }T
        """
        return (x1 == x2,)

    @staticmethod ### < ###
    def word_langle__R_b(e, t, c, x1, x2):
        return (x1 < x2,)

    @staticmethod ### U< ###
    def word_U_langle__R_b(e, t, c, u1, u2):
        return (u1 < u2,)

    @staticmethod ### <= ###
    def word_langle_equal__R_b(e, t, c, x1, x2):
        return (x1 <= x2,)

    @staticmethod ### > ###
    def word_rangle__R_b(e, t, c, x1, x2):
        return (x1 > x2,)

    @staticmethod ### U> ###
    def word_rangle__R_b(e, t, c, u1, u2):
        return (u1 > u2,)

    @staticmethod ### >= ###
    def word_rangle_equal__R_b(e, t, c, x1, x2):
        return (x1 >= x2,)

    @staticmethod ### <> ###
    def word_langle_rangle__R_b(e, t, c, x1, x2):
        return (x1 != x2,)

    @staticmethod ### ~= ###
    def word_tilde_equal__R_b(e, t, c, x1, x2):
        return (x1 != x2,)

    @staticmethod ### != ###
    def word_bang_equal__R_b(e, t, c, x1, x2):
        return (x1 != x2,)



    @staticmethod ### 0= ###
    def word_0_equal__R_b(e, t, c, x):
        """
        T{ 0 0= -> <true> }T
        T{ 0.0 0= -> <true> }T
        T{ 0.0j 0= -> <true> }T
        """
        return (x == 0,)

    @staticmethod ### 0< ###
    def word_0_langle__R_b(e, t, c, x):
        return (x < 0,)

    @staticmethod ### 0> ###
    def word_0_rangle__R_b(e, t, c, x):
        return (x > 0,)



    @staticmethod ### ." ###
    def word_dot_dquote(e, t, c):
        c.stack.append({"m":"DOT_QUOTE", "PARTS":[]})
        t.state = e.NUCLEUS.state_dot_dquote

    @staticmethod
    def state_dot_dquote(e, t, c, token):
        end = token[-1] == '"'
        token = token[:-1] if end else token

        block = c.stack[-1]
        block["PARTS"].append(token)

        if end:
            print(" ".join(block["PARTS"]), end="")
            c.stack.pop()
            t.state = e.state_INTERPRET
            return

        t.state = e.NUCLEUS.state_dot_dquote

    @staticmethod ### : ###
    def word_colon(e, t, c):
        c.stack.append({"m":"COMPILE", "NAME":None, "...":[], "#":None})
        t.state = e.NUCLEUS.state_COMPILE_NAME

    @staticmethod ### ; ###
    def word_semicolon(e, t, c):
        e.raise_SyntaxError(";: error(-0): Free Standing ; Illegal")

    @staticmethod
    def state_COMPILE_NAME(e, t, c, token):
        block = c.stack[-1]
        if token == ";": # This is a no-op for : ;
            c.stack.pop()
            t.state = e.state_INTERPRET
            return

        block["NAME"] = token.upper()
        t.state = e.NUCLEUS.state_COMPILE_TOKENS

    @staticmethod
    def state_COMPILE_TOKENS(e, t, c, token):
        block = c.stack[-1]
        if token == ";":
            c.stack.pop()
            name = block["NAME"]
            tokens = block["..."]
            if len(tokens) == 0:
                del t.words[name]
            else:
                t.words[name] = tokens

            t.state = e.state_INTERPRET
            return

        if token == "#" or token == "\\":
            block["#"] = t.line
            return

        if block["#"]:
            if block["#"] == t.line:
                return
            block["#"] = None

        block["..."].append(token)

        t.state = e.NUCLEUS.state_COMPILE_TOKENS



    @staticmethod ### ! ###
    def word_bang__M__R(e, t, c, x, a):
        ""

        if isinstance(a, int) and a >= 1_000_000:
            if not t.is_root:
                e.raise_RuntimeError("!: error(-1): Illegal Memory Access")

        t.memory[a] = x


    @staticmethod ### @ ###
    def word_at__R_x(e, t, c, a):
        t.stack.append(t.memory.get(a,0))


    @staticmethod ### @NONE ###
    def word_at_NONE__R_x(e, t, c, a):
        t.stack.append(t.memory.get(a,None))


    @staticmethod ### VALUE ### ( x "<spaces>name" -- )
    def word_VALUE__R(e, t, c, x):
        """
        T{  111 VALUE v1 -> }T
        T{ -999 VALUE v2 -> }T
        T{ v1 ->  111 }T
        T{ v2 -> -999 }T
        """
        c.stack.append({"?":"VALUE", "x":x})
        t.state = e.NUCLEUS.state_VALUE

    @staticmethod
    def state_VALUE(e, t, c, token):
        struct = c.stack.pop()
        assert struct["?"] == "VALUE"
        t.words[token.upper()] = [(struct["x"],),]
        t.state = e.state_INTERPRET



    @staticmethod ### LOCALS| ###
    def word_LOCALS_pipe__R(e, t, c):
        """
        """
        c.stack.append({"?":"LOCALS|"})
        t.state = e.NUCLEUS.state_LOCALS_pipe

    @staticmethod
    def state_LOCALS_pipe(e, t, c, token):
        if token == "|":
            struct = c.stack.pop()
            assert struct["?"] == "LOCALS|"
            t.state = e.state_INTERPRET
            return

        t.words[token.upper()] = [(t.stack.pop(),),]
        t.state = e.NUCLEUS.state_LOCALS_pipe




    @staticmethod ### TO ### ( x "<spaces>name" -- )
    def word_TO__R(e, t, c, x):
        """
        T{ 111 VALUE v1 ->     }T
        T{ 222 TO v1    ->     }T
        T{ v1           -> 222 }T
        T{ : vd1 v1 ;   ->     }T
        T{ vd1          -> 222 }T
        """
        c.stack.append({"?":"TO", "x":x})
        t.state = e.NUCLEUS.state_TO

    @staticmethod
    def state_TO(e, t, c, token):
        block = c.stack.pop()
        assert block["?"] == "TO"
        t.words[token.upper()] = [(block["x"],),]
        t.state = e.state_INTERPRET



    @staticmethod ### CONSTANT ###
    def word_CONSTANT__R(e, t, c, x):
        """
        T{ 123 CONSTANT X123 ->     }T
        T{ X123              -> 123 }T
        T{ : EQU CONSTANT ;  ->     }T
        T{ X123 EQU Y123     ->     }T
        T{ Y123              -> 123 }T
        """
        c.stack.append(x)
        t.state = e.NUCLEUS.state_CONSTANT

    @staticmethod
    def state_CONSTANT(e, t, c, token):
        t.words[token.upper()] = [c.stack.pop()]
        t.state = e.state_INTERPRET


    @staticmethod ### VARIABLE ###
    def word_VARIABLE__R_a(e, t, c):
        """
        T{ VARIABLE V1 ->     }T
        T{    123 V1 ! ->     }T
        T{        V1 @ -> 123 }T
        """
        t.state = e.NUCLEUS.state_VARIABLE

    @staticmethod
    def state_VARIABLE(e, t, c, token):
        t.words[token.upper()] = [t.here]
        t.here +=1
        t.state = e.state_INTERPRET




    @staticmethod ### ' ###
    def sigil_squote(e, t, c, token, start=False):
        end = token[-1] == "'"
        if end:
            token = token[:-1]
        if start:
            token = token[1:]

        t.stack.append(" ".join(token.split(t.squote_space)))
        t.state = e.state_INTERPRET


    @staticmethod ### 1+ ###
    def word_1_plus__R_n2(e, t, c, n1):
        return (n1 + 1,)

    @staticmethod ### 1- ###
    def word_1_minus__R_n2(e, t, c, n1):
        return (n1 - 1,)

    @staticmethod ### 2+ ###
    def word_2_plus__R_n2(e, t, c, n1):
        return (n1 + 2,)

    @staticmethod ### 2- ###
    def word_2_minus__R_n2(e, t, c, n1):
        return (n1 - 2,)


    @staticmethod ### CREATE ###
    def word_CREATE__R(e, t, c):
        t.state = e.NUCLEUS.static_CREATE

    @staticmethod
    def static_CREATE(e, t, c, token):
        t.words[token.upper()] = [(t.here,),]
        t.state = e.state_INTERPRET

    @staticmethod ### HERE ###
    def word_HERE__R_a(e, t, c):
        """
        """
        return (t.here,)

    @staticmethod ### CELLS ###
    def word_CELLS__R_n2(e, t, c, n1):
        """
        T{ 1 CELLS 1 <         -> <FALSE> }T
        """
        return (n1,)

    @staticmethod ### CHARS ###
    def word_CHARS__R_n2(e, t, c, n1):
        """
        """
        return (n1,)


    @staticmethod ### ALLOT ###
    def word_ALLOT__R(e, t, c, n):
        t.here = t.here + n


    @staticmethod ### , ###
    def word_comma__R(e, t, c, x):
        t.memory[t.here] = x
        t.here += 1



import copy


