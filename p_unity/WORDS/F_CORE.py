#!/usr/bin/env python3
# -*- encoding: utf-8


__banner__ = r""" ( Copyright Intermine.com.au Pty Ltd. or its affiliates.
                    License SPDX: Programming-Unity-10.42 or as negotiated.

     _       _____    ____    _____    ______
  /\| |/\   / ____|  / __ \  |  __ \  |  ____|
  \ ` ' /  | |      | |  | | | |__) | | |__
 |_     _| | |      | |  | | |  _  /  |  __|
  / , . \  | |____  | |__| | | | \ \  | |____
  \/|_|\/   \_____|  \____/  |_|  \_\ |______|



)
# : ; ' ." ! @ @NONE CREATE HERE ALLOT
# VARIABLE CONSTANT VALUE TO LOCALS| |
# 1+ 1- 2+ 2- <TRUE> <FALSE>


""" # __banner__

class LIB: # { CORE : words }

    def __init__(self, e, **kwargs):
        e.tests_1.append(__tests_1__)

    @staticmethod ### ( ###
    def sigil_lparen(e, t, c, token, start=False):
        end = token[-1] == ")"
        if end:
            t.state = e.state_INTERPRET
            return

        t.state = LIB.sigil_lparen

    @staticmethod ### \ ###
    def sigil_slash(e, t, c, token, start=False):
        c.stack.append({"?":"SLASH", "LINE":t.line, "r":t.state})
        t.state = LIB.state_slash

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
        assert block["?"] == "TEST"

        have = block["HAVE"]
        need = t.stack[len(block["STACK"]):]
        t.stack = block["STACK"]

        if need == have:
            t.p_count += 1
            return

        line = t.lines.get(t.line, "")

        if not len(need) == len(have):
            t.f_count += 1
            print(f"WRONG NUMBER OF RESULTS: {have} ~= {need} {line}")
            return

        equal = True
        for i in range(0, len(need)):
            if isinstance(need[i], bool):
                if need[i]:
                    equal = True if have[i] else False
                else:
                    equal = True if not have[i] else False
            elif isinstance(have[i], bool):
                if have[i]:
                    equal = True if need[i] else False
                else:
                    equal = True if not need[i] else False
            else:
                equal = need[i] == have[i]

            if not equal:
                break

        if not equal:
            t.f_count += 1
            print(f"INCORRECT RESULT: {have} ~= {need} {line}")


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
    def word_langle_NIL_rangle__R_b(e, t, c):
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
        t.state = LIB.state_TESTING

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
    def word_dot_quote(e, t, c):
        c.stack.append({"m":"DOT_QUOTE", "PARTS":[]})
        t.state = LIB.state_dot_quote

    @staticmethod
    def state_dot_quote(e, t, c, token):
        end = token[-1] == '"'
        token = token[:-1] if end else token

        block = c.stack[-1]
        block["PARTS"].append(token)

        if end:
            print(" ".join(block["PARTS"]), end="")
            c.stack.pop()
            t.state = e.state_INTERPRET
            return

        t.state = LIB.state_dot_quote


    @staticmethod ### : ###
    def word_colon(e, t, c):
        call = c
        while call:
            for index in range(-1, (len(call.stack) * -1) - 1, -1):
                if " : " in call.stack[index]:
                    call.stack[index][" : "](e, t, call)
                    return
            call = call.parent

        c.stack.append({"?":":", 0:0})
        t.state = LIB.state_COMPILE

    @staticmethod ### :NONAME ###
    def word_colon_NONAME__R(e, t, c):
        c.stack.append({"?":":", 0:1, 1:[], "=":""})
        t.state = LIB.state_COMPILE

    @staticmethod ### IM... ###
    def word_IM_dot_dot_dot__R(e, t, c):
        LIB.word_IMMEDIATE__R(e, t, c)

    @staticmethod ### IMMEDIATE ###
    def word_IMMEDIATE__R(e, t, c):
        t.word_IMMEDIATE[t.last_compile] = True

    @staticmethod ### LITERAL ###
    def word_LITERAL__IR(e, t, c):
        """
        : TEN I[ 5 5 + ]I LITERAL ;
        T{ TEN -> 10 }T
        """
        assert t.state == LIB.state_COMPILE
        block = c.stack[-1]
        block[1].append(t.stack.pop())

    @staticmethod ### STATE ###
    def word_STATE__R_b(e, t, c):
        return (t.state == e.state_INTERPRET,)

    @staticmethod ### I[ ###
    def word_I_lbrack__IR(e, t, c):
        c.stack.append({"?":"[[", "r":t.state})
        t.state = e.state_INTERPRET

    @staticmethod ### ]I ###
    def word_rbrack_I__R(e, t, c):
        struct = c.stack.pop()
        assert struct["?"] == "[["
        t.state = struct["r"]

    @staticmethod ### CREATE ###
    def word_CREATE__R(e, t, c):
        """
        T{ CREATE CR1 -> }T
        T{ CR1   -> HERE }T

        T{ : FOO CREATE ; -> }T
        T{ FOO BAR -> }T
        T{ BAR -> HERE }T

        """
        t.last_create = c.tokens.pop(0)
        t.words[t.last_create] = (t.here,)


    @staticmethod ### DOES> ###
    def word_DOES_rangle__IR(e, t, c):
        struct = c.stack[-1]
        if not t.state == LIB.state_COMPILE:
            e.raise_SyntaxError("DOES>: error (-0): Not Valid Outside :")
        if not struct[0] == 1:
            e.raise_SyntaxError("DOES>: error (-0): Only 1 DOES> Allowed")
        if struct["="] == "":
            e.raise_SyntaxError("DOES>: error (-0): Not Valid in :NONAME")

        struct[0] = 2
        struct[2] = []

    @staticmethod ### ; ###
    def word_semicolon__IR(e, t, c):
        block = c.stack.pop()
        if "=" in block:
            if block["="] == "":
                t.stack.append(block[1])
            else:
                t.words[block["="]] = block[1]
                if 2 in block:
                    t.word_DOES[block["="]] = block[2]

        t.state = e.state_INTERPRET

    @staticmethod
    def state_COMPILE(e, t, c, token):
        token_u = token.upper() if isinstance(token, str) else token
        if token_u in t.word_IMMEDIATE or token_u in e.root.word_IMMEDIATE:
            return e.run(e, t, c, token_u)

        block = c.stack[-1]
        if block[0] == 0:
            block[0] = 1
            block[1] = []
            block["="] = token_u
            t.last_compile = token_u
            return

        if token == "#" or token == "\\":
            block["#"] = t.line
            return

        if "#" in block:
            if block["#"] == t.line:
                return
            del block["#"]

        is_number, value = e.to_number(e, t, c, token)
        if is_number:
            block[block[0]].append(value)
        else:
            block[block[0]].append(token)


    @staticmethod ### CHAR+ ###
    def word_CHAR_plus__R_a2(e, t, c, a1):
        return (a1 + 1,)

    @staticmethod ### ! ###
    def word_bang__R(e, t, c, x, a):
        ""
        if isinstance(a, int) and a >= 1_000_000:
            if not t.is_root:
                e.raise_RuntimeError("!: error(-1): Illegal Memory Access")

        t.memory[a] = x

    @staticmethod ### C! ###
    def word_C_bang__M__R(e, t, c, x, a):
        ""
        if isinstance(a, int) and a >= 1_000_000:
            if not t.is_root:
                e.raise_RuntimeError("!: error(-1): Illegal Memory Access")

        t.memory[a] = x



    @staticmethod ### 2! ###
    def word_2_bang__M__R(e, t, c, x1, x2, a):
        ""
        if isinstance(a, int) and a >= 1_000_000:
            if not t.is_root:
                e.raise_RuntimeError("!: error(-1): Illegal Memory Access")

        t.memory[a] = x1
        t.memory[a+1] = x2

    @staticmethod ### @ ###
    def word_at__R_x(e, t, c, a):
        t.stack.append(t.memory.get(a,0))

    @staticmethod ### @NONE ###
    def word_at_NONE__R_x(e, t, c, a):
        t.stack.append(t.memory.get(a,None))

    @staticmethod ### C@ ###
    def word_C_at__R_x(e, t, c, a):
        t.stack.append(t.memory.get(a,0))

    @staticmethod ### 2@ ###
    def word_2_at__R_x(e, t, c, a):
        t.stack.append(t.memory.get(a,0))
        t.stack.append(t.memory.get(a+1,0))


    @staticmethod ### VALUE ### ( x "<spaces>name" -- )
    def word_VALUE__R(e, t, c, x):
        """
        T{  111 VALUE v1 -> }T
        T{ -999 VALUE v2 -> }T
        T{ v1 ->  111 }T
        T{ v2 -> -999 }T
        """
        c.stack.append({"?":"VALUE", "x":x})
        t.state = LIB.state_VALUE

    @staticmethod
    def state_VALUE(e, t, c, token):
        struct = c.stack.pop()
        assert struct["?"] == "VALUE"
        t.words[token.upper()] = (struct["x"],)
        t.state = e.state_INTERPRET



    @staticmethod ### LOCALS| ###
    def word_LOCALS_pipe__R(e, t, c):
        """
        """
        c.stack.append({"?":"LOCALS|"})
        t.state = LIB.state_LOCALS_pipe

    @staticmethod
    def state_LOCALS_pipe(e, t, c, token):
        if token == "|":
            struct = c.stack.pop()
            assert struct["?"] == "LOCALS|"
            t.state = e.state_INTERPRET
            return

        t.words[token.upper()] = (t.stack.pop(),)
        t.state = LIB.state_LOCALS_pipe




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
        t.state = LIB.state_TO

    @staticmethod
    def state_TO(e, t, c, token):
        struct = c.stack.pop()
        assert struct["?"] == "TO"
        t.words[token.upper()] = (struct["x"],)
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
        t.state = LIB.state_CONSTANT

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
        t.state = LIB.state_VARIABLE

    @staticmethod
    def state_VARIABLE(e, t, c, token):
        t.words[token.upper()] = [t.here]
        t.here +=1
        t.state = e.state_INTERPRET




    @staticmethod ### ' ###
    def sigil_tick(e, t, c, token, start=False):
        end = token[-1] == "'"
        if end:
            token = token[:-1]
        if start:
            token = token[1:]

        t.stack.append(" ".join(token.split(t.tick_space)))
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


    @staticmethod ### CELL+ ###
    def word_CELL_plus__R_a2(e, t, c, a1):
        """
        """
        return (a1 + 1,)

    @staticmethod ### ALIGNED ###
    def word_ALIGNED__R_a2(e, t, c, a1):
        """
        """
        return (a1,)

    @staticmethod ### ALIGN ###
    def word_ALIGN__R_a2(e, t, c):
        """
        """
        pass

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


    @staticmethod ### C, ###
    def word_C_comma__R(e, t, c, x):
        t.memory[t.here] = x
        t.here += 1


    @staticmethod ### , ###
    def word_comma__R(e, t, c, x):

        for index in range(-1, (len(c.stack) * -1) - 1, -1):
            if " , " in c.stack[index]:
                c.stack[index][" x "] = x
                c.stack[index][" , "](e, t, c)
                return

        t.memory[t.here] = x
        t.here += 1

    @staticmethod ### ,, ###
    def word_comma_comma__R(e, t, c, x):
        t.memory[t.here] = x
        t.here += 1



    @staticmethod ### ' ###
    def word_tick__R_x(e, t, c):
        t.state = LIB.state_tick

    @staticmethod
    def state_tick(e, t, c, token):
        token_u = token.upper() if isinstance(token, str) else str

        if token_u in t.words:
            xt = t.words[token_u]
        else:
            xt = e.root.words[token_u]

        t.stack.append(xt)

        t.state = e.state_INTERPRET

    @staticmethod ### EXECUTE ###
    def word_EXECUTE__R(e, t, c):
        e.execute_tokens(e, t, c, t.stack.pop())


import copy

__tests_1__ = """

0 999999 !

: TEN 10 ;

T{ TEN -> 10 }T

T{ : DOES1 DOES> @ 1 + ; -> }T
T{ : DOES2 DOES> @ 2 + ; -> }T
T{ CREATE CR1 -> }T
T{ CR1   -> HERE }T
T{ 1 ,   ->   }T
T{ CR1 @ -> 1 }T

    """

