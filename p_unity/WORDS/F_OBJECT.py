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

    """

    -2 VALUE foo
    'ABCDE VALUE bar
    ([1,2,3]) VALUE List1

    T{ LIST1 2 -        -> ([1,3])         }T
    T{ LIST1            -> ([ 1 , 2 , 3 ]) }T
    T{ 'Hello [ foo : ] -> 'lo             }T
    T{ LIST1 [ foo ]    -> 2               }T
    T{ BAR [ 1 : 3 ]    -> 'BC             }T

    LIST1 99 !

    T{ 99 *LEN          -> 3               }T
    T{ 99 *[ -1 ]       -> 3               }T

    """

    def __init__(self, e, **kwargs):
        pass


    @staticmethod ### LEN ###
    def word_LEN__R_x_n(e, t, c, x):
        "T{ 'Hello'World' LEN -> 11 }T"
        return (len(x),)

    @staticmethod ### *LEN ###
    def word_times_LEN__R_n(e, t, c, a):
        ""
        return (len(t.memory[a]),)


    @staticmethod ### ~ ###
    def word_tilde__R_b(e, t, c, x):
        return (not x,)

    @staticmethod ### *~ ###
    def word_times_tilde__R_b(e, t, c, a):
        return (not t.memory[a],)


    @staticmethod ### [ ###
    def word_lbrack__R(e, t, c):
        struct = {"?":"[", ".len":len(t.stack), "r":t.state}
        struct[" : "] = e.OBJECT.state_do_slice
        struct[" , "] = e.OBJECT.state_make_list
        c.stack.append(struct)

    @staticmethod ### *[ ###
    def word_times_lbrack__R(e, t, c, a):
        struct = {"?":"[", ".len":len(t.stack), "a":a, "r":t.state}
        struct[" : "] = e.OBJECT.state_do_slice
        struct[" , "] = e.OBJECT.state_make_list
        c.stack.append(struct)

    @staticmethod
    def state_do_slice(e, t, c):
        struct = c.stack[-1]
        assert struct["?"] == "["
        struct[2] = t.stack[struct[".len"]:]
        t.stack = t.stack[:struct[".len"]]

    @staticmethod
    def state_make_list(e, t, c):
        struct = c.stack[-1]
        assert struct["?"] == "["
        struct[0] = struct.get(0, [])
        struct[0].extend(t.stack[struct[".len"]:])
        struct[0].append(struct[" x "])
        t.stack = t.stack[:struct[".len"]]

    @staticmethod ### ] ###
    def word_rbrack__R_x(e, t, c):
        struct = c.stack.pop()
        assert struct["?"] == "["

        if 0 in struct:
            struct[0].extend(t.stack[struct[".len"]:])
            t.stack = t.stack[:struct[".len"]]
            t.stack.append(struct[0])
            return

        struct_1 = t.stack[struct[".len"]:]
        t.stack = t.stack[:struct[".len"]]

        if "a" in struct:
            obj = t.memory[struct["a"]]
        else:
            obj = t.stack.pop()

        if 2 in struct:
            struct_2 = struct[2]

            if len(struct_2):
                if len(struct_1):
                    t.stack.append(obj[struct_2[-1]:struct_1[-1]])
                else:
                    t.stack.append(obj[struct_2[-1]:])
            else:
                if len(struct_1):
                    t.stack.append(obj[:struct_1[-1]])
                else:
                    t.stack.append(obj[:])
        else:

            if len(struct_1):
                index_1 = struct_1[-1]
                # index_1 = index_1 if isinstance(index_1, str) else int(index_1)
                t.stack.append(obj[index_1])
            else:
                e.raise_SyntaxError("[ ] Is Illegal")



    @staticmethod ### (. ###
    def sigil_lparen_dot(e, t, c, token, start=False):
        end = token[-1] == ")"
        if end:
            token = token[:-1]

        start = True if t.state == e.state_INTERPRET else False
        if start:
            token = token[2:]
            struct = {"?":"()", ".":token, "*":[], "**":{}, "r":t.state}
            c.stack.append(struct)
            t.state = e.OBJECT.sigil_lparen_dot
        else:
            struct = c.stack[-1]

        if end:
            c.stack.pop()

            obj = t.stack[-1]
            code = getattr(obj, struct["."])
            args = tuple(struct["*"])
            kwargs = struct["**"]
            result = code(*args, **kwargs)
            if isinstance(result, tuple):
                t.stack.extend(result)
            else:
                t.stack.append(result)

            t.state = struct["r"]
            return


