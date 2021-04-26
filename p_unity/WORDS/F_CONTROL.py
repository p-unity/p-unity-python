#!/usr/bin/env python3
# -*- encoding: utf-8


__banner__ = r""" ( Copyright Intermine.com.au Pty Ltd. or its affiliates.
                    License SPDX: Programming-Unity-10.42 or as negotiated.

     _       _____    ____    _   _   _______   _____     ____    _
  /\| |/\   / ____|  / __ \  | \ | | |__   __| |  __ \   / __ \  | |
  \ ` ' /  | |      | |  | | |  \| |    | |    | |__) | | |  | | | |
 |_     _| | |      | |  | | | . ` |    | |    |  _  /  | |  | | | |
  / , . \  | |____  | |__| | | |\  |    | |    | | \ \  | |__| | | |____
  \/|_|\/   \_____|  \____/  |_| \_|    |_|    |_|  \_\  \____/  |______|



)





""" # __banner__

class LIB: # { Control Flow : words }

    """

    T{  0 IF 123 THEN ->     }T
    T{ -1 IF 123 THEN -> 123 }T
    T{  1 IF 123 THEN -> 123 }T
    T{ -1 IF 123 THEN -> 123 }T
    T{  0 IF 123 ELSE 234 THEN -> 234 }T
    T{  1 IF 123 ELSE 234 THEN -> 123 }T

    : TEST1 IF 123 ELSE EXIT THEN 345 ;

    T{ 0 TEST1 -> }T
    T{ 1 TEST1 -> 123 345 }T

    # T{ : GD3 DO 1 0 DO J LOOP LOOP ; -> }T
    # T{          4        1 GD3 ->  1 2 3   }T

    : GD1 DO I LOOP ;

    T{ 5 1 GD1 -> 1 2 3 4 }T

    T{ 6 2 GD1 -> 2 3 4 5 }T

    """

    def __init__(self, e, **kwargs):
        pass

    @staticmethod ### EXIT ###
    def word_EXIT__R(e, t, c):
        c.EXIT = True

    @staticmethod ### V ###
    def word_V__R_x(e, t, c):
        call = c
        while call:
            for index in range(-1, (len(call.stack) * -1) - 1, -1):
                if "v" in call.stack[index]:
                    return (call.stack[index]["v"],)
            call = call.parent
        e.raise_RuntimeError("V: error (-0): Illegal Outside 'Object' DO")

    @staticmethod ### V^ ###
    def word_V_carat__R_x(e, t, c):
        call = c
        outer = False
        while call:
            for index in range(-1, (len(call.stack) * -1) - 1, -1):
                if "v" in call.stack[index]:
                    if not outer:
                        outer = True
                    else:
                        return (call.stack[index]["v"],)
            call = call.parent
        e.raise_RuntimeError("V^: error (-0): Illegal Outside 'Object' DO DO")

    @staticmethod ### K ###
    def word_K__R_x(e, t, c):
        call = c
        while call:
            for index in range(-1, (len(call.stack) * -1) - 1, -1):
                if "k" in call.stack[index]:
                    return (call.stack[index]["k"],)
            call = call.parent
        e.raise_RuntimeError("K: error (-0): Illegal Outside Object DO")

    @staticmethod ### K^ ###
    def word_K_carat__R_x(e, t, c):
        call = c
        outer = False
        while call:
            for index in range(-1, (len(call.stack) * -1) - 1, -1):
                if "k" in call.stack[index]:
                    if not outer:
                        outer = True
                    else:
                        return (call.stack[index]["k"],)
            call = call.parent
        e.raise_RuntimeError("K^: error (-0): Illegal Outside Object DO DO")

    @staticmethod ### I ###
    def word_I__R_n(e, t, c):
        call = c
        while call:
            for index in range(-1, (len(call.stack) * -1) - 1, -1):
                if "i2" in call.stack[index]:
                    return (call.stack[index]["i2"],)
            call = call.parent
        e.raise_RuntimeError("I: error (-0): Illegal Outside DO")

    @staticmethod ### J ###
    def word_J__R_n(e, t, c):
        call = c
        outer = False
        while call:
            for index in range(-1, (len(call.stack) * -1) - 1, -1):
                if "i2" in call.stack[index]:
                    if not outer:
                        outer = True
                    else:
                        return (call.stack[index]["i2"],)
            call = call.parent
        e.raise_RuntimeError("J: error (-0): Illegal Outside DO DO")

    @staticmethod ### DO ###
    def word_DO__R(e, t, c):
        struct = {"?":"DO", 1:[], "DO":0, "r":t.state}
        c.stack.append(struct)

        tos = t.stack.pop()
        if isinstance(tos, list) or isinstance(tos, dict):
            struct["iter"] = tos
        else:
            struct["i2"] = tos
            struct["i1"] = t.stack.pop()

        t.state = LIB.state_DO

    @staticmethod
    def state_DO(e, t, c, token):
        struct = c.stack[-1]
        assert struct["?"] == "DO"

        token_u = token.upper() if isinstance(token, str) else token

        if token_u == "LOOP" or token_u == "+LOOP":
            if struct["DO"] == 0:
                return LIB.impl_DO(e, t, c, token, struct)
            struct["DO"] -= 1

        if token_u == "DO":
            struct["DO"] += 1

        is_number, value = e.to_number(e, t, c, token)
        if is_number:
            struct[1].append((value,))
        else:
            struct[1].append(token)

    @staticmethod
    def impl_DO(e, t, c, token, struct):

        t.state = e.state_INTERPRET

        if "iter" in struct:
            if token == "+LOOP":
                e.raise_RuntimeError("LOOP+: error(-0): Only Valid on Integer Loops")

            iter = struct["iter"]
            if isinstance(iter, list):
                for v in iter:
                    struct["v"] = v
                    e.execute_tokens(e, t, c, struct[1])

            if isinstance(iter, dict):
                for k in sorted(iter):
                    struct["k"] = k
                    struct["v"] = iter[k]
                    e.execute_tokens(e, t, c, struct[1])

        else:

            while struct["i2"] < struct["i1"]:
                e.execute_tokens(e, t, c, struct[1])
                if token == "LOOP":
                    struct["i2"] += 1
                elif token == "+LOOP":
                    struct["i2"] += t.stack.pop()

        c.stack.pop()
        t.state = struct["r"]


    @staticmethod ### BEGIN ###
    def word_BEGIN(e, t, c):
        c.stack.append({"?":"BEGIN", "m":1, 1:[], 2:[], "r":t.state})
        t.state = e.CONTROL.state_BEGIN

    @staticmethod
    def impl_BEGIN(e, t, c, struct):

        if struct["m"] == 1:
            while True:
                t.state = e.state_INTERPRET
                e.execute_tokens(e, t, c, struct[1])
                b = t.stack.pop()
                if b:
                    break

        t.state = struct["r"]

    @staticmethod
    def state_BEGIN(e, t, c, token):
        struct = c.stack[-1]
        assert struct["?"] == "BEGIN"

        token_u = token.upper() if isinstance(token, str) else token
        if token_u == "UNTIL" or token_u == "REPEAT":
            return LIB.impl_BEGIN(e, t, c, struct)

        if token_u == "WHILE":
            struct["m"] = 2
            return

        struct[struct["m"]].append(token)

    @staticmethod ### REPEAT ###
    def word_REPEAT__R(e, t, c):
        e.raise_SyntaxError("REPEAT: error(-0): No BEGIN")

    @staticmethod ### UNTIL ###
    def word_UNTIL__R(e, t, c):
        e.raise_SyntaxError("UNTIL: error(-0): No BEGIN")

    @staticmethod ### WHILE ###
    def word_WHILE__R(e, t, c):
        e.raise_SyntaxError("WHILE: error(-0): No BEGIN")







    @staticmethod ### <.IF ###
    def word_langle_dot_IF__R(e, t, c, b):
        c = {"m":"<.IF", "b":b, "THEN.>":[], "ELSE.>":[], "r":f.state}
        c.fixme.append(c)
        t.state = f.langle_dot_IF

    @staticmethod ### THEN.> ###
    def word_THEN_dot_rangle__R(e, t, c):
        f.raise_SyntaxError("THEN.>: error(-0): Free Standing THEN.> Not Allowed")

    @staticmethod ### ELSE.> ###
    def word_ELSE_dot_rangle__R(e, t, c):
        f.raise_SyntaxError("ELSE.>: error(-0): Free Standing ELSE.> Not Allowed")

    @staticmethod ### IF. ###
    def word_IF_dot__R(e, t, c, free_standing=True):

        ""

        """
        T{ 0      <.IF THEN.> 'YES ELSE.> 'NO IF. -> 'NO }T
        T{ <true> <.IF THEN.> 'YES ELSE.> 'NO IF. -> 'YES }T
        """

        if free_standing:
            f.raise_SyntaxError("ELSE.>: error(-0): Free Standing IF. Not Allowed")

        c = c.fixme.pop()
        t.state = c["r"]
        if c["b"]:
           f.execute(c["THEN.>"])
        else:
           f.execute(c["ELSE.>"])



    @staticmethod
    def impl_IF(e, t, c):
        t.state = e.state_INTERPRET

        block = c.stack.pop()
        if block["b"]:
           e.execute_tokens(e, t, c, block[1])
        else:
           e.execute_tokens(e, t, c, block[0])

        t.state = block["r"]


    @staticmethod ### IF ###
    def word_IF__R(e, t, c, b):
        c.stack.append({"m":"IF", "b":b, 0:[], 1:[], "r":t.state})
        t.state = e.CONTROL.state_IF_TRUE


    @staticmethod
    def state_IF_TRUE(e, t, c, token):
        token_u = token.upper() if isinstance(token, str) else token

        if token_u == "ELSE":
            t.state = e.CONTROL.state_IF_FALSE
            return

        if token_u == "END_IF" or token_u == "THEN":
            e.CONTROL.impl_IF(e, t, c)
            return

        assert c.stack[-1]["m"] == "IF"

        is_number, value = e.to_number(e, t, c, token)
        if is_number:
            c.stack[-1][1].append((value,))
        else:
            c.stack[-1][1].append(token)

        t.state = e.CONTROL.state_IF_TRUE

    @staticmethod ### ELSE ###
    def word_ELSE__R(e, t, c, token):
        t.state = e.CONTROL.state_IF_FLASE

    @staticmethod
    def state_IF_FALSE(e, t, c, token):
        token_u = token.upper() if isinstance(token, str) else token

        if token_u == "ELSE":
            t.state = e.CONTROL.IF_TRUE
            return

        if token_u == "END_IF" or token_u == "THEN":
            e.CONTROL.impl_IF(e, t, c)
            return

        assert c.stack[-1]["m"] == "IF"

        is_number, value = e.to_number(e, t, c, token)
        if is_number:
            c.stack[-1][0].append((value,))
        else:
            c.stack[-1][0].append(token)

        t.state = e.CONTROL.state_IF_TRUE


    @staticmethod ### THEN ###
    def word_THEN__R(e, t, c):
        e.CONTROL.impl_IF(e, t, c)

    @staticmethod ### END_IF ###
    def word_END_IF__R(e, t, c):
        e.CONTROL.impl_IF(e, t, c)



#
#
#
#
#
#
#
#
#
#
#



r"""


    def langle_dot_IF(e, t, c, token):
        token_u = token.upper() if isinstance(token, str) else token

        if token_u == "THEN.>":
            t.state = f.THEN_dot_rangle
            return

        if token_u == "ELSE.>":
            t.state = f.ELSE_dot_rangle
            return

        if token_u == "IF.":
            f.CONTROL.word_IF_dot__R(e, t, c, free_standing=False)
            return

        raise ForthException("<.IF: error(-0): Words not allowed between <.IF and THEN.>")

    def THEN_dot_rangle(e, t, c, token):
        token_u = token.upper() if isinstance(token, str) else token

        if token_u == "THEN.>":
            raise ForthSyntaxException("THEN.>: error(-0): Nested THEN.> Not Allowed")

        if token_u == "ELSE.>":
            t.state = f.ELSE_dot_rangle
            return

        if token_u == "IF.":
            f.CONTROL.word_IF_dot__R(e, t, c, free_standing=False)
            return

        c.fixme[-1]["THEN.>"].append(token)
        t.state = f.THEN_dot_rangle

    def ELSE_dot_rangle(e, t, c, token):
        token_u = token.upper() if isinstance(token, str) else token

        if token_u == "THEN.>":
            raise ForthSyntaxException("THEN.>: error(-0): THEN.> Folling ELSE.> Not Allowed")

        if token_u == "ELSE.>":
            raise ForthSyntaxException("ELSE.>: error(-0): Nested ELSE.> Not Allowed")

        if token_u == "IF.":
            f.CONTROL.word_IF_dot__R(e, t, c, free_standing=False)
            return

        c.fixme[-1]["ELSE.>"].append(token)
        t.state = f.ELSE_dot_rangle



"""












