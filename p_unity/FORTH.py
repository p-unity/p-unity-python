#!/usr/bin/env python3
# -*- encoding: utf-8


__banner__ = """ ( Copyright Intermine.com.au Pty Ltd. or its affiliates.
                   SPDX-License-Identifier: Programming-Unity-10.42

       ______    ____    _____    _______   _    _
  _   |  ____|  / __ \  |  __ \  |__   __| | |  | |   _
 (_)  | |__    | |  | | | |__) |    | |    | |__| |  (_)
      |  __|   | |  | | |  _  /     | |    |  __  |
  _   | |      | |__| | | | \ \     | |    | |  | |   _
 (_)  |_|       \____/  |_|  \_\    |_|    |_|  |_|  ( )
                                                     |/


)





""" # __banner__

class Engine:

    def __init__(self, **kwargs):

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
        self.state_names.extend(['words','words_argc'])

        self.stack = []
        self.state_names.append('stack')

        self.minus_gt = 0
        self.state_names.append('minus_gt')

        self.state = self.INTERPRET
        self.state_names.append('state')

        self.squote_space = "'"

        self.digits = {}
        for digit in "#$%-01234567890":
            self.digits[digit] = True

        self.__core__()

        self.TEST = F_TEST.LIB(**kwargs)
        self.add_words(self.TEST)

        self.DSTACK = F_DSTACK.LIB(**kwargs)
        self.add_words(self.DSTACK)

        self.CORE = F_CORE.LIB(**kwargs)
        self.add_words(self.CORE)

        self.REPL = F_REPL.LIB(**kwargs)
        self.add_words(self.REPL)

        self.MATH = F_MATH.LIB(**kwargs)
        self.add_words(self.MATH)

        self.OBJECT = F_OBJECT.LIB(**kwargs)
        self.add_words(self.OBJECT)

        self.JSON = F_JSON.LIB(**kwargs)
        self.add_words(self.JSON)

        self.CURSES = F_CURSES.LIB(**kwargs)
        self.add_words(self.CURSES)

        for line in __smoke_0__.split('\n'):
            self.execute(line.split())

        if 'autoexec' in kwargs:
            autoexec = kwargs['autoexec']
            for line in autoexec.split('\n'):
                self.execute(line.split())

    __word_map = {

            "colon":":", "semicolon":";", "dot":".", "comma":",",
            "squote":"'", "dquote":'"', "btick":"`",
            "under":"_", "tilde":"~", "minus":"-", "plus":"+",
            "percent":"%", "carat":"^", "amper":"&", "times":"*",
            "bang":"!", "at":"@", "hash":"#", "dollar":"$",
            "lbrace":"[", "rbrace":"]", "lbrace":"{", "rbrace":"}",
            "lbracket":"(", "rbracket":")", "langle":"<", "rangle":">",
            "pipe":"|", "slash":"\\", "divide":"/", "qmark":"?",
            "unicorn":"\u1F984", "rainbow":"\u1F308",
            "astonished":"\u1F632"

            }

    def add_words(self, source):

        tests = []

        names = dir(source)
        names.sort()

        if 'P_UNITY' in names:
            constructor = getattr(source, 'P_UNITY')
            constructor(self)

        for fname in names:
            parts = fname.split('_')
            if len(parts) < 2 or not parts[0][:4] == 'word':
                continue
            parts = parts[1:]

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

            if name in self.words:
                raise ForthException(f"{name}: error(-4): Already defined")

            self.words[name] = word
            argc = word.__code__.co_argcount
            if argc > 1:
                self.words_argc[name] = argc - 1

            if word.__doc__:
                for line in word.__doc__.split('\n'):
                    f_count = self.TEST.f_count
                    self.execute(line.split())
                    if not f_count == self.TEST.f_count:
                        print(str(word))

        if source.__doc__:
            for line in source.__doc__.split('\n'):
                f_count = self.TEST.f_count
                self.execute(line.split())
                if not f_count == self.TEST.f_count:
                   print(str(source))

        return tests

    def __core__(self):

        @ForthWord(self, "PRINT")
        def PRINT(f, o):
            print(o)

        @ForthWord(self, "CONSTANT")
        def CONSTANT(f):
            f.state = f.CONSTANT

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
        if token[0] == '#':
            token = token[1:]
        elif token[0] == '$':
            token = token[1:]
            is_integer = True
            if '.' in token:
                is_integer = False
                token = token.split('.')[0]
            if is_integer:
                return (True, int(token, 16))
            else:
                return (True, Decimal(int(token,16)))
        elif token[0] == '%':
            token = token[1:]
            is_integer = True
            if '.' in token:
                is_integer = False
                token = token.split('.')[0]
            if is_integer:
                return (True, int(token, 2))
            else:
                return (True, Decimal(int(token,2)))

        if token[0] == '-' and len(token) > 1:
            if not token[1].isdigit():
                return (False, None)

        if 'J' in token:
            return (True, complex(token))
        else:
            if '.' in token:
                return (True, Decimal(token))
            else:
                return (True, int(token))
        return (False, None)

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
            self.__compile = []
            self.__compile_name = None

        if token == ":":
            raise ForthException(':: error (-1): compile in compile')

        if not self.__compile_name:
            if not token == '':
                self.__compile_name = token.upper()
        else:
            if len(token):
                token_upper = token.upper()
                if not token_upper in self.words and token[0] in self.digits:
                    is_number, value = self.to_number(token)
                    if is_number:
                        self.__compile.append(value)
                    else:
                        self.__compile.append(token)
                else:
                    self.__compile.append(token)

        if end:
            if self.__compile_name:
                self.words[self.__compile_name] = self.__compile

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
            self.stack.append(" ".join(self.__dot_quote))
            self.state = self.INTERPRET
            return

        self.state = self.DOT_QUOTE


    def sJSON(self, token, start=False):
        end = token[-1] == ')'
        if end:
            token = token[:-1]
        if start:
            self.__json = []
            self.__json_mode = token[1]
            token = token[1:]
            if self.__json_mode == '(':
                token = token[1:]

        if self.__json_mode == '(':
            if end:
                token = token[:-1]

        self.__json.append(token)

        if end:
            def hook(values):
                if '__complex__' in values:
                    return complex(values['real'], values['imag'])
                return values
            json = " ".join(self.__json)
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
            self.__call = [token[1:]]
            self.__call_invert = invert

        if end:
            obj = self.stack[-1]
            code = getattr(obj, self.__call[0])
            args = self.__call[1:]
            result = code(*args)
            if result == None:
                pass
            elif isinstance(result, tuple):
                self.stack.extend(result)
            else:
                if self.__call_invert:
                    self.stack.append(not result)
                else:
                    self.stack.append(result)

            self.state = self.INTERPRET
            return

        self.state = self.CALL


    def CONSTANT(self, token):
        self.words[token.upper()] = self.stack[-1]
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

    def execute(self, token_list, rollback=False):
        #if rollback:
        #    self.state_push()
        #try:

        for token in token_list:
            if isinstance(token, str) and len(token):
                if token[0] in ["#", "\\"]:
                    break
            self.state(token)

        #except Exception as ex:
        #    #if rollback:
        #    #    self.state_pop()
        #    raise ex

        #if rollback:
        #    self.state_drop()



class ForthWord(object):
    def __init__ (self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __call__(self, func):
        def newf(*args, **kwargs):
            return func(*args, **kwargs)
        argc = func.__code__.co_argcount
        self.args[0].word(self.args[1], newf, argc=argc)
        return newf

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

import dis, copy, collections, simplejson

from decimal import Decimal

from .STD import F_TEST

from .STD import F_DSTACK

from .STD import F_CORE, F_REPL

from .STD import F_MATH

from .STD import F_OBJECT

from .STD import F_CURSES

from .STD import F_JSON
