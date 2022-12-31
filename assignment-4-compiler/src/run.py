from gebalang.gebalang_lexer import GebalangLexer
from gebalang.gebalang_parser import GebalangParser

if __name__ == '__main__':
    with open("scratch.imp") as file:
        data = file.read()
    lexer = GebalangLexer()
    for token in list(lexer.tokenize(data)):
        print(token)
    parser = GebalangParser()
    parser.parse(lexer.tokenize(data))
    new_text = ""
    with open("scratch.tac", 'w+') as file:
        for code in parser.tac:
            print(str(code))
            file.write(str(code) + "\n")
            new_text += str(code) + "\n"
    #run_lexer(new_text)

