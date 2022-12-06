from lexer import CalcLexer
from sly import Parser
from utils import *

P = 1234577

class CalcParser(Parser):
    tokens = CalcLexer.tokens

    precedence = (
        ('left', ADD, SUB),
        ('left', MUL, DIV),
        ('right', UMINUS),
        ('nonassoc', POW)
        )

    def __init__(self):
        self.notation = ""

    @_('line statement')
    def statement(self, p):
        pass

    @_('')
    def statement(self, p):
        pass
    
    @_('expr NEWLINE')
    def line(self, p):
        print(f"Notation: {self.notation}\nResult: {p.expr}")
        self.notation=""

    @_('NEWLINE')
    def line(self, p):
        pass

    @_('number')
    def expr(self, p):
        self.notation += str(p.number)
        return p.number

    @_('NUM')
    def number(self, p):
        return p.NUM % P
    
    @_('SUB number %prec UMINUS')
    def number(self, p):
        return neg(-p.number)
    

    


