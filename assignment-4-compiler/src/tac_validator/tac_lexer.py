from sly import Lexer


class TACLexer(Lexer):
    tokens = {NEWLINE, ETIQUETTE, PROCNAME,
              VARIABLE, DELIMITER,
              ASSIGN, ARIT_OP, COND_OP,
              IF, GOTO, NUM,
              PUSH, WRITE, READ, CALL, PARAM, LOCAL, RETURN}
    ignore = " "
    DELIMITER = r"\|"
    NEWLINE = r"\n"
    ETIQUETTE = r"E_[A-Z]+_[0-9]+"
    PROCNAME = r"P_[a-zA-Z]+"
    VARIABLE = r"[_a-z]+|\$.*"
    NUM = r"[0-9]+"

    # flow
    IF = r"IF"
    GOTO = r"GOTO"

    # commands
    READ = r"READ"
    WRITE = r"WRITE"
    LOCAL = r"LOCAL"
    PARAM = r"PARAM"
    RETURN = r"RETURN"
    PUSH = r"PUSH"
    CALL = r"CALL"

    # operators
    ASSIGN = r":="
    ARIT_OP = r"\+|-|\*|/|%"
    COND_OP = r">=|<=|>|<|!=|="

    def error(self, t):
        print('Line %d: Bad character %r' % (self.lineno, t.value[0]))
        raise Exception("xd")

