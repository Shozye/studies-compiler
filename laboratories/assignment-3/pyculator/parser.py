from lexer import CalcLexer
from sly import Parser

class CalcParser(Parser):
    tokens = CalcLexer.tokens

    precedence = (
        ('left', ADD, SUB),
        ('left', MUL, DIV),
        ('left', NEG),
        ('nonassoc', POW)
        )

    def __init__(self):
        self.notation = ""

    @_('statement line')
    def statement(self, p):
        pass
    @_('')
    def statement(self, p):
        pass
    
    @_('expr NEWLINE')
    def line(self, p):
        print(f"Notation: {self.notation}\nResult: {p.expr0}")

    @_('NUM')
    def expr(self, p):
        self.notation
        return p.NUM

    @_('expr "+" expr')
    def expr(self, p):
        return p.expr0 + p.expr1

    @_('expr "-" expr')
    def expr(self, p):
        return p.expr0 - p.expr1

    @_('expr "*" expr')
    def expr(self, p):
        return p.expr0 * p.expr1

    @_('expr "/" expr')
    def expr(self, p):
        return p.expr0 / p.expr1

    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return -p.expr

    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr

    @_('NUMBER')
    def expr(self, p):
        return p.NUMBER

    @_('NAME')
    def expr(self, p):
        try:
            return self.names[p.NAME]
        except LookupError:
            print("Undefined name '%s'" % p.NAME)
            return 0
        
