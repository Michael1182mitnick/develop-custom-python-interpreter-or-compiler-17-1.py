# Develop a Custom Python Interpreter or Compiler
# Create a basic interpreter or compiler for a custom programming language with its own syntax and grammar.
# Parsing (Creating an Abstract Syntax Tree)

class ASTNode:
    pass


class BinOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class Number(ASTNode):
    def __init__(self, value):
        self.value = value


class Variable(ASTNode):
    def __init__(self, name):
        self.name = name


class Assign(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value


class Print(ASTNode):
    def __init__(self, expr):
        self.expr = expr


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def parse(self):
        statements = []
        while self.pos < len(self.tokens):
            statements.append(self.statement())
        return statements

    def statement(self):
        if self.current_token()[0] == 'LET':
            return self.assignment()
        elif self.current_token()[0] == 'PRINT':
            return self.print_statement()
        else:
            raise SyntaxError("Unknown statement")

    def assignment(self):
        self.expect('LET')
        name = self.expect('ID')[1]
        self.expect('ASSIGN')
        value = self.expr()
        self.expect('SEMICOLON')
        return Assign(name, value)

    def print_statement(self):
        self.expect('PRINT')
        self.expect('LPAREN')
        expr = self.expr()
        self.expect('RPAREN')
        self.expect('SEMICOLON')
        return Print(expr)

    def expr(self):
        left = self.term()
        while self.current_token() and self.current_token()[0] in ('PLUS', 'MINUS'):
            op = self.current_token()
            self.pos += 1
            right = self.term()
            left = BinOp(left, op, right)
        return left

    def term(self):
        left = self.factor()
        while self.current_token() and self.current_token()[0] in ('TIMES', 'DIVIDE'):
            op = self.current_token()
            self.pos += 1
            right = self.factor()
            left = BinOp(left, op, right)
        return left

    def factor(self):
        token = self.current_token()
        if token[0] == 'NUMBER':
            self.pos += 1
            return Number(token[1])
        elif token[0] == 'ID':
            self.pos += 1
            return Variable(token[1])
        elif token[0] == 'LPAREN':
            self.pos += 1
            expr = self.expr()
            self.expect('RPAREN')
            return expr
        else:
            raise SyntaxError("Unexpected token")

    def current_token(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def expect(self, token_type):
        token = self.current_token()
        if token is None or token[0] != token_type:
            raise SyntaxError(f"Expected {token_type}, got {token}")
        self.pos += 1
        return token


# Example usage:
tokens = tokenize(code)
parser = Parser(tokens)
ast = parser.parse()
