#!/usr/bin/env python3
# -*- encoding: utf-8
# SPDX-License-Identifier: MIT
# Copyright (c) 2021 - 2021, Scott.McCallum@HQ.UrbaneINTER.NET

__banner__ = r""" (

           _____    _____   _____    _____    _______     __
  _   _   / ____|  / ____| |  __ \  |  __ \  |__   __|   / /
 (_) (_) | (___   | |      | |__) | | |__) |    | |     | |
          \___ \  | |      |  _  /  |  ___/     | |    / /
  _   _   ____) | | |____  | | \ \  | |         | |    \ \
 (_) (_) |_____/   \_____| |_|  \_\ |_|         |_|     | |
                                                         \_\
)







* see footer for upstream license information

"""  # __banner__

class Engine:  # { The Reference Implementation of FORTH^3 : p-unity }

    def __init__(self, run=None, run_tests=1, **kwargs):

        stack = kwargs.get('stack', [])
        memory = kwargs.get('memory', {})

        self.eFORTH = None
        self.eSCRPT = None



def standard_library():
    """
    Function that generates a dictionary that contains all the basic functions
    """
    env = Env()
    env.update({
        'is_float': lambda val: isinstance(val, Decimal),
        'is_int': lambda val: isinstance(val, int),
        'is_string': lambda val: isinstance(val, str),
        'is_list': lambda val: isinstance(val, list),
        'is_dict': lambda val: isinstance(val, dict),
        'is_bool': lambda val: isinstance(val, bool),
        'to_float': lambda val: float(val),
        'to_int': lambda val: int(val),
        'to_string': lambda val: str(val),
        'to_list': lambda val: list(val),
        'to_bool': lambda val: bool(val),
        'append': lambda lst, val: lst.append(val),
        'pop': lambda lst: lst.pop(),
        'pop_at': lambda lst, idx: lst.pop(idx),
        'extend': lambda lst1, lst2: lst1.extend(lst2),
        'len': lambda obj : len(obj),
        'ceil': lambda val : ceil(val),
        'floor': lambda val : floor(val),
        'abs': lambda val : abs(val),
        'sqrt': lambda val : sqrt(val),
        'pow': lambda base, exponent : pow(base, exponent),
        'log': lambda val : log(val),
        'exit': lambda val : exit(val),
        'trim': lambda val : val.strip(),
        'split': lambda val, delimeter=" " : val.split(delimeter),
        'print': lambda val : print(val),
    })
    return env


class Process:
    """
    The main process the executes O Abstract Syntax Tree
    """
    def __init__(self, tree, filename="?", env={}):
        self.tree = tree
        self.file_path = filename
        if not isinstance(env, Env):
            _env = env
            env = Env(outer=standard_library())
            env.update(_env)
        self.env = Env(outer=env)
        self.should_return = False
        self.depth = 0
        self.types  =  { 'int': int, 'float': float, 'string': str, 'bool': bool, 'list': list, 'dict': dict }
        self.rtypes = { int: 'int', float: 'float', str: 'string', bool: 'bool', list: 'list', dict: 'dict' }

    def run(self, tree=None, env={}):
        current_env = self.env
        result = None
        if env != {}:
            self.env = env
        if tree is None:
            for line in self.tree:
                try:
                    result = self.evaluate(line)
                except ValueError as e:
                    print(e)
                    break
                except UnboundLocalError as e:
                    print(e)
                    break
                except NameError as e:
                    print(e)
                    break
                except IndexError as e:
                    print(e)
                    break
                except TypeError as e:
                    print(e)
                    break
                if self.depth == 0:
                    self.should_return = False
                if self.should_return:
                    return result
        else:
            for line in tree:
                try:
                    result = self.evaluate(line)
                except ValueError as e:
                    print(e)
                    break
                except UnboundLocalError as e:
                    print(e)
                    break
                except NameError as e:
                    print(e)
                    break
                except IndexError as e:
                    print(e)
                    break
                except TypeError as e:
                    print(e)
                    break
                if self.depth == 0:
                    self.should_return = False
                if self.should_return:
                    return result
        self.env = current_env
        return result

    def stringify(self, expr):
        """
        Preparing values for printing
        """
        if type(expr) == dict:
            return str(expr)
        elif expr is None:
            return "nil"
        elif expr is True:
            return "true"
        elif expr is False:
            return "false"
        elif expr in self.rtypes:
            return self.rtypes[expr]
        return str(expr)

    def evaluate(self, parsed):
        """
        Evaluating a parsed tree/tuple/expression
        """
        if type(parsed) != tuple:
            return parsed
        else:
            action = parsed[0]
            if action == 'class_func_call':
                instance = self.env.find(parsed[1]).value
                method = instance.find_method(parsed[2])
                args = [self.evaluate(arg) for arg in parsed[3][1]]
                self.depth += 1
                res = method(*args)
                self.depth -= 1
                return res
            elif action == 'class':
                name = parsed[1]
                if name in self.env:
                    raise NameError('Cannot redefine variable \'%s\'' % name)
                    return None

                class_process = Process((), env=Env(self.env))

                for function in parsed[2][1]:
                    class_process.evaluate(function)

                # print(class_process.env)

                self.env.update({ name: OClass(name, class_process.env) })
            elif action == 'typeof':
                try:
                    if len(parsed[1]) == 2:
                        var = self.env.find(parsed[1][1])
                        return var.type
                    elif len(parsed[1]) == 3:
                        var = self.env.find(parsed[1][1][1])
                        index = self.evaluate(parsed[1][2])
                        return self.rtypes[type(var.value[index])]
                except TypeError as e:
                    return self.rtypes[type(parsed[1])]
            elif action == 'struct':
                name = parsed[1]
                if name in self.env:
                    raise NameError('Cannot redefine variable \'%s\'' % name)
                    return None

                fields = parsed[2]

                self.env.update({ name: { "__fields__": fields } })
            elif action == 'init_struct':
                name = parsed[1]
                struct_definition = self.env.find(name)
                if struct_definition is None:
                    raise UnboundLocalError('Struct %s is undefined' % name)
                    return None
                fields = struct_definition['__fields__']
                values = [self.evaluate(value) for value in parsed[2]]

                struct = {}
                for i in range(len(fields)):
                    if i < len(values):
                        if type(values[i]) != self.types[fields[i][1]]:
                            raise ValueError("Type for field '{}' should be '{}' but instead got '{}'".format(fields[i][0], fields[i][1], self.rtypes[type(values[i])]))
                        struct.update({ fields[i][0]: values[i] })
                    else:
                        struct.update({ fields[i][0]: None })

                return struct
            elif action == 'import':
                pass
                #base_dir = getenv('OPATH')
                #if base_dir is None:
                #    base_dir = dirname(__file__)
                #rel_path = 'include/' + parsed[1] + '.olang'
                #path = join(base_dir, rel_path)
                #if exists(path):
                #    fp = open(path)
                #    self.import_contents(fp.read())
            elif action == 'fn':
                params = parsed[2]
                body = parsed[3]
                self.env.update({parsed[1]: Function(
                    self, params[1], body, self.env)})
                return None
            elif action == 'call':
                func = self.env.find(parsed[1])
                if isinstance(func, Value):
                    func = func.get()

                if isinstance(func, OClass):
                    return func()
                elif not isinstance(func, Function):
                    if type(func) == type(lambda x: x):
                        args = [self.evaluate(arg) for arg in parsed[2][1]]
                        self.depth += 1
                        res = func(*args)
                        self.depth -= 1
                        return res
                    else:
                        raise ValueError('\'%s\' not a function' % parsed[1])

                args = [self.evaluate(arg) for arg in parsed[2][1]]
                self.depth += 1
                res = func(*args)
                self.depth -= 1
                return res

            elif action == 'lambda':
                body = parsed[2]
                params = parsed[1]
                return Function(self, params[1], body, self.env)

            elif action == 'return':
                result = self.evaluate(parsed[1])
                self.should_return = True
                return result

            elif action == 'var_define':
                name = parsed[1]
                if name in self.env:
                    raise NameError('Cannot redefine variable \'%s\'' % name)
                result = self.evaluate(parsed[2])
                self.env.update({name: Value(result, type(result))})
                return None
            elif action == 'var_define_no_expr':
                name = parsed[1]
                if name in self.env:
                    raise NameError('Cannot redefine variable \'%s\'' % name)
                self.env.update({name: Value(None, self.types[parsed[2]])})
                return None
            elif action == 'var_assign':
                if type(parsed[1]) is not tuple:
                    if parsed[1] not in self.env:
                        raise UnboundLocalError('Cannot assign to undefined variable \'%s\'' %
                              parsed[1])
                    result = self.evaluate(parsed[2])
                    var = self.env.find(parsed[1])
                    if type(result) != var.type:
                        raise ValueError("Type of variable '{}' should be '{}' but instead got '{}'".format(parsed[1], self.rtypes[var.type], self.rtypes[type(result)]))

                    # self.env.update({parsed[1]: result})
                    var.value = result
                    return None
                else:
                    var = self.evaluate(parsed[1][1])
                    index = self.evaluate(parsed[1][2])
                    value = self.evaluate(parsed[2])
                    var[index] = value
            elif action == 'if':
                cond = self.evaluate(parsed[1])
                if cond:
                    return self.evaluate(parsed[2])
                if parsed[3] is not None:
                    return self.evaluate(parsed[3])
            elif action == 'while':
                cond = self.evaluate(parsed[1])
                while cond:
                    self.evaluate(parsed[2])
                    cond = self.evaluate(parsed[1])
            elif action == 'condition':
                return self.evaluate(parsed[1])
            elif action == 'block':
                return self.run(parsed[1])
            elif action == 'var':
                var = self.env.find(parsed[1])
                if not isinstance(var, Value):
                    return var
                return var.value
            elif action == 'indexing':
                var = self.evaluate(parsed[1])
                index = self.evaluate(parsed[2])
                if index > len(var):
                    raise IndexError('Index out of bounds error')
                    return None
                elif type(index) != int:
                    raise IndexError('List indices must be integers')
                    return None
                return var[index]
            elif action == '+':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                return result + result2
            elif action == '-':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                return result - result2
            elif action == '*':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                return result * result2
            elif action == '/':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                return result / result2
            elif action == '%':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                return result % result2
            elif action == '==':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                return result == result2
            elif action == '!=':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                return result != result2
            elif action == '<':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                return result < result2
            elif action == '>':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                return result > result2
            elif action == '<=':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                return result <= result2
            elif action == '>=':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                return result >= result2
            elif action == '<<':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                return result << result2
            elif action == '>>':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                return result >> result2
            elif action == '&':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                return result & result2
            elif action == '^':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                return result ^ result2
            elif action == '|':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                return result | result2
            elif action == '~':
                result = self.evaluate(parsed[1])
                return ~result
            elif action == 'and':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                return result and result2
            elif action == 'or':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                return result or result2
            elif action == '!':
                result = self.evaluate(parsed[1])
                if result == True:
                    return False
                return True
            elif action == '?:':
                cond = self.evaluate(parsed[1])
                if cond:
                    return self.evaluate(parsed[2])
                return self.evaluate(parsed[3])
            elif action == '.':
                if type(parsed[1]) == tuple:
                    var = self.evaluate(parsed[1])
                else:
                    var = self.env.find(parsed[1])
                if isinstance(var, Value):
                    res = self.evaluate(var.value[parsed[2]])
                else:
                    res = self.evaluate(var[parsed[2]])
                return res

            else:
                if len(parsed) > 0 and type(parsed[0]) == tuple:
                    return self.run(parsed)

                print(parsed)
                return None

    def import_contents(self, file_contents):
        lexer = OLexer()
        parser = OParser()
        tokens = lexer.tokenize(file_contents)
        tree = parser.parse(tokens)
        program = Process(tree)
        program.run()
        self.env.update(program.env)

class Env(dict):
    """
    Environment Class
    """
    def __init__(self, params=(), args=(), outer=None):
        self.update(zip(params, args))
        self.outer = outer

    def find(self, name):
        if name in self:
            return self[name]
        elif self.outer is not None:
            return self.outer.find(name)

        raise UnboundLocalError("{} is undefined".format(name))


class Function(object):
    """
    Function object for O Functions and annoymous functions (lambdas)
    """
    def __init__(self, process, params, body, env):
        self.process, self.params, self.body, self.env = process, params, body, env
        self.type = 'function'

    def __call__(self, *args):
        params = []
        for i in range(len(self.params)):
            if type(args[i]) != self.process.types[self.params[i][1]]:
                raise TypeError("Type of parameter {} should be {} but got {}.".format(self.params[i][0], self.params[i][1], self.process.rtypes[type(args[i])]))
            params.append(self.params[i][0])
        return self.process.run(self.body, Env(params, args, self.env))

class Value(object):
    """
    Class container for values inside the O Language
    """
    def __init__(self, value, val_type):
        self.value = value
        self.type = val_type

    def __len__(self):
        return len(self.value)

    def __str__(self):
        return "{}: {}".format(self.value, self.type)

    def get(self):
        return self.value

class OClass(object):
    """
    Object for classes in O
    """
    def __init__(self, name, env):
        self.name = name
        self.env = env
        self.type = 'class'

    def __str__(self):
        return "<{} class>".format(self.name)

    def __call__(self):
        return OInstance(self)

class OInstance(object):
    """
    Object for instances of a class in O
    """
    def __init__(self, oclass):
        self.oclass = oclass
        self.type = 'instance'
        init_method = self.oclass.env.get('init')
        if init_method is not None:
            init_method()

    def __str__(self):
        return "<{} instance>".format(self.oclass.name)

    def find_method(self, name):
        return self.oclass.env.find(name)

from sly import Lexer

class OLexer(Lexer):
    """
    O language Lexer
    """
    tokens = {ID, INT, FLOAT, ASSIGN, STRING, LET,
              IF, ELSE, EQEQ, SEP, NOTEQ, LESS,
              GREATER, LESSEQ, GREATEREQ, NIL, WHILE,
              FOR, FN, RETURN, LAMBDA, ARROW, TRUE, FALSE,
              AND, OR, SHR, SHL, INC, DEC, PLUSASGN,
              MINUSASGN, STARASGN, SLASHASGN, MODULOASGN,
              ANDASGN, ORASGN, XORASGN, SHLASGN, SHRASGN,
              IMPORT, STRUCT, INT_TYPE, FLOAT_TYPE, BOOL_TYPE,
              LIST_TYPE, DICT_TYPE, STRING_TYPE, TYPEOF,
              LEFTARROW, PIPE, CLASS, DOUBLECOLON}
    ignore = ' \t'
    ignore_comment_slash = r'//.*'

    literals = {'=', '+', '-', '/', '*',
                '(', ')', ',', '{', '}',
                '%', '[', ']', '!', '&',
                '|', '^', '?', ':', '~',
                '.'}

    INC = r'\+\+'
    DEC = r'--'
    PIPE = r'\|>'
    PLUSASGN = r'\+='
    MINUSASGN = r'-='
    STARASGN = r'\*='
    SLASHASGN = r'/='
    MODULOASGN = r'%='
    ANDASGN = r'&='
    ORASGN = r'\|='
    XORASGN = r'^='
    SHLASGN = r'<<='
    SHRASGN = r'>>='
    ARROW = r'=>'
    LESSEQ = r'<='
    GREATEREQ = r'>='
    LEFTARROW = r'<-'
    SHR = r'>>'
    SHL = r'<<'
    LESS = r'<'
    GREATER = r'>'
    NOTEQ = r'!='
    EQEQ = r'=='
    ASSIGN = r'='
    SEP = r';'
    DOUBLECOLON = r'::'

    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['let'] = LET
    ID['if'] = IF
    ID['else'] = ELSE
    ID['nil'] = NIL
    ID['while'] = WHILE
    ID['for'] = FOR
    ID['fn'] = FN
    ID['return'] = RETURN
    ID['lambda'] = LAMBDA
    ID['true'] = TRUE
    ID['false'] = FALSE
    ID['and'] = AND
    ID['or'] = OR
    ID['import'] = IMPORT
    ID['struct'] = STRUCT
    ID['int'] = INT_TYPE
    ID['float'] = FLOAT_TYPE
    ID['string'] = STRING_TYPE
    ID['bool'] = BOOL_TYPE
    ID['list'] = LIST_TYPE
    ID['dict'] = DICT_TYPE
    ID['typeof'] = TYPEOF
    ID['class'] = CLASS

    @_(r'\d+\.\d+')
    def FLOAT(self, t):
        """
        Parsing float numbers
        """
        t.value = float(t.value)
        return t

    @_(r'\d+')
    def INT(self, t):
        """
        Parsing integers
        """
        t.value = int(t.value)
        return t

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

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)

    def error(self, t):
        print("Illegal character '%s' on line %d" % (t.value[0], self.lineno))
        self.index += 1

from sly import Parser

class OParser(Parser):
    """
    Parser for the O Language
    """
    tokens = OLexer.tokens

    precedence = (
        ('right', PLUSASGN, MINUSASGN, STARASGN, SLASHASGN,
         MODULOASGN, ANDASGN, ORASGN, XORASGN, SHLASGN, SHRASGN),
        ('left', OR),
        ('left', AND),
        ('left', '|'),
        ('left', '^'),
        ('left', '&'),
        ('left', EQEQ, NOTEQ),
        ('left', LESS, LESSEQ, GREATER, GREATEREQ),
        ('left', SHL, SHR),
        ('left', '+', '-'),
        ('left', '*', '/', '%'),
        ('right', 'UMINUS', 'UPLUS', 'LOGICALNOT', INC, DEC),
        ('right', '!'),
    )

    @_('statements')
    def program(self, p):
        return p.statements

    @_('empty')
    def program(self, p):
        return ()

    @_('statement')
    def statements(self, p):
        return (p.statement, )

    @_('statements statement')
    def statements(self, p):
        return p.statements + (p.statement, )

    @_('import_statement')
    def statement(self, p):
        return p.import_statement

    @_('function_definition')
    def statement(self, p):
        return p.function_definition

    @_('return_statement')
    def statement(self, p):
        return p.return_statement

    @_('while_statement')
    def statement(self, p):
        return p.while_statement

    @_('for_statement')
    def statement(self, p):
        return p.for_statement

    @_('if_statement')
    def statement(self, p):
        return p.if_statement

    @_('struct_definition')
    def statement(self, p):
        return p.struct_definition

    @_('class_definition')
    def statement(self, p):
        return p.class_definition

    @_('CLASS ID "{" function_definitions "}"')
    def class_definition(self, p):
        return ('class', p.ID, ('functions', p.function_definitions))

    @_('empty')
    def function_definitions(self, p):
        return []

    @_('function_definition')
    def function_definitions(self, p):
        return [p.function_definition]

    @_('function_definitions function_definition')
    def function_definitions(self, p):
        return p.function_definitions + [p.function_definition]

    @_('STRUCT ID "{" struct_fields "}" SEP')
    def struct_definition(self, p):
        return ('struct', p.ID, p.struct_fields)

    @_('struct_field')
    def struct_fields(self, p):
        return p.struct_field

    @_('struct_fields struct_field')
    def struct_fields(self, p):
        return p.struct_fields + p.struct_field

    @_('LET ID ":" var_type SEP')
    def struct_field(self, p):
        return [(p.ID, p.var_type)]

    @_('INT_TYPE')
    def var_type(self, p):
        return 'int'

    @_('FLOAT_TYPE')
    def var_type(self, p):
        return 'float'

    @_('STRING_TYPE')
    def var_type(self, p):
        return 'string'

    @_('BOOL_TYPE')
    def var_type(self, p):
        return 'bool'

    @_('LIST_TYPE')
    def var_type(self, p):
        return 'list'

    @_('DICT_TYPE')
    def var_type(self, p):
        return 'dict'

    @_('IMPORT STRING SEP')
    def import_statement(self, p):
        return ('import', p.STRING)

    @_('var_define SEP')
    def statement(self, p):
        return p.var_define

    @_('FN ID "(" params ")" block')
    def function_definition(self, p):
        return ('fn', p.ID, ('params', p.params), ('block', p.block))

    @_('ID LEFTARROW "{" struct_init_exprs "}" ')
    def expr(self, p):
        return ('init_struct', p.ID, p.struct_init_exprs)

    @_('expr')
    def struct_init_exprs(self, p):
        return [p.expr]

    @_('struct_init_exprs "," expr')
    def struct_init_exprs(self, p):
        return p.struct_init_exprs + [p.expr]

    @_('LAMBDA "(" params ")" ARROW expr')
    def expr(self, p):
        return ('lambda', ('params', p.params), ('block', ('return', p.expr)))

    @_('LET var ASSIGN expr')
    def var_define(self, p):
        return ('var_define', p.var, p.expr)

    @_('LET getter ASSIGN expr')
    def var_define(self, p):
        return ('var_define', p.getter, p.expr)

    @_('LET var ":" var_type SEP')
    def statement(self, p):
        return ('var_define_no_expr', p.var, p.var_type)

    @_('TYPEOF expr')
    def expr(self, p):
        return ('typeof', p.expr)

    @_('var_assign SEP')
    def statement(self, p):
        return p.var_assign

    @_('RETURN expr SEP')
    def return_statement(self, p):
        return ('return', p.expr)

    @_('var ASSIGN expr')
    def var_assign(self, p):
        return ('var_assign', p.var, p.expr)

    @_('var PLUSASGN expr')
    def var_assign(self, p):
        return ('var_assign', p.var, ('+', ('var', p.var), p.expr))

    @_('var MINUSASGN expr')
    def var_assign(self, p):
        return ('var_assign', p.var, ('-', ('var', p.var), p.expr))

    @_('var STARASGN expr')
    def var_assign(self, p):
        return ('var_assign', p.var, ('*', ('var', p.var), p.expr))

    @_('var SLASHASGN expr')
    def var_assign(self, p):
        return ('var_assign', p.var, ('/', ('var', p.var), p.expr))

    @_('var MODULOASGN expr')
    def var_assign(self, p):
        return ('var_assign', p.var, ('%', ('var', p.var), p.expr))

    @_('var ANDASGN expr')
    def var_assign(self, p):
        return ('var_assign', p.var, ('&', ('var', p.var), p.expr))

    @_('var ORASGN expr')
    def var_assign(self, p):
        return ('var_assign', p.var, ('|', ('var', p.var), p.expr))

    @_('var XORASGN expr')
    def var_assign(self, p):
        return ('var_assign', p.var, ('^', ('var', p.var), p.expr))

    @_('var SHLASGN expr')
    def var_assign(self, p):
        return ('var_assign', p.var, ('<<', ('var', p.var), p.expr))

    @_('var SHRASGN expr')
    def var_assign(self, p):
        return ('var_assign', p.var, ('>>', ('var', p.var), p.expr))

    @_('IF expr block ELSE block')
    def if_statement(self, p):
        return ('if', ('condition', p.expr), ('block', p.block0), ('block', p.block1))

    @_('IF expr block')
    def if_statement(self, p):
        return ('if', ('condition', p.expr), ('block', p.block), None)

    @_('WHILE expr block')
    def while_statement(self, p):
        return ('while', ('condition', p.expr), ('block', p.block))

    @_('FOR var_assign SEP expr SEP var_assign block')
    def for_statement(self, p):
        return (p.var_assign0, ('while', ('condition', p.expr), ('block', p.block + (p.var_assign1, ))))

    @_('expr "?" expr ":" expr')
    def expr(self, p):
        return ('?:', p.expr0, p.expr1, p.expr2)

    @_('ID "(" args ")"')
    def expr(self, p):
        return ('call', p.ID, ('args', p.args))

    @_('ID DOUBLECOLON ID "(" args ")"')
    def expr(self, p):
        return ('class_func_call', p.ID0, p.ID1, ('args', p.args))

    @_('expr PIPE ID "(" args ")"')
    def expr(self, p):
        return ('call', p.ID, ('args', [p.expr] + p.args))

    @_('expr EQEQ expr')
    def expr(self, p):
        return ('==', p.expr0, p.expr1)

    @_('expr NOTEQ expr')
    def expr(self, p):
        return ('!=', p.expr0, p.expr1)

    @_('expr LESSEQ expr')
    def expr(self, p):
        return ('<=', p.expr0, p.expr1)

    @_('expr GREATEREQ expr')
    def expr(self, p):
        return ('>=', p.expr0, p.expr1)

    @_('expr AND expr')
    def expr(self, p):
        return ('and', p.expr0, p.expr1)

    @_('expr OR expr')
    def expr(self, p):
        return ('or', p.expr0, p.expr1)

    @_('expr LESS expr')
    def expr(self, p):
        return ('<', p.expr0, p.expr1)

    @_('expr GREATER expr')
    def expr(self, p):
        return ('>', p.expr0, p.expr1)

    @_('expr SHL expr')
    def expr(self, p):
        return ('<<', p.expr0, p.expr1)

    @_('expr SHR expr')
    def expr(self, p):
        return ('>>', p.expr0, p.expr1)

    @_('expr "&" expr')
    def expr(self, p):
        return ('&', p.expr0, p.expr1)

    @_('expr "^" expr')
    def expr(self, p):
        return ('^', p.expr0, p.expr1)

    @_('expr "|" expr')
    def expr(self, p):
        return ('|', p.expr0, p.expr1)

    @_('"~" expr %prec LOGICALNOT')
    def expr(self, p):
        return ('~', p.expr)

    @_('expr SEP')
    def statement(self, p):
        return p.expr

    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return ('neg', p.expr)

    @_('"+" expr %prec UPLUS')
    def expr(self, p):
        return p.expr

    @_('"!" expr')
    def expr(self, p):
        return ('!', p.expr)

    @_('INC var')
    def var_assign(self, p):
        return ('var_assign', p.var, ('+', ('var', p.var), 1))

    @_('DEC var')
    def var_assign(self, p):
        return ('var_assign', p.var, ('-', ('var', p.var), 1))

    @_('expr "+" expr')
    def expr(self, p):
        return ('+', p.expr0, p.expr1)

    @_('expr "-" expr')
    def expr(self, p):
        return ('-', p.expr0, p.expr1)

    @_('expr "*" expr')
    def expr(self, p):
        return ('*', p.expr0, p.expr1)

    @_('expr "/" expr')
    def expr(self, p):
        return ('/', p.expr0, p.expr1)

    @_('expr "%" expr')
    def expr(self, p):
        return ('%', p.expr0, p.expr1)

    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr

    @_('INT')
    def expr(self, p):
        return p.INT

    @_('FLOAT')
    def expr(self, p):
        return p.FLOAT

    @_('STRING')
    def expr(self, p):
        return p.STRING

    @_('TRUE')
    def expr(self, p):
        return True

    @_('FALSE')
    def expr(self, p):
        return False

    @_('list_val')
    def expr(self, p):
        return p.list_val

    @_('"[" exprs "]"')
    def list_val(self, p):
        return p.exprs

    @_('empty')
    def exprs(self, p):
        return []

    @_('expr')
    def exprs(self, p):
        return [p.expr]

    @_('exprs "," expr')
    def exprs(self, p):
        return p.exprs + [p.expr]

    @_('var "[" expr "]"')
    def expr(self, p):
        return ('indexing', ('var', p.var), p.expr)

    @_('var')
    def expr(self, p):
        return ('var', p.var)

    @_('ID')
    def var(self, p):
        return p.ID

    @_('var "[" expr "]"')
    def var(self, p):
        return ('indexing', ('var', p.var), p.expr)

    @_('NIL')
    def expr(self, p):
        return None

    @_('')
    def empty(self, p):
        pass

    @_('"{" program "}"')
    def block(self, p):
        return p.program

    @_('statement')
    def block(self, p):
        return (p.statement, )

    @_('params "," param')
    def params(self, p):
        return p.params + [p.param]

    @_('param')
    def params(self, p):
        return [p.param]

    @_('empty')
    def params(self, p):
        return []

    @_('ID ":" var_type')
    def param(self, p):
        return (p.ID, p.var_type)

    @_('args "," arg')
    def args(self, p):
        return p.args + [p.arg]

    @_('arg')
    def args(self, p):
        return [p.arg]

    @_('empty')
    def args(self, p):
        return []

    @_('expr')
    def arg(self, p):
        return p.expr

    @_('"{" member_list "}"')
    def expr(self, p):
        return p.member_list

    @_('empty')
    def member_list(self, p):
        return {}

    @_('member')
    def member_list(self, p):
        return p.member

    @_('member_list "," member')
    def member_list(self, p):
        return { **p.member_list, **p.member }

    @_('STRING ":" expr')
    def member(self, p):
        return { p.STRING : p.expr }

    @_('getter "." ID')
    def getter(self, p):
        return ('.', p.getter, p.ID)

    @_('ID')
    def getter(self, p):
        return p.ID

    @_('getter')
    def expr(self, p):
        return p.getter


from decimal import Decimal
from math import ceil, floor, sqrt, log

import p_unity.FORTH
import p_unity.BASIC

#
# https://github.com/oransimhony/o/blob/master/LICENSE
#
# MIT License
#
# Copyright (c) 2019 Oran Simhony
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
