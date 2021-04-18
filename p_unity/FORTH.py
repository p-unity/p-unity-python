#!/usr/bin/env python3
# -*- encoding: utf-8


__banner__ = r""" ( Copyright Intermine.com.au Pty Ltd. or its affiliates.
                    License SPDX: Programming-Unity-10.42 or as negotiated.

      ______    ____    _____    _______   _    _   /\   ____
  _  |  ____|  / __ \  |  __ \  |__   __| | |  | | |/\| |___ \   _
 (_) | |__    | |  | | | |__) |    | |    | |__| |        __) | (_)
     |  __|   | |  | | |  _  /     | |    |  __  |       |__ <
  _  | |      | |__| | | | \ \     | |    | |  | |       ___) |  _
 (_) |_|       \____/  |_|  \_\    |_|    |_|  |_|      |____/  ( )
                                                                |/


)




"""  # __banner__


class Engine:  # { The Reference Implementation of FORTH^3 : p-unity }

    def __init__(self, run_tests=None, autoexec=None):

        self.run_tests = run_tests # None/0, 1=Sanity, 2=&Smoke

        self.g = {}

        self.state_stack = collections.deque()
        self.state_names = []

        self.here = 1_000_000
        self.state_names.append('here')

        self.memory = {}
        self.state_names.append('memory')

        self.sigils = {}
        self.state_names.append('sigils')

        self.words = {}
        self.words_argc = {}
        self.state_names.extend(['words', 'words_argc'])

        self.stack = []
        self.state_names.append('stack')

        self.cstack = []
        self.state_names.append('cstack')

        self.minus_gt = 0
        self.state_names.append('minus_gt')

        self.state = self.INTERPRET
        self.state_names.append('state')

        self.squote_space = "'"

        self.digits = {}
        for digit in "#$%-01234567890":
            self.digits[digit] = True

        self.__core__()

        self.TEST = F_TEST.LIB(self)
        self.add_words(self.TEST)

        self.NUCLEUS = F_NUCLEUS.LIB(self)
        self.add_words(self.NUCLEUS)

        self.DSTACK = F_DSTACK.LIB(self)
        self.add_words(self.DSTACK)

        self.CONTROL = F_CONTROL.LIB(self)
        self.add_words(self.CONTROL)

        self.REPL = F_REPL.LIB(self)
        self.add_words(self.REPL)

        self.IO = F_IO.LIB(self)
        self.add_words(self.IO)

        self.MATH = F_MATH.LIB(self)
        self.add_words(self.MATH)

        self.OBJECT = F_OBJECT.LIB(self)
        self.add_words(self.OBJECT)

        self.JSON = F_JSON.LIB(self)
        self.add_words(self.JSON)

        self.CURSES = F_CURSES.LIB(self)
        self.add_words(self.CURSES)

        if self.run_tests and self.run_tests >= 2:
            for line in __smoke_0__.split('\n'):
                self.execute(line.split())

        if autoexec:
            for line in autoexec.split('\n'):
                self.execute(line.split())

    __word_map = {

        "colon": ":", "semicolon": ";", "dot": ".", "comma": ",",
        "squote": "'", "dquote": '"', "btick": "`", "equal": "=",
        "under": "_", "tidlies": "~", "minus": "-", "plus": "+",
        "percent": "%", "carat": "^", "amper": "&", "times": "*",
        "bang": "!", "at": "@", "hash": "#", "dollar": "$",
        "lsquare": "[", "rsquare": "]", "lbrace": "{", "rbrace": "}",
        "lbracket": "(", "rbracket": ")", "langle": "<", "rangle": ">",
        "pipe": "|", "slash": "\\", "divide": "/", "qmark": "?",
        "unicorn": "\u1F984", "rainbow": "\u1F308",
        "astonished": "\u1F632"

    }

    def add_words(self, source):

        tests = []

        names = []
        for fname in dir(source):
            parts = fname.split('_')
            if len(parts) < 2 or not parts[0][:4] == 'word':
                continue
            word = getattr(source, fname)
            names.append((word.__code__.co_firstlineno, fname))

        names.sort()

        for order, fname in names:
            parts = fname.split('_')[1:]

            name = []
            for part in parts:
                if part == '': break
                if part[0].isupper() or part[0].isdigit():
                    name.append(part.upper())
                else:
                    name.append(self.__word_map[part])

            # __n1_n2 - the tail contains the return spec
            if not len(name) == len(parts):
                pass

            name = "".join(name)
            word = getattr(source, fname)

            #ic(name, fname)
            if name in self.words:
                raise ForthException(f"{name}: error(-4): Already defined")

            self.words[name] = word
            argc = word.__code__.co_argcount
            if argc > 1:
                self.words_argc[name] = argc - 1

            if self.run_tests and word.__doc__:
                for line in word.__doc__.split('\n'):
                    f_count = self.TEST.f_count
                    try:
                        self.execute(line.split())
                    except Exception as ex:
                        raise ex
                    if not f_count == self.TEST.f_count:
                        print(str(word))

        if self.run_tests and source.__doc__:
            for line in source.__doc__.split('\n'):
                f_count = self.TEST.f_count
                self.execute(line.split())
                if not f_count == self.TEST.f_count:
                    print(str(source))

        return tests

    def __core__(self):

        self.sigil("(", self.COMMENT)

        self.sigil(":", self.COMPILE)

        self.sigil("(.", self.CALL)
        self.sigil("(.~", self.CALL_NOT)
        self.word(".)", self.CALL_END, argc=0)

        self.sigil("'", self.SQUOTE)
        self.sigil('."', self.DOT_QUOTE)

        self.sigil("([", self.sJSON)
        self.sigil("({", self.sJSON)
        self.sigil("((", self.sJSON)
        self.sigil('("', self.sJSON)

    def to_number(self, token):
        base = 10
        if token[0] == '#':
            token = token[1:]
        elif token[0] == '$':
            base = 16
            token = token[1:]
        elif token[0] == '%':
            base = 2
            token = token[1:]

        if token[0] == '-':
            if len(token) == 1:
                return (False, None)
            if not token[1].isdigit():
                return (False, None)

        if 'J' in token:
            return (True, complex(token))
        else:
            if '.' in token:
                if base == 10:
                    return (True, Decimal(token))
                else:
                    return (True, Decimal(int(token, base)))
            else:
                return (True, int(token, base))

    def BEGIN(f, token):
        token_u = token.upper() if isinstance(token, str) else token

        if token_u == "REPEAT":
            f.CONTROL.word_REPEAT__R(f, free_standing=False)
            return

        f.cstack[-1]["TOKENS"].append(token)
        f.state = f.BEGIN


    def IF(f, token):
        token_u = token.upper() if isinstance(token, str) else token

        if token_u == "ELSE":
            f.state = f.ELSE
            return

        if token_u == "END_IF" or token_u == "THEN":
            f.CONTROL.word_END_IF__R(f)
            f.state = f.INTERPRET
            return

        f.cstack[-1]["IF"].append(token)
        f.state = f.IF

    def langle_dot_IF(f, token):
        token_u = token.upper() if isinstance(token, str) else token

        if token_u == "THEN.>":
            f.state = f.THEN_dot_rangle
            return

        if token_u == "ELSE.>":
            f.state = f.ELSE_dot_rangle
            return

        if token_u == "IF.":
            f.CONTROL.word_IF_dot__R(f, free_standing=False)
            return

        raise ForthException("<.IF: error(-0): Words not allowed between <.IF and THEN.>")

    def THEN_dot_rangle(f, token):
        token_u = token.upper() if isinstance(token, str) else token

        if token_u == "THEN.>":
            raise ForthSyntaxException("THEN.>: error(-0): Nested THEN.> Not Allowed")

        if token_u == "ELSE.>":
            f.state = f.ELSE_dot_rangle
            return

        if token_u == "IF.":
            f.CONTROL.word_IF_dot__R(f, free_standing=False)
            return

        f.cstack[-1]["THEN.>"].append(token)
        f.state = f.THEN_dot_rangle

    def ELSE_dot_rangle(f, token):
        token_u = token.upper() if isinstance(token, str) else token

        if token_u == "THEN.>":
            raise ForthSyntaxException("THEN.>: error(-0): THEN.> Folling ELSE.> Not Allowed")

        if token_u == "ELSE.>":
            raise ForthSyntaxException("ELSE.>: error(-0): Nested ELSE.> Not Allowed")

        if token_u == "IF.":
            f.CONTROL.word_IF_dot__R(f, free_standing=False)
            return

        f.cstack[-1]["ELSE.>"].append(token)
        f.state = f.ELSE_dot_rangle



    def ELSE(f, token):
        token_u = token.upper() if isinstance(token, str) else token

        if token_u == "ELSE":
            f.state = f.IF
            return

        if token_u == "END_IF" or token_u == "THEN":
            f.CONTROL.word_END_IF__R(f)
            f.state = f.INTERPRET
            return

        f.cstack[-1]["ELSE"].append(token)
        f.state = f.ELSE

    def INTERPRET(self, token):

        if not isinstance(token, str):
            if isinstance(token, tuple):
                self.stack.append(token[0])
            else:
                self.stack.append(token)
            return

        for sigil_len in [5, 4, 3, 2, 1]:
            sigil = token[:sigil_len].upper()
            if sigil in self.sigils:
                self.sigils[sigil](token, start=True)
                return

        token_u = token.upper()

        if not token_u in self.words and token[0] in self.digits:
            is_number, value = self.to_number(token_u)
            if is_number:
                self.stack.append(value)
                return

        if not token_u in self.words:
            details = f"{token}: error(-13): word not found"
            raise ForthException(details)

        code = self.words[token_u]
        if isinstance(code, list):
            self.execute(code)
            return

        if callable(code):

            args = []
            argc = self.words_argc.get(token_u, 0)

            if argc > len(self.stack):
                details = f"{token}: error(-4): stack underflow"
                raise ForthException(details)

            if argc > 0:
                self.stack, args = self.stack[:-argc], self.stack[-argc:]

            self.stack.extend(code(self, *args) or tuple())

        else:

            self.stack.append(code)

    def COMPILE(self, token, start=False):
        end = token[-1] == ';'
        if end:
            token = token[:-1]
        if start:
            token = token[1:]
            self.compile__ = []
            self.compile_name__ = None

        if token == ":":
            raise ForthException(':: error (-1): compile in compile')

        if not self.compile_name__:
            if not token == '':
                self.compile_name__ = token.upper()
        else:
            if len(token):
                token_upper = token.upper()
                if not token_upper in self.words and token[0] in self.digits:
                    is_number, value = self.to_number(token)
                    if is_number:
                        self.compile__.append(value)
                    else:
                        self.compile__.append(token)
                else:
                    self.compile__.append(token)

        if end:
            if self.compile_name__:
                self.words[self.compile_name__] = self.compile__

            self.state = self.INTERPRET
            return

        self.state = self.COMPILE

    def SQUOTE(self, token, start=False):
        end = token[-1] == "'"
        if end:
            token = token[:-1]
        if start:
            token = token[1:]

        self.stack.append(" ".join(token.split(self.squote_space)))
        self.state = self.INTERPRET

    def DOT_QUOTE(self, token, start=False):
        end = token[-1] == '"'
        if end:
            token = token[:-1]
        if start:
            token = token[2:]
            self.__dot_quote = []

        self.__dot_quote.append(token)

        if end:
            print(" ".join(self.__dot_quote))
            self.state = self.INTERPRET
            return

        self.state = self.DOT_QUOTE

    def sJSON(self, token, start=False):
        end = token[-1] == ')'
        if end:
            token = token[:-1]
        if start:
            self.json__ = []
            self.json_mode__ = token[1]
            token = token[1:]
            if self.json_mode__ == '(':
                token = token[1:]

        if self.json_mode__ == '(':
            if end:
                token = token[:-1]

        self.json__.append(token)

        if end:
            def hook(values):
                if '__complex__' in values:
                    return complex(values['real'], values['imag'])
                return values

            json = " ".join(self.json__)
            json = simplejson.loads(json, use_decimal=True, object_hook=hook)
            self.stack.append(json)
            self.state = self.INTERPRET
            return

        self.state = self.sJSON

    def COMMENT(self, token, start=False):
        end = token[-1] == ")"
        if end:
            self.state = self.INTERPRET
            return

        self.state = self.COMMENT

    def CALL_NOT(self, token, start=False):
        self.CALL(token, start, invert=True)

    def CALL_END(self):
        pass

    def CALL(self, token, start=False, invert=False):
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

            self.state = self.INTERPRET
            return

        self.state = self.CALL

    def CONSTANT(self, token):
        self.words[token.upper()] = self.constant__
        self.state = self.INTERPRET

    def VARIABLE(self, token):
        self.words[token.upper()] = self.here
        self.here +=1
        self.state = self.INTERPRET

    def SEE(self, token):
        word = self.words.get(token.upper(), None)
        if callable(word):
            dis.show_code(word)
            dis.dis(word)
        else:
            print(word)
        self.state = self.INTERPRET

    def sigil(self, name, func):
        name = name.upper()
        self.sigils[name] = func

    def word(self, name, func, has_self=False, argc=None):
        name = name.upper()
        self.words[name] = func

        argc = func.__code__.co_argcount if argc == None else argc
        if argc > 1:
            self.words_argc[name] = argc - 1

    def state_push(self):
        state = {}
        for name in self.state_names:
            state[name] = getattr(self, name)
        self.state_stack.append(copy.deepcopy(state))

    def state_pop(self):
        state = self.state_stack.pop()
        for name in self.state_names:
            setattr(self, name, state[name])

    def state_drop(self):
        self.state_stack.pop()

    def raise_SyntaxException(self, details):
        raise ForthSyntaxException(details)

    def execute(self, token_list, rollback=False, push_frame=True):
        # if rollback:
        #    self.state_push()
        # try:

        c = {"m":"CALL", "EXIT":False}
        c_index = len(self.cstack)
        self.cstack.append(c)

        for token in token_list:
            if isinstance(token, str) and len(token):
                if token[0] in ["#", "\\"]:
                    break

            self.state(token)
            if self.cstack[c_index]["EXIT"]:
                break

        if push_frame:
            self.cstack = self.cstack[:c_index]

        # except Exception as ex:
        #    #if rollback:
        #    #    self.state_pop()
        #    raise ex

        # if rollback:
        #    self.state_drop()


__smoke_0__ = """

T{ 0.1 0.2 + -> 0.3 }T

# :_SQUOTE_SPACE_ 999001;
# (("`")) _SQUOTE_SPACE_ !

T{ 'FOO'BAR' -> (("FOO BAR")) }T

#T{ ''' (.__len__) -> (" ") #1 }T

#T{ ("--") (.__len__) -> ("--") #2 }T

: IDE

CURSES

0 0 20 20 WINDOW

BORDER

REFRESH

GETKEY

;

"""


class ForthException(Exception):
    pass

class ForthSyntaxException(ForthException):
    pass

import dis, copy, collections, simplejson

from decimal import Decimal

from .STD import F_TEST
from .STD import F_NUCLEUS, F_REPL
from .STD import F_DSTACK, F_CONTROL
from .STD import F_MATH, F_IO
from .STD import F_OBJECT
from .STD import F_CURSES
from .STD import F_JSON
