import sys
# Token Types
#
# EOF token is used to indicate that there is 
# no more input left for lexical analysis

INTEGER, PLUS, EOF = 'INTEGER', 'PLUS', 'EOF'
CMD = 'CMD'

class Token(object):
    def __init__(self, type, value):
        #token type: INTEGER, PLUS, or EOF 
        self.type = type
        #token value: decimal digit, '+', e,x,i,t, or None
        self.value = value

    def __str__(self):
        """String representation of the class instance

        Examples:
            Token(Integer, 3)
            Token(PLUS, '+')
        """

        return 'Token ({type}, {value})'.format(
                type=self.type,
                value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


class Interpreter(object):
    def __init__(self, text):
        # client string input, e.g. "3+5"
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        #current token instance
        self.current_token = None

    def error(self):
        raise Exception('Error parsing input')

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence apart
        into tokens. One token at a time.
        """
        text = self.text
        print(text)

        # is self.pos index past the end of the self.text?
        # if so, return EOF token, because input is finished
        if self.pos > len(text) - 1:
            return Token(EOF, None)

        # get a character at the position self.pos and decide
        # what token to create based on the single character
        current_char = text[self.pos]

        # if the character is a digit then convert it to
        # integer, create an INTEGER token, increment self.pos
        # index to point to the next character after the digit,
        # and return the INTEGER token
        if current_char == ' ':
            self.pos += 1
            return self.get_next_token()

        if current_char.isdigit():
            number = current_char
            print(number)
            
            while text[self.pos+1].isdigit():
                number += text[self.pos+1]
                self.pos += 1
                if self.pos > len(text)-2:
                    break

            token = Token(INTEGER, int(number))
            self.pos += 1
            return token

        if current_char == '+':
            token = Token(PLUS, current_char)
            self.pos += 1
            return token

        if current_char == 'e':
            self.pos += 1
            current_char = text[self.pos]
            if current_char == 'x':
                self.pos += 1
                current_char = text[self.pos]
                if current_char == 'i':
                    self.pos += 1
                    current_char = text[self.pos]
                    if current_char == 't':
                        current_char = text[self.pos]

                        token = Token(CMD, 'exit')
                        self.pos += 1
                        return token

        self.error()

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match, then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise, raise an exception
        print("current token type", self.current_token.type)
        print("passed token type", token_type)
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr2(self):
        """expr2 -> e,x,i,t"""
        self.current_token = self.get_next_token()
        command = self.current_token
        self.eat(CMD)
        print(command)
        sys.exit()

    def expr(self):
        """expr -> INTEGER PLUS INTEGER"""
        # set current token to the first token taken from the input
        self.current_token = self.get_next_token()

        # we expect the current token to be a single-digit integer
        left = self.current_token
        self.eat(INTEGER)

        # we expect the current token to be a '+' token
        op = self.current_token
        self.eat(PLUS)
        
        # we expect the current token to be a single-digit integer
        right = self.current_token
        self.eat(INTEGER)
        # after the above call, the self.current_token is set to
        # EOF token

        # return the result of adding two integers, thus
        # effectively interpreting client input
        print(left)
        print(op)
        print(right)
        result = left.value + right.value
        return result

def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        if text[0].isdigit():
            result = interpreter.expr()
        if text[0] == 'e':
            result = interpreter.expr2()
        print(result)

if __name__ == '__main__':
    main()
