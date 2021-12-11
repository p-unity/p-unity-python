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
        self.lineno = 0
        self.lexer = BasicLexer()
        self.parser = BasicParser(self)
        self.running_program = False

        self.eSCRPT = None

        self.eFORTH = p_unity.FORTH.Engine()
        self.eFORTH_abi = {}

        self.connection = None
        self.statements = None
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

    def get_variable(self, name):
        return self.eFORTH.root.memory.get(name.lower(), 0)

    def set_variable(self, name, value):
        self.eFORTH.root.memory[name.lower()] = self.evaluate(value)

    def compare_variable(self, name, value):
        return -1 if self.eFORTH.root.memory[name.lower()] == value else 0

    def add_program_line(self, lineno, line):
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

        while True:
            if self.current_program_lineno is not None:
                current_line_index = linenos.index(self.current_program_lineno)

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

    def conditional(self, expr, then_statements, else_statement=None):
        if self.evaluate(expr):
            for statement in then_statements:
                self.execute(*statement)

        elif else_statement:
            self.execute(*else_statement)

    def noop(self):
        pass

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
        index = 0
        for result in results:
            self.eFORTH.root.memory[f"f{index}"] = result
            self.eFORTH_abi[f"f{index}"] = result
            index += 1

    def list(self):
        for lineno, line in sorted(self.program.items()):
            print(f'{lineno} {line}')

    def sql(self, *args):
        arg0 = self.evaluate(args[0])
        if self.connection == None:
            if self.statements == None:
                if arg0.upper() == "DECLARE":
                    self.statements = {}
            else:
                if arg0.upper() == "DECLARE_DONE":
                    import sqlite3
                    self.connection = sqlite3.connect("example.sqlite")
                    self.cursor = self.connection.cursor()
                else:
                    self.statements[arg0.lower()] = self.evaluate(args[1])
            return

        statement = self.statements[arg0.lower()]
        #self.cursor.execute(statement,(self.evaluate(arg) for arg in args[1:]))
        self.cursor.execute(statement)
        self.eFORTH.root.memory["sql"] = self.cursor.fetchall()

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
        PRINT,
        FORTH,
        SQL,
        IF,
        THEN,
        ELSE,
        LIST,
        RUN,
        END,
        GOTO,
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
        LPAREN,
        RPAREN
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

    def nocase_match(name):
        result = []
        for letter in name:
            result.append("[{0}{1}]".format(letter, letter.lower()))
        return r''.join(result)

    REM = r"(?:[Rr][Ee][Mm]|').*"
    PRINT = nocase_match("PRINT")
    FORMAT = nocase_match("FORMAT")
    FORTH = nocase_match("FORTH")
    SQL = nocase_match("SQL")
    IF = nocase_match("IF")
    THEN = nocase_match("THEN")
    ELSE = nocase_match("ELSE")
    LIST = nocase_match("LIST")
    RUN = nocase_match("RUN")
    END = nocase_match("END")
    GOTO = nocase_match("GOTO")

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

    @_(r"~.*?(?<!\\)(\\\\)*~")
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
    #debugfile = 'lamb.out'
    tokens = BasicLexer.tokens.union(LineLexer.tokens)
    precedence = (
        ('nonassoc', IF, THEN),
        ('left', COLON),
        ('nonassoc', ELSE),
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

    @_('LINENO')
    def statement(self, parsed):
        return Statement('remove_program_line', [parsed.LINENO])

    @_('IF expr THEN statements')
    def statement(self, parsed):
        return Statement('conditional', (parsed.expr, parsed.statements))

    @_('IF expr THEN statements ELSE statement')
    def statement(self, parsed):
        return Statement(
            'conditional',
            (parsed.expr, parsed.statements, parsed.statement),
        )

    @_('variable EQUALS expr')
    def statement(self, parsed):
        return Statement('set_variable', (parsed.variable.name, parsed.expr))

    @_('REM')
    def statement(self, parsed):
        return Statement('noop', [])

    @_('FORMAT exprs')
    def statement(self, parsed):
        return Statement('format', parsed.exprs)

    @_('SQL exprs')
    def statement(self, parsed):
        return Statement('sql', parsed.exprs)

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

    @_('expr %prec CREATE_EXPRS')
    def exprs(self, parsed):
        return [parsed.expr]

    @_('exprs expr %prec APPEND_EXPRS')
    def exprs(self, parsed):
        parsed.exprs.append(parsed.expr)
        return parsed.exprs

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

