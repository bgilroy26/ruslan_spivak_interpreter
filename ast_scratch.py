INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, EOF = (
            'INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', '(', ')', 'EOF'
            )

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

class AST(object):
    pass

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token, self.op = op, op
        self.right = right

class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value
