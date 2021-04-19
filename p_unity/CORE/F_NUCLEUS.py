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
    def sigil_lbracket(e, t, c, token, start=False):
        end = token[-1] == ")"
        if end:
            t.state = e.state_INTERPRET
            return

        t.state = e.NUCLEUS.sigil_lbracket


    @staticmethod ### ." ###
    def sigil_dot_dquote(e, t, c, token, start=False):
        end = token[-1] == '"'
        token = token[:-1] if end else token
        token = token[2:] if start else token

        if not start:
            print(" ", end="")

        print(token, end="")

        if end:
            t.state = e.state_INTERPRET
            return

        t.state = e.NUCLEUS.sigil_dot_dquote


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
            tokens = block["TOKENS"]
            if len(tokens) == 0:
                del t.words[name]
            else:
                t.words[name] = tokens

            t.state = e.state_INTERPRET
            return

        block["TOKENS"].append(token)

        t.state = e.NUCLEUS.state_COMPILE_TOKENS

    @staticmethod ### ; ###
    def word_semicolon(e, t, c):
        e.raise_SyntaxError(";: error(-0): Free Standing ; Illegal")

    @staticmethod ### : ###
    def word_colon(e, t, c):
        c.stack.append({"m":"COMPILE", "NAME":None, "TOKENS":[]})
        t.state = e.NUCLEUS.state_COMPILE_NAME


    @staticmethod ### WORDS ###
    def word_WORDS(e, t, c):
        words = {}
        for name in e.root.words.keys():
            words[name] = True
        for name in t.words.keys():
            words[name] = True
        for name in e.root.sigils.keys():
            words[name] = True
        for name in t.sigils.keys():
            words[name] = True
        words = sorted(words)
        print(" ".join(words))


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

    @staticmethod ### HERE ###
    def word_HERE__R_a(e, t, c):
        return (t.here,)

    @staticmethod ### ALLOT ###
    def word_ALLOT__R(e, t, c, n):
        t.here = t.here + n

    @staticmethod ### <TRUE> ###
    def word_langle_TRUE_rangle__R_b(e, t, c):
        return (True,)

    @staticmethod ### <FALSE> ###
    def word_langle_FALSE_rangle__R_b(e, t, c):
        return (False,)




