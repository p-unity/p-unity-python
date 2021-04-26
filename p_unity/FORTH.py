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





""" # __banner__

class Engine: # { The Reference Implementation of FORTH^3 : p-unity }

    def __init__(self, run=None, run_tests=2, **kwargs):

        self.run_tests = run_tests # 0, 1=Sanity, 2=&Smoke
        self.tests_1 = []; self.tests_2 = []; self.tests_3 = []

        self.root = TASK(self, root=True)
        self.call = CALL(self)

        self.digits = {}
        for digit in "#$%-01234567890":
            self.digits[digit] = True

        def load(self, names):
            for name in names.split(' '):
                exec(f"from .WORDS import F_{name}")
                exec(f"self.{name} = F_{name}.LIB(self)")
                exec(f"self.add_words(self.{name})")

        load(self, 'CORE STACK MATH CONTROL')
        load(self, 'INPUT OUTPUT REPL')
        load(self, 'OBJECT JSON')
        load(self, 'UNICODE CURSES')

        if self.run_tests >= 1:
            self.execute_tests(__tests_1__)
            for test in self.tests_1:
                self.execute_tests(test if test else "")

        if self.run_tests >= 2:
            self.execute_tests(__tests_2__)
            for test in self.tests_2:
                self.execute_tests(test if test else "")

        if run:
           self.execute(run)

    def raise_SyntaxError(self, details):
        raise ForthSyntaxException(details)

    def raise_RuntimeError(self, details):
        raise ForthRuntimeException(details)

    __word_map = {

        "bang": "!", "at": "@", "hash": "#", "dollar": "$",
        "tick": "'", "quote": '"', "btick": "`", "equal": "=",
        "under": "_", "tilde": "~", "minus": "-", "plus": "+",
        "pipe": "|", "slash": "\\", "divide": "/", "qmark": "?",
        "colon": ":", "semicolon": ";", "dot": ".", "comma": ",",
        "percent": "%", "carat": "^", "amper": "&", "times": "*",
        "lparen": "(", "rparen": ")", "langle": "<", "rangle": ">",
        "lbrack": "[", "rbrack": "]", "lbrace": "{", "rbrace": "}",

        "unicorn": "\u1F984", "rainbow": "\u1F308",
        "astonished": "\u1F632"

    }

    def Mark(self, **kwargs):
        return EngineMark(self, **kwargs)

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
            meta = None
            for part in parts:

                if meta == None:
                    if part == '':
                        meta = []
                        continue
                else:
                    meta.append(part)
                    continue

                if part[0].isupper() or part[0].isdigit():
                    name.append(part.upper())
                else:
                    name.append(self.__word_map[part])

            name = "".join(name)

            if name in self.root.words:
                raise ForthException(f"{name}: error(-4): Word Already Defined")

            if not meta == None:
                if 'I' in meta[0]:
                    self.root.word_IMMEDIATE[name] = True

            word = getattr(source, fname)
            self.root.words[name] = word
            argc = word.__code__.co_argcount
            if argc > 3:
                self.root.word_argc[name] = argc - 3

            self.tests_1.append(word.__doc__)

        self.tests_2.append(source.__doc__)

    @staticmethod
    def to_number(e, t, c, token):

        if not isinstance(token, str):
            return (True, token)

        if not token[0] in e.digits:
            return (False, None)

        if token in e.root.words or token in t.words:
            return (False, None)

        token = token.replace("_", "")

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

        if 'j' in token:
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
                t.stack.extend(token)
            else:
                t.stack.append(token)
            return

        is_number, value = e.to_number(e, t, c, token)
        if is_number:
           t.stack.append(value)
           return

        Engine.run(e, t, c, token)

    @staticmethod
    def run(e, t, c, token):
        token_u = token.upper()

        if not (token_u in e.root.words or token_u in t.words):

            for sigil_len in [5, 4, 3, 2, 1]:
                sigil = token[:sigil_len].upper()
                if sigil in e.root.sigils:
                    e.root.sigils[sigil](e, t, c, token, start=True)
                    return

            details = f"{token}: error(-13): word not found"
            raise ForthException(details)

        args = []
        if token_u in t.words:
            code = t.words[token_u]
            argc = t.word_argc.get(token_u, 0)
        else:
            code = e.root.words[token_u]
            argc = e.root.word_argc.get(token_u, 0)

        if isinstance(code, list):
            t.call_count += 1
            if c.depth == 0:
                c.depth += 1
                e.execute_tokens(e, t, c, code)
                c.depth -= 1
            else:
                e.execute_tokens(e, t, CALL(e, c), code)
            return

        if isinstance(code, tuple):
            t.stack.extend(code)

            if token_u in t.word_does:
                does = t.word_does[token_u]
                e.exeute_tokens(e, t, c, does)

            return

        if argc > len(t.stack):
            details = f"{token}: error(-4): stack underflow"
            raise ForthException(details)

        if argc > 0:
            t.stack, args = t.stack[:-argc], t.stack[-argc:]

        t.stack.extend(code(e, t, c, *args) or tuple())

    @staticmethod
    def execute_tokens(e, t, c, tokens):
        for token in tokens:
            if token in ["#"]:
                break
            t.state(e, t, c, token)
            if c.EXIT:
                break


    def execute_tests(self, tests):
        task = TASK(self)
        call = CALL(self, self.call)
        for line in tests.split("\n"):
            line = line.strip()
            if line == "" or line[0] in ["#"]:
                continue

            f_count = task.f_count
            try:

                call.tokens = line.split()
                while len(call.tokens):
                    token = call.tokens.pop(0)
                    if token in ["#"]:
                        break
                    task.state(self, task, call, token)
                    if call.EXIT:
                        break

            except Exception as ex:
                print(ex)
                task.f_count += 1
            if not f_count == task.f_count:
                print(line)


        self.root.p_count += task.p_count
        self.root.f_count += task.f_count

    def execute(self, lines):
        self.call.EXIT = False
        for line in lines.split("\n"):
            self.root.line += 1
            self.root.lines[self.root.line] = line
            line = line.strip()
            if len(line) == 0 or line[0] in ["#"]:
                continue

            self.call.tokens = line.split()
            while len(self.call.tokens):
                token = self.call.tokens.pop(0)
                self.root.state(self, self.root, self.call, token)
                if self.call.EXIT:
                    return


class TASK:

    def __init__(self, engine, root=False):

        self.engine = engine
        self.is_root = root

        self.stack = []
        self.rstack = []

        self.memory = {}
        self.here = 1_000_000 if root else 1

        self.sigils = {}

        self.words = {}
        self.word_argc = {}
        self.word_does = {}
        self.word_DOES = {}
        self.word_IMMEDIATE = {}

        self.call_count = 0

        self.last_create = ""
        self.last_compile = ""

        self.tick_space = "'"

        self.line = 0
        self.lines = {}

        self.f_count = 0
        self.p_count = 0
        self.x_count = 0

        self.state = engine.state_INTERPRET


class CALL:

    def __init__(self, engine, parent=None):
        self.engine = engine
        self.parent = parent
        self.tokens = []
        self.depth = 0
        self.stack = []
        self.EXIT = False

class EngineMark:

    def __init__(self, engine, **kwargs):
        self.engine = engine
        for k, v in kwargs.items():
            setattr(self, k, v)

class ForthException(Exception):
    pass

class ForthSyntaxException(ForthException):
    pass

class ForthRuntimeException(ForthException):
    pass

import functools

from decimal import Decimal

__tests_1__ = """

T{ 0.1 0.2 + -> 0.3 }T

# T{ 'FOO'BAR' -> (("FOO BAR")) }T

# T{ ''' (.__len__) -> (" ") #1 }T

# T{ ("--") (.__len__) -> ("--") #2 }T

: IDE
CURSES
0 0 20 20 WINDOW BORDER REFRESH
GETKEY
;

: COUNTDOWN    ( n --)
               BEGIN  CR   DUP  .  1 -   DUP   0  =   UNTIL  DROP  ;

# 5 COUNTDOWN

"""

__tests_2__ = """

0 CONSTANT 0S
0 INVERT CONSTANT 1S

T{ <TRUE>  -> 0 INVERT }T
T{ <FALSE> -> 0 }T

: TEN I[ 5 5 + ]I LITERAL ; IM...

: FOO TEN ;

T{ ' FOO -> [ 10 , ] }T

"""

