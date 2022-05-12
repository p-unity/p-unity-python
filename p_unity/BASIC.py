#!/usr/bin/env python3
# -*- encoding: utf-8
# SPDX-License-Identifier: MIT
# Copyright (c) 2021 - 2021, Scott.McCallum@HQ.UrbaneINTER.NET

__banner__ = r""" (

  __    ___       ____                _____   _____    _____
 /_ |  / _ \     |  _ \      /\      / ____| |_   _|  / ____|    _     _
  | | | | | |    | |_) |    /  \    | (___     | |   | |       _| |_ _| |_
  | | | | | |    |  _ <    / /\ \    \___ \    | |   | |      |_   _|_   _|
  | | | |_| |    | |_) |  / ____ \   ____) |  _| |_  | |____    |_|   |_|
  |_|  \___/     |____/  /_/    \_\ |_____/  |_____|  \_____|



)







""" # __banner__

class Engine: # { The Reference Implementation of BASIC++ : p-unity }

    def __init__(self, run_tests=None):
        self.program = {}
        self.cache = {}
        self.loops = {}
        self.lineno = 0
        self.lexer = BasicLexer()
        self.parser = BasicParser(self)
        self.running_program = False
        self.more_variable = None
        self.gosub_stack = collections.deque()

        self.eSCRPT = None

        self.eFORTH = p_unity.FORTH.Engine()
        self.eFORTH_abi = {}

        self.eFORTH.root.memory["__name__"] = "__main__"
        self.eFORTH.root.memory["db"] = DBDispatch()

        self.connection = None
        self.definesql = {}
        self.cursor = None

    def interpret(self, line):

        line = line.strip()
        if line == '' or line[0] == '#':
            return

        try:
            statements = self.parser.parse(self.lexer.tokenize(line))

        except EOFError:
            raise SyntaxError('Unexpected EOF')

        for statement in statements:
            self.execute(*statement)

            if statement.operation in ('list', 'run_program', 'goto'):
                break

    def execute(self, instruction, arguments):
        return getattr(self, instruction)(*arguments)

    def evaluate(self, expression):
        evaluation_stack = collections.deque()
        argument_index_stack = collections.deque()
        node = expression
        last_visited_node = None

        while evaluation_stack or node is not None:
            if node is not None:
                evaluation_stack.append(node)

                if isinstance(node, Expression):
                    argument_index_stack.append(0)
                    node = node.arguments[0]
                else:
                    node = None

            else:
                next_node = evaluation_stack[-1]

                if(
                    isinstance(next_node, Expression)
                    and len(next_node.arguments) > 1
                    and last_visited_node != next_node.arguments[1]
                ):
                    argument_index_stack.append(1)
                    node = next_node.arguments[1]

                elif argument_index_stack:
                    evaluation_stack[-1].arguments[
                        argument_index_stack.pop()
                    ] = last_visited_node = self.visit(evaluation_stack.pop())

                else:
                    return self.visit(next_node)

    def visit(self, node):
        return_value = node

        if isinstance(node, Expression):
            return_value = self.execute(*node)

        return return_value

    def negative(self, a):
        return -a

    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        return a / b

    def fn_mul(self, a, b):
        return a * b

    def fn_abs(self, a):
        return abs(a)

    def fn_len(self, a):
        return len(a)

    def fn_type(self, a):
        return type(a)

    def fn_jsonload(self, a):

        def h(values):
            if "__complex__" in values:
                return complex(values["real"], values["imag"])
            return values

        import simplejson
        return simplejson.loads(a, use_decimal=True, object_hook=h)

    def fn_jsonsave(self, a):
        def encode(_):
            if isinstance(_, complex):
                return {"__complex__": True, "real": _.real, "imag": _.imag}
            raise TypeError(repr(_) + " is not JSON serializable")

        import simplejson
        return simplejson.dumps(a, default=encode)

    def fn_jsonpath(self, obj, path):
        from jsonpath import JSONPath
        return JSONPath(path).parse(obj)


    def get_variable(self, name, extra_keys=[]):

        keys = []
        parts = name.split("~")
        keys.append(parts[0].lower())
        for part in parts[1:]:
            index = part
            try:
                index = int(part)
            except ValueError:
                pass
            keys.append(index)
        keys.extend(extra_keys)

        object = self.eFORTH.root.memory
        for key in keys[:-1]:
            if type(object) == type([]):
                object = object[key]
            else:
                object = object[key] if key in object else {}

        if type(object) == type([]):
            return object[keys[-1]]
        else:
            return object[keys[-1]] if keys[-1] in object else 0

    def get_variable_indexed1(self, name, i0):
        keys = [self.evaluate(i0)]
        return self.get_variable(name, extra_keys=keys)

    def get_variable_indexed2(self, name, i0, i1):
        keys = [self.evaluate(i0),self.evaluate(i1)]
        return self.get_variable(name, extra_keys=keys)

    def get_variable_indexed3(self, name, i0, i1, i2):
        keys = [self.evaluate(i0),self.evaluate(i1),self.evaluate(i2)]
        return self.get_variable(name, extra_keys=keys)

    def set_variable(self, name, value, value_raw=None, extra_keys=[]):

        keys = []
        parts = name.split("~")
        keys.append(parts[0].lower())
        for part in parts[1:]:
            try:
                index = int(part)
            except ValueError:
                index = part
            keys.append(index)
        keys.extend(extra_keys)

        self.more_variable = keys

        object = self.eFORTH.root.memory
        for key in keys[:-1]:
            if type(object) == type([]):
                object = object[key]
            else:
                if not key in object:
                    object[key] = {}
                object = object[key]

        object[keys[-1]] = self.evaluate(value) if value_raw == None else value_raw

    def set_variable_index1(self, name, i0, value):
        keys = [self.evaluate(i0)]
        self.set_variable(name, value, extra_keys=keys)

    def set_variable_index2(self, name, i0, i1, value):
        keys = [self.evaluate(i0), self.evaluate(i1)]
        self.set_variable(name, value, extra_keys=keys)

    def set_variable_index3(self, name, i0, i1, i2, value):
        keys = [self.evaluate(i0), self.evaluate(i1), self.evaluate(i2)]
        self.set_variable(name, value, extra_keys=keys)

    def set_array(self, name):
        self.set_variable(name, None, value_raw=[])

    def set_table(self, name):
        self.set_variable(name, None, value_raw={})

    def control_for_to(self, name, start, end, step):
        loop = {"end":self.evaluate(end), "step":self.evaluate(step)}
        loop["line"] = self.last_program_lineno + 1
        self.loops[name.lower()] = loop
        self.eFORTH.root.memory[name.lower()] = self.evaluate(start)

    def control_next(self, name):
        loop = self.loops[name.lower()]
        curr = self.eFORTH.root.memory[name.lower()]
        curr = curr + loop["step"]
        self.eFORTH.root.memory[name.lower()] = curr
        if curr <= loop["end"]:
            self.current_program_lineno = loop["line"]

    def compare_variable(self, name, value):
        return -1 if self.eFORTH.root.memory[name.lower()] == value else 0

    def add_program_line(self, lineno, line):

        line = line.split('#', 1)[0]
        line = line.strip()
        if line == '':
            return

        #statements = self.parser.parse(self.lexer.tokenize(line))

        if line[:6].lower() == "defsql":
            statements = self.parser.parse(self.lexer.tokenize(line))
            k, v = tuple(statements[0].arguments[0:2])
            self.definesql[k] = v

        self.program[lineno] = line

    def remove_program_line(self, lineno):
        self.program.pop(lineno, None)

    def end_program(self):
        self.running_program = False

    def run_program(self, lineno=None):
        if not self.program:
            return

        self.running_program = True

        linenos = sorted(self.program)
        current_line_index = 0
        self.current_program_lineno = linenos[0]

        if lineno is not None:
            current_line_index = linenos.index(lineno)
            self.current_program_lineno = lineno

        self.last_program_lineno = 0
        while True:
            if self.current_program_lineno is not None:

                while True:
                    try:
                        current_line_index = linenos.index(self.current_program_lineno)
                        break
                    except ValueError:
                        self.current_program_lineno += 1


            else:
                try:
                    current_line_index += 1
                    self.current_program_lineno = linenos[current_line_index]

                except IndexError:
                    break

            current_program_line = self.program[self.current_program_lineno]
            self.last_program_lineno = self.current_program_lineno
            self.current_program_lineno = None
            self.interpret(current_program_line)

        self.running_program = False

    def goto(self, expr):
        try:
            int(expr)

        except ValueError:
            raise SyntaxError('Type mismatch error')

        if not self.running_program:
            self.run_program(lineno=int(expr))

        else:
            self.current_program_lineno = int(expr)

    def gosub(self, expr):
        try:
            int(expr)

        except ValueError:
            raise SyntaxError('Type mismatch error')

        self.gosub_stack.append(self.last_program_lineno + 1)

        self.current_program_lineno = int(expr)

    def statement_return(self):
        self.current_program_lineno = self.gosub_stack.pop()

    def conditional(self, expr, then_statements, else_statement=None):
        if self.evaluate(expr):
            for statement in then_statements:
                self.execute(*statement)

        elif else_statement:
            self.execute(*else_statement)

    def noop(self):
        pass

    def more(self, *args):
        keys = self.more_variable
        object = self.eFORTH.root.memory
        for key in keys[:-1]:
            if not key in object:
                object[key] = {}
            object = object[key]

        current = object[keys[-1]]
        for arg in args:
            current = current + str(self.evaluate(arg))
        object[keys[-1]] = current

    def print(self, *args):
        print(*(self.evaluate(arg) for arg in args))

    def format(self, *args):
        string = self.evaluate(args[0])
        if len(args) == 1:
            print(string.format(**self.eFORTH.root.memory))
        else:
            format_args = (self.evaluate(arg) for arg in args)
            print(string.format(*format_args))

    def forth(self, *args):

        depth = len(self.eFORTH.root.stack)

        if len(args) > 1:
            for arg in args[1:]:
                self.eFORTH.root.stack.append(self.evaluate(arg))

        self.eFORTH.execute(self.evaluate(args[0]))

        for k, v in self.eFORTH_abi.items():
            if k in self.eFORTH.root.memory:
                del self.eFORTH.root.memory[k]

        self.eFORTH_abi = {}

        results = self.eFORTH.root.stack[depth:]
        results.reverse()
        self.eFORTH.root.memory["stack"] = results
        index = 0
        for result in results:
            self.eFORTH.root.memory[f"f{index}"] = result
            self.eFORTH_abi[f"f{index}"] = result
            index += 1

    def list(self):
        for lineno, line in sorted(self.program.items()):
            print(f'{lineno} {line}')

    def defsql(self, *args):
        pass

    def sql(self, *args):
        arg0 = self.evaluate(args[0])
        if self.connection == None:
            import sqlite3
            self.connection = sqlite3.connect("example.sqlite")
            self.cursor = self.connection.cursor()

        statement = self.definesql[arg0.lower()]
        if len(args) == 1:
            self.cursor.execute(statement, self.eFORTH.root.memory)
        else:
            args = tuple((self.evaluate(arg) for arg in args[1:]))
            self.cursor.execute(statement,args)
        self.eFORTH.root.memory["s"] = self.cursor.fetchall()

from p_unity.pysos import Dict

class DBDispatch:

    def __init__(self):
        self.dbs = {}

    def __getitem__(self, key):
        key = key.lower()
        if not key in self.dbs:
            self.dbs[key] = Dict(f"db\\{key}.txt")
        return self.dbs[key]

    def __contains__(self, key):
        return True


import math
import collections

from sly.lex import Lexer, Token
from sly.yacc import Parser

Variable = collections.namedtuple('Variable', ['name'])
Expression = collections.namedtuple('Expression', ['operation', 'arguments'])
Statement = collections.namedtuple('Statement', ['operation', 'arguments'])

class BasicLexer(Lexer):
    tokens = {
        ID,
        REM,
        FORMAT,
        ARRAY,
        TABLE,
        PRINT,
        FORTH,
        SQL,
        DEFSQL,
        IF,
        THEN,
        ELSE,
        LIST,
        RUN,
        END,
        GOTO,
        GOSUB,
        RETURN,
        STRING,
        SSTRING,
        RSTRING,
        LINENO,
        NUMBER,
        PLUS,
        MINUS,
        MULTIPLY,
        DIVIDE,
        EQUALS,
        COLON,
        COMMA,
        MORE,

        FOR,
        TO,
        IN,
        STEP,
        NEXT,

        MUL,
        ABS,

        LEN,
        TYPE,

        JSONLOAD,
        JSONSAVE,
        JSONPATH,

        LPAREN,
        RPAREN,
        LBRACK,
        RBRACK
    }

    ignore = ' \t\n'
    ignore_comment = r'\#.*'

    PLUS = r'\+'
    MINUS = r'-'
    MULTIPLY = r'\*'
    DIVIDE = r'/'
    EQUALS = r'='
    COLON = r':'
    LPAREN = r'\('
    RPAREN = r'\)'
    COMMA = r','

    LBRACK = r'\['
    RBRACK = r'\]'

    def nocase_match(name):
        result = []
        for letter in name:
            result.append("[{0}{1}]".format(letter, letter.lower()))
        return r''.join(result)

    REM = r"(?:[Rr][Ee][Mm]).*"
    PRINT = nocase_match("PRINT")
    FORMAT = nocase_match("FORMAT")
    FORTH = nocase_match("FORTH")
    SQL = nocase_match("SQL")

    TABLE = nocase_match("TABLE")
    ARRAY = nocase_match("ARRAY")

    DEFSQL = nocase_match("DEFSQL")
    IF = nocase_match("IF")
    THEN = nocase_match("THEN")
    ELSE = nocase_match("ELSE")
    LIST = nocase_match("LIST")
    RUN = nocase_match("RUN")
    END = nocase_match("END")
    GOTO = nocase_match("GOTO")
    GOSUB = nocase_match("GOSUB")
    RETURN = nocase_match("RETURN")

    FOR = nocase_match("FOR")
    TO = nocase_match("TO")
    IN = nocase_match("IN")
    STEP = nocase_match("STEP")
    NEXT = nocase_match("NEXT")

    MUL = nocase_match("MUL")
    ABS = nocase_match("ABS")
    LEN = nocase_match("LEN")
    TYPE = nocase_match("TYPE")

    JSONLOAD = nocase_match("JSONLOAD")
    JSONSAVE = nocase_match("JSONSAVE")
    JSONPATH = nocase_match("JSONPATH")

    MORE = nocase_match("MORE")

    ID = r'[A-Za-z_][A-Za-z0-9_$~!]*'

    @_(r'(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)')
    def NUMBER(self, token):
        if(
            self.index
            and self.text[:token.index] != token.index * ' '
        ):

            if '.' not in token.value:
                token.value = (int(token.value))
            else:
                token.value = (Decimal(token.value))

        else:
            if '.' not in token.value:
                token.value = int(token.value)

            else:
                dot_index = token.value.index('.')
                self.index -= len(token.value) - dot_index
                token.value = int(token.value[:dot_index])

            token.type = 'LINENO'

            if self.text[self.index:].strip(' '):
                self.begin(LineLexer)

        return token


    @_(r'\".*?(?<!\\)(\\\\)*\"')
    def STRING(self, t):
        """
        Parsing strings (including escape characters)
        """
        t.value = t.value[1:-1]
        t.value = t.value.replace(r"\n", "\n")
        t.value = t.value.replace(r"\t", "\t")
        t.value = t.value.replace(r"\\", "\\")
        t.value = t.value.replace(r"\"", "\"")
        t.value = t.value.replace(r"\a", "\a")
        t.value = t.value.replace(r"\b", "\b")
        t.value = t.value.replace(r"\r", "\r")
        t.value = t.value.replace(r"\t", "\t")
        t.value = t.value.replace(r"\v", "\v")
        return t

    @_(r"\'.*?(?<!\\)(\\\\)*\'")
    def SSTRING(self, t):
        """
        Parsing strings (including escape characters)
        """
        t.value = t.value[1:-1]
        t.value = t.value.replace(r"\n", "\n")
        t.value = t.value.replace(r"\t", "\t")
        t.value = t.value.replace(r"\\", "\\")
        t.value = t.value.replace(r"\a", "\a")
        t.value = t.value.replace(r"\b", "\b")
        t.value = t.value.replace(r"\r", "\r")
        t.value = t.value.replace(r"\t", "\t")
        t.value = t.value.replace(r"\v", "\v")
        return t

    @_(r'`[^`]*`?')
    def RSTRING(self, token):
        token.value = token.value[1:]

        if token.value.endswith('`'):
            token.value = token.value[:-1]

        return token





class LineLexer(Lexer):
    tokens = {LINE}
    ignore = ' '

    @_(r'.+')
    def LINE(self, token):
        self.begin(BasicLexer)
        return token


class BasicParser(Parser):
    #debugfile = 'basic_debug.out'
    tokens = BasicLexer.tokens.union(LineLexer.tokens)
    precedence = (
        ('nonassoc', IF, THEN, FOR, NEXT),
        ('left', COLON),
        ('nonassoc', ELSE, TO),
        ('left', EQUALS),
        ('left', CREATE_EXPRS, APPEND_EXPRS),
        ('left', PLUS, MINUS),
        ('left', MULTIPLY, DIVIDE),
        ('nonassoc', UNARY_MINUS),
    )

    def __init__(self, interpreter):
        self.interpreter = interpreter

    @_('statement')
    def statements(self, parsed):
        if parsed.statement:
            return [parsed.statement]

    @_('statements COLON statement')
    def statements(self, parsed):
        parsed.statements.append(parsed.statement)
        return parsed.statements

    @_(
        'statements COLON empty',
        'empty COLON statements',
    )
    def statements(self, parsed):
        return parsed.statements

    @_('')
    def empty(self, parsed):
        pass

    @_('LINENO LINE')
    def statement(self, parsed):
        return Statement('add_program_line', (parsed.LINENO, parsed.LINE))

    @_('IF expr THEN statements')
    def statement(self, parsed):
        return Statement('conditional', (parsed.expr, parsed.statements))

    @_('IF expr THEN statements ELSE statement')
    def statement(self, parsed):
        return Statement(
            'conditional',
            (parsed.expr, parsed.statements, parsed.statement),
        )

    @_('FOR variable IN expr')
    def statement(self, parsed):
        return Statement('control_for_in', (parsed.variable.name, parsed.expr0))

    @_('FOR variable EQUALS expr TO expr')
    def statement(self, parsed):
        return Statement('control_for_to', (parsed.variable.name, parsed.expr0, parsed.expr1, 1))

    @_('FOR variable EQUALS expr TO expr STEP expr')
    def statement(self, parsed):
        return Statement('control_for_to', (parsed.variable.name, parsed.expr0, parsed.expr1, parsed.expr2))

    @_('NEXT variable')
    def statement(self, parsed):
        return Statement('control_next', (parsed.variable.name,))

    @_('ARRAY variable')
    def statement(self, parsed):
        return Statement('set_array', (parsed.variable.name,))

    @_('TABLE variable')
    def statement(self, parsed):
        return Statement('set_table', (parsed.variable.name,))

    @_('variable EQUALS expr')
    def statement(self, parsed):
        return Statement('set_variable', (parsed.variable.name, parsed.expr))

    @_('variable LBRACK expr RBRACK EQUALS expr')
    def statement(self, p):
        return Statement('set_variable_index1', (p.variable.name, p.expr0, p.expr1))

    @_('variable LBRACK expr RBRACK LBRACK expr RBRACK EQUALS expr')
    def statement(self, p):
        return Statement('set_variable_index2', (p.variable.name, p.expr0, p.expr1, p.expr2))

    @_('variable LBRACK expr RBRACK LBRACK expr RBRACK LBRACK expr RBRACK EQUALS expr')
    def statement(self, p):
        return Statement('set_variable_index3', (p.variable.name, p.expr0, p.expr1, p.expr2, p.expr3))

    @_('MORE exprs')
    def statement(self, parsed):
        return Statement('more', parsed.exprs)

    @_('REM')
    def statement(self, parsed):
        return Statement('noop', [])

    @_('FORMAT exprs')
    def statement(self, parsed):
        return Statement('format', parsed.exprs)

    @_('SQL exprs')
    def statement(self, parsed):
        return Statement('sql', parsed.exprs)

    @_('DEFSQL exprs')
    def statement(self, parsed):
        return Statement('defsql', parsed.exprs)

    @_('PRINT exprs')
    def statement(self, parsed):
        return Statement('print', parsed.exprs)

    @_('FORTH exprs')
    def statement(self, parsed):
        return Statement('forth', parsed.exprs)

    @_('LIST')
    def statement(self, parsed):
        return Statement('list', [])

    @_('RUN')
    def statement(self, parsed):
        return Statement('run_program', [])

    @_('END')
    def statement(self, parsed):
        return Statement('end_program', [])

    @_('GOTO expr')
    def statement(self, parsed):
        return Statement('goto', [parsed.expr])

    @_('GOSUB expr')
    def statement(self, parsed):
        return Statement('gosub', [parsed.expr])

    @_('RETURN')
    def statement(self, parsed):
        return Statement('statement_return', [])

    @_('expr %prec CREATE_EXPRS')
    def exprs(self, parsed):
        return [parsed.expr]

    #@_('exprs expr %prec APPEND_EXPRS')
    #def exprs(self, parsed):
    #    parsed.exprs.append(parsed.expr)
    #    return parsed.exprs

    @_('exprs COMMA expr %prec APPEND_EXPRS')
    def exprs(self, parsed):
        parsed.exprs.append(parsed.expr)
        return parsed.exprs


    @_('MUL LPAREN expr COMMA expr RPAREN')
    def expr(self, parsed):
        return Expression('fn_mul', [parsed.expr0, parsed.expr1])

    @_('ABS LPAREN expr RPAREN')
    def expr(self, parsed):
        return Expression('fn_abs', [parsed.expr])

    @_('LEN LPAREN expr RPAREN')
    def expr(self, parsed):
        return Expression('fn_len', [parsed.expr])

    @_('TYPE LPAREN expr RPAREN')
    def expr(self, parsed):
        return Expression('fn_type', [parsed.expr])

    @_('JSONLOAD LPAREN expr RPAREN')
    def expr(self, parsed):
        return Expression('fn_jsonload', [parsed.expr])

    @_('JSONSAVE LPAREN expr RPAREN')
    def expr(self, parsed):
        return Expression('fn_jsonsave', [parsed.expr])

    @_('JSONPATH LPAREN expr COMMA expr RPAREN')
    def expr(self, parsed):
        return Expression('fn_jsonpath', [parsed.expr0, parsed.expr1])

    @_('variable EQUALS expr')
    def expr(self, parsed):
        return Expression(
            'compare_variable',
            [parsed.variable.name, parsed.expr],
        )

    @_('MINUS expr %prec UNARY_MINUS')
    def expr(self, parsed):
        return Expression('negative', [parsed.expr])

    @_('LPAREN expr RPAREN')
    def expr(self, parsed):
        return parsed.expr

    @_('expr PLUS expr')
    def expr(self, parsed):
        return Expression('add', [parsed.expr0, parsed.expr1])

    @_('expr MINUS expr')
    def expr(self, parsed):
        return Expression('subtract', [parsed.expr0, parsed.expr1])

    @_('expr MULTIPLY expr')
    def expr(self, parsed):
        return Expression('multiply', [parsed.expr0, parsed.expr1])

    @_('expr DIVIDE expr')
    def expr(self, parsed):
        return Expression('divide', [parsed.expr0, parsed.expr1])

    @_(
        'NUMBER',
        'STRING',
        'SSTRING',
        'RSTRING',
    )
    def expr(self, parsed):
        return parsed[0]

    @_('variable')
    def expr(self, parsed):
        return Expression('get_variable', [parsed.variable.name])

    @_('variable LBRACK expr RBRACK')
    def expr(self, p):
        return Expression('get_variable_indexed1', [p.variable.name, p.expr])

    @_('variable LBRACK expr RBRACK LBRACK expr RBRACK')
    def expr(self, p):
        return Expression('get_variable_indexed2', [p.variable.name, p.expr0, p.expr1])

    @_('variable LBRACK expr RBRACK LBRACK expr RBRACK LBRACK expr RBRACK')
    def expr(self, p):
        return Expression('get_variable_indexed3', [p.variable.name, p.expr0, p.expr1, p.expr2])

    @_('ID')
    def variable(self, parsed):
        return Variable(parsed.ID)

    def error(self, token):
        if not token:
            raise EOFError('Parse error in input, unexpected EOF')

        raise SyntaxError(
            f'Syntax error at line {token.lineno}, token={token.type}'
        )

import p_unity.FORTH

from decimal import Decimal

import copy


