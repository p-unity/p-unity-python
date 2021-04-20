#!/usr/bin/env python3
# -*- encoding: utf-8


__banner__ = r""" ( Copyright Intermine.com.au Pty Ltd. or its affiliates.
                    License SPDX: Programming-Unity-10.42 or as negotiated.

     _       ____    ____         _   ______    _____   _______
  /\| |/\   / __ \  |  _ \       | | |  ____|  / ____| |__   __|
  \ ` ' /  | |  | | | |_) |      | | | |__    | |         | |
 |_     _| | |  | | |  _ <   _   | | |  __|   | |         | |
  / , . \  | |__| | | |_) | | |__| | | |____  | |____     | |
  \/|_|\/   \____/  |____/   \____/  |______|  \_____|    |_|



)





""" # __banner__

class LIB: # { The Object ABI : words }

    def __init__(self, e, **kwargs):
        pass

    @staticmethod ### LEN ###
    def word_LEN__R_x_n(e, t, c, x):
        "T{ 'Hello'World' LEN NIP -> 11 }T"
        return (x, len(x),)

    @staticmethod ### ~ ###
    def word_tilde__R_x_b(e, t, c, x):
        return (x, not x,)

    @staticmethod ### [[ ###
    def word_lbracket_lbracket(e, t, c):
        c.stack.append(0)
        c.stack.append(None)
        c.stack.append(len(t.stack))

    @staticmethod ### :: ###
    def word_colon_colon(e, t, c):
        c.stack[-2] = t.stack[c.stack[-1]:]
        while len(t.stack) > t.stack[-1]:
            t.stack.pop()

    @staticmethod ### ]] ###
    def word_rparen_rparen__R_x(e, t, c):

        if c.stack[-3] == 0: # 0 is object on stack
            o = t.stack[c.stack[-1] - 1]

        if c.stack[-2] == None:
            if len(t.stack) == c.stack[-1]:
                raise e.raise_SyntaxError("[[ ]] Not Allowed")

            x = o[t.stack[-1]]
            while len(t.stack) > t.stack[-1]:
                t.stack.pop()
            return (x, )


    #@staticmethod ### (~. ###
    #def sigil_lparen_tilde_dot(e, t, c, token, start=False):
    #    return e.OBJECT.sigil_lparen_dot(e, t, c, token, start, invert=True)

    @staticmethod ### (. ###
    def sigil_lparen_dot(self, token, start=False):
        end = token[-1] == ")"
        if end:
            token = token[:-1]
        if start:
            token = token[1:]
            if invert:
                token = token[1:]
            self.call__ = [token[1:]]
            self.call_invert__ = invert

        if end:
            obj = self.stack[-1]
            code = getattr(obj, self.call__[0])
            args = self.call__[1:]
            result = code(*args)
            if result == None:
                pass
            elif isinstance(result, tuple):
                self.stack.extend(result)
            else:
                if self.call_invert__:
                    self.stack.append(not result)
                else:
                    self.stack.append(result)

            selt.state = self.INTERPRET
            return

        selt.state = self.CALL




