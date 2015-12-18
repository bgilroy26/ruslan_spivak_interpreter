import sys
# Token types
# EOF indicates there is no more input
# CMD indicates command
INTEGER, PLUS, MINUS, MULT, DIV, CMD, EOF = 'INTEGER', 'PLUS', 'MINUS', 'MULT', 'DIV', 'CMD', 'EOF'  

ops = { 
    'PLUS': (lambda x,y: x+y),
    'MINUS': (lambda x,y: x-y),
    'MULT': (lambda x,y: x*y),
    'DIV': (lambda x,y: x/y)
    }

class Token(object):
    def __init__(self, type, value):
        # token type: INTEGER, PLUS, MINUS, CMD, or EOF
        self.type = type
        # token value: non-negative integer value, '+', '-', 'exit', or None
        self.value = value

    def __str__(self):
        """String representation of the class instance.

        Examples:
            Token(INTEGER, 3)
            Token(PLUS, '+')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()

class Interpreter(object):
    def __init__(self, text):
        # client string input, e.g. "3 + 5", "12-5", etc
        self.text = text
        # self.pos tracks position of lexer in self.text
        self.pos = 0
        # current token instance
        self.current_token = None
        self.current_char = self.text[self.pos]

    @staticmethod
    def error():
        raise Exception('Error parsing input')

    def advance(self):
        """Advance the 'pos' pointer and set the 'current_char' variable"""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        """Return a (multidigit) integer consumed from the input."""
        grabint_result = ''
        while self.current_char is not None and self.current_char.isdigit():
            grabint_result += self.current_char
            self.advance()
        return int(grabint_result)

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens. 
        """
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char == 'e':
                self.advance()
                if self.current_char == 'x':
                    self.advance()
                    if self.current_char == 'i':
                        self.advance()
                        if self.current_char == 't':
                             self.advance()
                             token = Token(CMD, 'exit')
                             return token

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MULT, '*')

            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')

            self.error()

        return Token(EOF, None)

    def eat(self, expected_token_type):
        # compare the current token type with expected
        # type and if they match then "eat" the current
        # token and assign the next to the 
        # self.current_token, otherwise raise exception
        if self.current_token.type == expected_token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        """Parse/Interpret

        expr -> CMD
        expr -> INTEGER PLUS INTEGER
        expr -> INTEGER MINUS INTEGER
        """
        # set current token to the first token taken from the input
        self.current_token = self.get_next_token()

        # we expect the current token to be an integer
        left = self.current_token
        if left.value == 'exit':
            sys.exit()
        self.eat(INTEGER)

        # we expect the current token to be either a '+ or a '-'
        op = self.current_token
        if op.type in [PLUS, MINUS, MULT, DIV]:
            self.eat(op.type)
        else:
            return result

        # we expect the current token to be an integer
        right = self.current_token
        self.eat(INTEGER)
        # after the above call, the self.current_token
        # is set to EOF token
 
        # at this point either the INTEGER PLUS INTEGER
        # or the INTEGER MINUS INTEGER sequence of tokens
        # has been successfully found and the method can
        # just return the result of adding or subtracting
        # two integers
        math_result = ops[op.type](left.value, right.value)
        while self.current_token.type != EOF:
            op = self.current_token
            if op.type in [PLUS, MINUS, MULT, DIV]:
                self.eat(op.type)
            else:
                return math_result
            right = self.current_token
            self.eat(INTEGER)

            math_result = ops[op.type](math_result, right.value)


        return math_result

        self.error()


def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        interpreter_result = interpreter.expr()
        print(interpreter_result)

if __name__ == '__main__':
    main()
