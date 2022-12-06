from lexer import CalcLexer
from parser import CalcParser

if __name__ == '__main__':
    lexer = CalcLexer()
    parser = CalcParser()
    while True:
        try:
            text = input('calc > ')
        except EOFError:
            break
        else:
            parser.parse(lexer.tokenize(text))