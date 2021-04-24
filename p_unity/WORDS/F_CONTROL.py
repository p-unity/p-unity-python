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

    : TEST1 IF 123 ELSE EXIT THEN 345 :

    T{ 0 TEST1 -> }T
    T{ 1 TEST1 -> 123 345 }T


    # if(0) {
    # } else {
    # }

    """

    def __init__(self, e, **kwargs):
        pass

    @staticmethod ### EXIT ###
    def word_EXIT__R(e, t, c):
        c.EXIT = True

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











