#!/usr/bin/env python3
import re
import sys

# --- Lexer ---

# Token specifications: numbers, strings, identifiers, operators, punctuation, whitespace, and comments.
TOKEN_SPECIFICATION = [
    ('NUMBER',    r'\d+(\.\d+)?'),              # Integer or decimal number
    ('STRING',    r'"[^"]*"'),                  # String literal in double quotes
    ('IDENT',     r'[A-Za-z_][A-Za-z0-9_]*'),     # Identifiers
    ('OP',        r'\+|\-|\*|\/|%'),             # Arithmetic operators
    ('COMPARE',   r'==|!=|>=|<=|>|<'),           # Comparison operators
    ('ASSIGN',    r'='),                        # Assignment operator
    ('SEMICOLON', r';'),                        # Statement terminator
    ('LPAREN',    r'\('),                       # Left parenthesis
    ('RPAREN',    r'\)'),                       # Right parenthesis
    ('LBRACE',    r'\{'),                       # Left brace
    ('RBRACE',    r'\}'),                       # Right brace
    ('COMMA',     r','),                        # Comma (for function arguments etc.)
    ('NEWLINE',   r'\n'),                       # Newline
    ('SKIP',      r'[ \t]+'),                   # Skip spaces and tabs
    ('COMMENT',   r'\#.*'),                     # Comments starting with #
]

# Compile the regex patterns into one combined pattern.
token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPECIFICATION)
get_token = re.compile(token_regex).match

# Reserved keywords for Fourward.
KEYWORDS = {"let", "const", "if", "else", "while", "for", "function", "return", "print", "input", "true", "false", "null"}

class Token:
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column
    def __repr__(self):
        return f"Token({self.type}, {self.value})"

def tokenize(code):
    line_num = 1
    line_start = 0
    pos = 0
    tokens = []
    mo = get_token(code, pos)
    while mo:
        typ = mo.lastgroup
        value = mo.group(typ)
        if typ == 'NEWLINE':
            line_start = mo.end()
            line_num += 1
        elif typ in ('SKIP', 'COMMENT'):
            pass  # Ignore whitespace and comments.
        else:
            # If the token is an identifier, check if it's a reserved keyword.
            if typ == 'IDENT' and value in KEYWORDS:
                typ = value.upper()  # Keywords become their own token types (e.g., LET, IF, PRINT)
            tokens.append(Token(typ, value, line_num, mo.start()-line_start))
        pos = mo.end()
        mo = get_token(code, pos)
    tokens.append(Token('EOF', '', line_num, pos - line_start))
    return tokens

# --- AST (Abstract Syntax Tree) Nodes ---

class ASTNode:
    pass

class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements

class VarDecl(ASTNode):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

class Assignment(ASTNode):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

class PrintStatement(ASTNode):
    def __init__(self, expr):
        self.expr = expr

class IfStatement(ASTNode):
    def __init__(self, condition, then_branch, else_branch):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

class WhileStatement(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class Block(ASTNode):
    def __init__(self, statements):
        self.statements = statements

class BinaryOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class UnaryOp(ASTNode):
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand

class Number(ASTNode):
    def __init__(self, value):
        self.value = value

class String(ASTNode):
    def __init__(self, value):
        self.value = value

class Variable(ASTNode):
    def __init__(self, name):
        self.name = name

class FunctionCall(ASTNode):
    def __init__(self, name, args):
        self.name = name
        self.args = args

# --- Parser ---

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        return self.tokens[self.pos]

    def eat(self, token_type=None):
        token = self.current()
        if token_type and token.type != token_type:
            raise Exception(f"Expected token {token_type} but got {token.type}")
        self.pos += 1
        return token

    def parse(self):
        statements = []
        while self.current().type != 'EOF':
            stmt = self.statement()
            if stmt:
                statements.append(stmt)
        return Program(statements)

    def statement(self):
        token = self.current()
        if token.type == 'LET':
            return self.var_decl()
        elif token.type == 'IDENT':
            # Could be an assignment or a function call used as a statement.
            next_tok = self.tokens[self.pos+1]
            if next_tok.type == 'ASSIGN':
                return self.assignment()
            else:
                expr = self.expression()
                self.eat('SEMICOLON')
                return expr
        elif token.type == 'PRINT':
            return self.print_statement()
        elif token.type == 'IF':
            return self.if_statement()
        elif token.type == 'WHILE':
            return self.while_statement()
        elif token.type == 'LBRACE':
            return self.block()
        else:
            # Expression statement fallback.
            expr = self.expression()
            self.eat('SEMICOLON')
            return expr

    def var_decl(self):
        self.eat('LET')
        name = self.eat('IDENT').value
        self.eat('ASSIGN')
        expr = self.expression()
        self.eat('SEMICOLON')
        return VarDecl(name, expr)

    def assignment(self):
        name = self.eat('IDENT').value
        self.eat('ASSIGN')
        expr = self.expression()
        self.eat('SEMICOLON')
        return Assignment(name, expr)

    def print_statement(self):
        self.eat('PRINT')
        self.eat('LPAREN')
        expr = self.expression()
        self.eat('RPAREN')
        self.eat('SEMICOLON')
        return PrintStatement(expr)

    def if_statement(self):
        self.eat('IF')
        self.eat('LPAREN')
        condition = self.expression()
        self.eat('RPAREN')
        then_branch = self.block()
        else_branch = None
        if self.current().type == 'ELSE':
            self.eat('ELSE')
            else_branch = self.block()
        return IfStatement(condition, then_branch, else_branch)

    def while_statement(self):
        self.eat('WHILE')
        self.eat('LPAREN')
        condition = self.expression()
        self.eat('RPAREN')
        body = self.block()
        return WhileStatement(condition, body)

    def block(self):
        self.eat('LBRACE')
        statements = []
        while self.current().type != 'RBRACE':
            statements.append(self.statement())
        self.eat('RBRACE')
        return Block(statements)

    # --- Expression Parsing ---
    # The grammar supports binary operations with standard operator precedence.
    def expression(self):
        return self.equality()

    def equality(self):
        node = self.comparison()
        while self.current().type == 'COMPARE' and self.current().value in ('==', '!='):
            op = self.eat('COMPARE').value
            right = self.comparison()
            node = BinaryOp(node, op, right)
        return node

    def comparison(self):
        node = self.term()
        while self.current().type == 'COMPARE' and self.current().value in ('>', '<', '>=', '<='):
            op = self.eat('COMPARE').value
            right = self.term()
            node = BinaryOp(node, op, right)
        return node

    def term(self):
        node = self.factor()
        while self.current().type == 'OP' and self.current().value in ('+', '-'):
            op = self.eat('OP').value
            right = self.factor()
            node = BinaryOp(node, op, right)
        return node

    def factor(self):
        node = self.unary()
        while self.current().type == 'OP' and self.current().value in ('*', '/', '%'):
            op = self.eat('OP').value
            right = self.unary()
            node = BinaryOp(node, op, right)
        return node

    def unary(self):
        token = self.current()
        if token.type == 'OP' and token.value == '-':
            op = self.eat('OP').value
            operand = self.unary()
            return UnaryOp(op, operand)
        else:
            return self.primary()

    def primary(self):
        token = self.current()
        if token.type == 'NUMBER':
            self.eat('NUMBER')
            if '.' in token.value:
                return Number(float(token.value))
            else:
                return Number(int(token.value))
        elif token.type == 'STRING':
            self.eat('STRING')
            return String(token.value.strip('"'))
        elif token.type == 'IDENT':
            ident = self.eat('IDENT').value
            # Check if this is a function call.
            if self.current().type == 'LPAREN':
                self.eat('LPAREN')
                args = []
                if self.current().type != 'RPAREN':
                    args.append(self.expression())
                    while self.current().type == 'COMMA':
                        self.eat('COMMA')
                        args.append(self.expression())
                self.eat('RPAREN')
                return FunctionCall(ident, args)
            else:
                return Variable(ident)
        elif token.type == 'LPAREN':
            self.eat('LPAREN')
            node = self.expression()
            self.eat('RPAREN')
            return node
        else:
            raise Exception("Unexpected token: " + token.type)

# --- Interpreter ---

class Environment:
    def __init__(self, parent=None):
        self.vars = {}
        self.parent = parent

    def get(self, name):
        if name in self.vars:
            return self.vars[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            raise Exception(f"Undefined variable '{name}'")

    def set(self, name, value):
        if name in self.vars:
            self.vars[name] = value
        elif self.parent:
            self.parent.set(name, value)
        else:
            raise Exception(f"Undefined variable '{name}'")

    def define(self, name, value):
        self.vars[name] = value

class Interpreter:
    def __init__(self):
        self.global_env = Environment()
        # Define built-in functions.
        self.global_env.define("print", self.builtin_print)
        self.global_env.define("input", self.builtin_input)
        # Define built-in constants.
        self.global_env.define("true", True)
        self.global_env.define("false", False)
        self.global_env.define("null", None)

    def builtin_print(self, *args):
        print(*args)

    def builtin_input(self, prompt=""):
        return input(prompt)

    def eval(self, node, env=None):
        if env is None:
            env = self.global_env

        if isinstance(node, Program):
            for stmt in node.statements:
                self.eval(stmt, env)
        elif isinstance(node, VarDecl):
            value = self.eval(node.expr, env)
            env.define(node.name, value)
        elif isinstance(node, Assignment):
            value = self.eval(node.expr, env)
            env.set(node.name, value)
        elif isinstance(node, PrintStatement):
            value = self.eval(node.expr, env)
            print(value)
        elif isinstance(node, IfStatement):
            condition = self.eval(node.condition, env)
            if condition:
                self.eval(node.then_branch, Environment(env))
            elif node.else_branch:
                self.eval(node.else_branch, Environment(env))
        elif isinstance(node, WhileStatement):
            while self.eval(node.condition, env):
                self.eval(node.body, Environment(env))
        elif isinstance(node, Block):
            local_env = Environment(env)
            for stmt in node.statements:
                self.eval(stmt, local_env)
        elif isinstance(node, BinaryOp):
            left = self.eval(node.left, env)
            right = self.eval(node.right, env)
            if node.op == '+':
                # Handle string concatenation with type conversion
                if isinstance(left, str) or isinstance(right, str):
                    return str(left) + str(right)
                return left + right
            elif node.op == '-':
                return left - right
            elif node.op == '*':
                return left * right
            elif node.op == '/':
                return left / right
            elif node.op == '%':
                return left % right
            elif node.op == '==':
                return left == right
            elif node.op == '!=':
                return left != right
            elif node.op == '>':
                return left > right
            elif node.op == '<':
                return left < right
            elif node.op == '>=':
                return left >= right
            elif node.op == '<=':
                return left <= right
            else:
                raise Exception(f"Unknown binary operator '{node.op}'")
        elif isinstance(node, UnaryOp):
            operand = self.eval(node.operand, env)
            if node.op == '-':
                return -operand
            else:
                raise Exception(f"Unknown unary operator '{node.op}'")
        elif isinstance(node, Number):
            return node.value
        elif isinstance(node, String):
            return node.value
        elif isinstance(node, Variable):
            return env.get(node.name)
        elif isinstance(node, FunctionCall):
            func = env.get(node.name)
            args = [self.eval(arg, env) for arg in node.args]
            if callable(func):
                return func(*args)
            else:
                raise Exception(f"{node.name} is not a function")
        else:
            raise Exception("Unknown AST node")

def run(code):
    tokens = tokenize(code)
    parser = Parser(tokens)
    ast = parser.parse()
    interpreter = Interpreter()
    interpreter.eval(ast)

# --- Main Entry Point ---
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python fourward_interpreter.py <source_file>")
        sys.exit(1)
    with open(sys.argv[1], 'r') as f:
        code = f.read()
    run(code)
