#!/usr/bin/env python3
# -*- encoding: utf-8


__banner__ = r""" ( Copyright Intermine.com.au Pty Ltd. or its affiliates.
                    License SPDX: Programming-Unity-10.42 or as negotiated.

  __    ___     ____                _____   _____    _____
 /_ |  / _ \   |  _ \      /\      / ____| |_   _|  / ____|     _     _
  | | | | | |  | |_) |    /  \    | (___     | |   | |        _| |_ _| |_
  | | | | | |  |  _ <    / /\ \    \___ \    | |   | |       |_   _|_   _|
  | | | |_| |  | |_) |  / ____ \   ____) |  _| |_  | |____     |_|   |_|
  |_|  \___/   |____/  /_/    \_\ |_____/  |_____|  \_____|



)




"""  # __banner__


class Engine: # { The Reference Implementation of BASIC++ : p-unity }

    def __init__(self, run_tests=None):
        self.program = {}
        self.lexer = BasicLexer()
        self.parser = BasicParser(self)
        self.datastack = collections.deque()
        self.callstack = collections.deque()
        self.variables = collections.defaultdict(int)
        self.variables_nocase = {}
        self.running_program = False

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

        if isinstance(return_value, float):
            int_return_value = int(return_value)
            return_value = (
                int_return_value
                if math.isclose(int_return_value, return_value)
                else return_value
            )

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

    def call_len(self, value):
        return len(value)

    def call_variable(self, name, value):

        if name.lower() == 'lower':
            return str(value).lower()

        return None

    def get_variable(self, name):
        name = self.variables_nocase[name.lower()]
        return self.variables.get(name, 0)

    def set_variable(self, name, value):
        self.variables[name] = self.evaluate(value)
        self.variables_nocase[name.lower()] = name

    def compare_variable(self, name, value):
        name = self.variables_nocase[name.lower()]
        return -1 if self.variables[name] == value else 0

    def add_program_line(self, lineno, line):
        self.program[lineno] = line

    def remove_program_line(self, lineno):
        self.program.pop(lineno, None)

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

    def push(self, *args):
        for arg in args:
            self.datastack.append(self.evaluate(arg))

    def pop(self, *args):
        return self.datastack.pop()

    def top(self, *args):
        return self.datastack[-1]

    def depth(self, *args):
        return len(self.datastack)

    def print(self, *args):
        print(*(self.evaluate(arg) for arg in args))

    def list(self):
        for lineno, line in sorted(self.program.items()):
            print(f'{lineno} {line}')

import collections
import math

from sly.lex import Lexer, Token
from sly.yacc import Parser

Variable = collections.namedtuple('Variable', ['name'])
Expression = collections.namedtuple('Expression', ['operation', 'arguments'])
Statement = collections.namedtuple('Statement', ['operation', 'arguments'])

class BasicLexer(Lexer):
    tokens = {
        ID,
        REM,
        PRINT,
        IF,
        THEN,
        ELSE,
        LIST,
        RUN,
        GOTO,
        STRING,
        LINENO,
        NUMBER,
        PLUS,
        MINUS,
        MULTIPLY,
        DIVIDE,
        EQUALS,
        COLON,
        LBRACKET,
        RBRACKET,
        LEN, POP, TOP, DEPTH,
        LET, PUSH,
    }

    ignore = ' \t\n'
    ignore_comment = r'\#.*'

    PLUS = r'\+'
    MINUS = r'-'
    MULTIPLY = r'\*'
    DIVIDE = r'/'
    EQUALS = r'='
    COLON = r':'

    def nocase_match(name):
        result = []
        for letter in name:
            result.append("[{0}{1}]".format(letter, letter.lower()))
        return r''.join(result)

    REM = r"(?:REM|').*"
    PRINT = nocase_match("PRINT")
    IF = nocase_match("IF")
    THEN = nocase_match("THEN")
    ELSE = nocase_match("ELSE")
    LIST = nocase_match("LIST")
    RUN = nocase_match("RUN")
    GOTO = nocase_match("GOTO")

    LET = nocase_match("LET")
    PUSH = nocase_match("PUSH")

    LEN = nocase_match("LEN")
    POP = nocase_match("POP")
    TOP = nocase_match("TOP")
    DEPTH = nocase_match("DEPTH")

    LBRACKET = r'\('
    RBRACKET = r'\)'

    ID = r'[A-Za-z_][A-Za-z0-9_]*'

    @_(r'(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)')
    def NUMBER(self, token):
        if(
            self.index
            and self.text[:token.index] != token.index * ' '
        ):
            float_value = float(token.value)
            int_value = int(float_value)
            token.value = (
                int_value
                if math.isclose(int_value, float_value)
                else float_value
            )

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

    @_(r'"[^"]*"?')
    def STRING(self, token):
        token.value = token.value[1:]

        if token.value.endswith('"'):
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
        ('nonassoc', IF, THEN, LET, PUSH),
        ('left', COLON),
        ('nonassoc', ELSE),
        ('left', EQUALS),
        ('left', CREATE_EXPRS, APPEND_EXPRS),
        ('left', PLUS, MINUS),
        ('left', MULTIPLY, DIVIDE),
        ('nonassoc', UNARY_MINUS),
        ('left', LEN, POP, TOP, DEPTH),
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

    @_('LET variable EQUALS expr')
    def statement(self, parsed):
        return Statement('set_variable', (parsed.variable.name, parsed.expr))

    @_('variable EQUALS expr')
    def statement(self, parsed):
        return Statement('set_variable', (parsed.variable.name, parsed.expr))

    @_('REM')
    def statement(self, parsed):
        return Statement('noop', [])

    @_('PRINT exprs')
    def statement(self, parsed):
        return Statement('print', parsed.exprs)

    @_('PUSH exprs')
    def statement(self, parsed):
        return Statement('push', parsed.exprs)


    @_('LIST')
    def statement(self, parsed):
        return Statement('list', [])

    @_('RUN')
    def statement(self, parsed):
        return Statement('run_program', [])

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

    @_('LEN expr')
    def expr(self, parsed):
        return Expression('call_len',[parsed.expr])

    #@_('PUSH expr')
    #def expr(self, parsed):
    #    return Expression('push',[parsed.expr])

    @_('POP')
    def expr(self, parsed):
        return Expression('pop', [parsed[0]])

    @_('TOP')
    def expr(self, parsed):
        return Expression('top', [parsed[0]])

    @_('DEPTH')
    def expr(self, parsed):
        return Expression('depth', [parsed[0]])

    @_('variable EQUALS expr')
    def expr(self, parsed):
        return Expression(
            'compare_variable',
            [parsed.variable.name, parsed.expr],
        )

    @_('MINUS expr %prec UNARY_MINUS')
    def expr(self, parsed):
        return Expression('negative', [parsed.expr])

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

    @_('LBRACKET expr RBRACKET')
    def expr(self, parsed):
        return parsed.expr

    @_(
        'NUMBER',
        'STRING',
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

