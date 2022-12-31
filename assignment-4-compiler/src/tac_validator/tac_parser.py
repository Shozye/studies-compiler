from sly import Parser
from .tac_lexer import TACLexer


def get_default_procedure_template():
    return {
        "params": [],
        "local": [],
        "used": [],
        "calls": []
    }

class TACParser(Parser):
    tokens = TACLexer.tokens

    def __init__(self):
        self.procs = {}

    @_("procedures")
    def program(self, p):
        pass

    @_("procedures procedure")
    def procedures(self, p):
        pass

    @_("")
    def procedures(self, p):
        pass

    @_("procline commands retline")
    def procedure(self, p):
        pass


