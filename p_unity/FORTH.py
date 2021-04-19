#!/usr/bin/env python3
# -*- encoding: utf-8


__banner__ = r""" ( Copyright Intermine.com.au Pty Ltd. or its affiliates.
                    License SPDX: Programming-Unity-10.42 or as negotiated.

       ______    ____    _____    _______   _    _     /\   ____
  _   |  ____|  / __ \  |  __ \  |__   __| | |  | |   |/\| |___ \    _
 (_)  | |__    | |  | | | |__) |    | |    | |__| |          __) |  (_)
      |  __|   | |  | | |  _  /     | |    |  __  |         |__ <
  _   | |      | |__| | | | \ \     | |    | |  | |         ___) |   _
 (_)  |_|       \____/  |_|  \_\    |_|    |_|  |_|        |____/   ( )
                                                                    |/


)




"""  # __banner__


class Engine: # { The Reference Implementation of FORTH^3 : p-unity }

    def __init__(self, run_tests=None, autoexec=None):

        self.run_tests = run_tests # None/0, 1=Sanity, 2=&Smoke

        self.root = EngineTask(self, root=True)

        self.digits = {}
        for digit in "#$%-01234567890":
            self.digits[digit] = True

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

        self.ASCII = F_ASCII.LIB(self)
        self.add_words(self.ASCII)

        self.CURSES = F_CURSES.LIB(self)
        self.add_words(self.CURSES)

        if self.run_tests and self.run_tests >= 2:
           self.execute(smoke_tests)

        if autoexec:
           self.execute(autoexec)

    def raise_SyntaxError(self, details):
        raise ForthSyntaxException(details)

    def raise_RuntimeError(self, details):
        raise ForthRuntimeException(details)

    __word_map = {

        "colon": ":", "semicolon": ";", "dot": ".", "comma": ",",
        "squote": "'", "dquote": '"', "btick": "`", "equal": "=",
        "under": "_", "tilde": "~", "minus": "-", "plus": "+",
        "percent": "%", "carat": "^", "amper": "&", "times": "*",
        "bang": "!", "at": "@", "hash": "#", "dollar": "$",
        "lsquare": "[", "rsquare": "]", "lbrace": "{", "rbrace": "}",
        "lbracket": "(", "rbracket": ")", "langle": "<", "rangle": ">",
        "pipe": "|", "slash": "\\", "divide": "/", "qmark": "?",
        "unicorn": "\u1F984", "rainbow": "\u1F308",
        "astonished": "\u1F632"

    }

    def add_word(self, name, code):
        self.root.words[name] = code

    def add_words(self, source):

        word_names = []
        sigil_names = []
        for fname in dir(source):
            parts = fname.split('_')
            if len(parts) > 1 and parts[0][:4] == 'word':
                word = getattr(source, fname)
                word_names.append((word.__code__.co_firstlineno, fname))
            if len(parts) > 1 and parts[0][:5] == 'sigil':
                sigil = getattr(source, fname)
                sigil_names.append((sigil.__code__.co_firstlineno, fname))


        sigil_names.sort()
        for order, fname in sigil_names:
            parts = fname.split('_')[1:]

            name = []
            for part in parts:
                if part == '': break
                if part[0].isupper() or part[0].isdigit():
                    name.append(part.upper())
                else:
                    name.append(self.__word_map[part])

            name = "".join(name)
            if name in self.root.sigils:
                raise ForthException(f"{name}: error(-4): Sigil Already Defined")

            sigil = getattr(source, fname)
            self.root.sigils[name] = sigil

            if self.run_tests and sigil.__doc__:
                self.execute_tests(sigil.__doc__)


        word_names.sort()
        for order, fname in word_names:
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
            if name in self.root.words:
                raise ForthException(f"{name}: error(-4): Word Already Defined")

            word = getattr(source, fname)
            self.root.words[name] = word
            argc = word.__code__.co_argcount
            if argc > 3:
                self.root.words_argc[name] = argc - 3

            if self.run_tests and word.__doc__:
                self.execute_tests(word.__doc__)

        if self.run_tests and source.__doc__:
            self.execute_tests(source.__doc__)


    @staticmethod
    def to_number(e, t, c, token):

        if not token[0] in e.digits:
            return (False, None)

        if token in e.root.words or token in t.words:
            return (False, None)

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

    @staticmethod
    def state_INTERPRET(e, t, c, token):

        if not isinstance(token, str):
            if isinstance(token, tuple):
                t.stack.append(token[0])
            else:
                t.stack.append(token)
            return

        for sigil_len in [5, 4, 3, 2, 1]:
            sigil = token[:sigil_len].upper()
            if sigil in e.root.sigils:
                e.root.sigils[sigil](e, t, c, token, start=True)
                return

        token_u = token.upper()

        is_number, value = e.to_number(e, t, c, token_u)
        if is_number:
           t.stack.append(value)
           return

        if not (token_u in e.root.words or token_u in t.words):
            details = f"{token}: error(-13): word not found"
            raise ForthException(details)

        args = []
        if token_u in e.root.words:
            argc = e.root.words_argc.get(token_u, 0)
            code = e.root.words[token_u]
        else:
            argc = t.words_argc.get(token_u, 0)
            code = t.words[token_u]

        if isinstance(code, list):
            if c.depth == 0:
                c.depth += 1
                e.execute_tokens(e, t, c, code)
                c.depth -= 1
            else:
                e.execute_tokens(e, t, EngineCall(e), code)

            return

        #if not callable(code):
        #    t.stack.append(code)
        #    return

        if argc > len(t.stack):
            details = f"{token}: error(-4): stack underflow"
            raise ForthException(details)

        if argc > 0:
            t.stack, args = t.stack[:-argc], t.stack[-argc:]

        t.stack.extend(code(e, t, c, *args) or tuple())


    @staticmethod
    def execute_tokens(e, t, c, tokens):
        for token in tokens:
            if token in ["#", "\\"]:
                break
            t.state(e, t, c, token)
            if c.EXIT:
                break

    def execute_tests(self, tests):
        task = EngineTask(self)
        call = EngineCall(self)
        for line in tests.split("\n"):
            line = line.strip()
            if line == "" or line[0] in ["#", "\\"]:
                continue
            f_count = self.TEST.f_count
            self.execute_tokens(self, task, call, line.split())
            if not f_count == self.TEST.f_count:
                print(line)

    def execute(self, lines):
        call = EngineCall(self)
        for line in lines.split("\n"):
            line = line.strip()
            if len(line) == 0 or line[0] in ["#", "\\"]:
                continue
            for token in line.split():
                self.root.state(self, self.root, call, token)
                if call.EXIT:
                    return


class EngineTask:

    def __init__(self, engine, root=False):

        self.engine = engine

        self.is_root = root

        self.stack = []

        self.memory = {}
        self.here = 1_000_000 if root else 1

        self.words = {}
        self.words_argc = {}

        self.sigils = {}

        self.squote_space = "'"

        self.state = engine.state_INTERPRET

class EngineCall:

    def __init__(self, engine):

        self.engine = engine

        self.depth = 0

        self.stack = []

        self.EXIT = False



class ForthException(Exception):
    pass

class ForthSyntaxException(ForthException):
    pass

class ForthRuntimeException(ForthException):
    pass

import dis, copy, collections, simplejson

from decimal import Decimal

from .CORE import F_TEST
from .CORE import F_NUCLEUS, F_REPL
from .CORE import F_DSTACK, F_CONTROL
from .CORE import F_MATH, F_IO
from .CORE import F_OBJECT
from .CORE import F_CURSES
from .CORE import F_JSON, F_ASCII



smoke_tests = """

T{ 0.1 0.2 + -> 0.3 }T

# T{ 'FOO'BAR' -> (("FOO BAR")) }T

# T{ ''' (.__len__) -> (" ") #1 }T

# T{ ("--") (.__len__) -> ("--") #2 }T

: IDE
CURSES
0 0 20 20 WINDOW BORDER REFRESH
GETKEY
;

"""

