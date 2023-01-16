from sly import Parser

from .gebalang_lexer import GebalangLexer
from src.tac_models.labels import Labels
from src.tac_models.models import (
    AssignTAC,
    IfGotoTAC, GotoTAC,
    WriteTAC, ReadTAC, CallTAC, ReturnTAC, LocalTAC, ParamTAC, Quadruple, LabelTAC
)
from .parser_returntypes import P


class GebalangParser(Parser):
    tokens = GebalangLexer.tokens
    tac: dict[str, list[Quadruple]]
    cond_negate: dict[str, str]
    cond_reverse: dict[str, str]

    def __init__(self):
        self.tac = {}
        self.cond_negate = {">": "<=", "<=": ">",
                            "<": ">=", ">=": "<",
                            "=": "!=", "!=": "="}
        self.cond_reverse = {">": "<", "<=": ">=",
                             "<": "<", ">=": "<=",
                             "=": "=", "!=": "!="}
        self.labels = Labels()

    @_('procedures main')
    def program_all(self, p: P):
        self.tac = p.procedures
        self.tac.update(p.main)

    @_('main')
    def program_all(self, p: P):
        """This is program without any procedures"""
        self.tac = p.main

    @_('procedures procedure')
    def procedures(self, p: P) -> dict[str, list[Quadruple]]:
        _tac = p.procedures
        _tac.update(p.procedure)
        return _tac

    @_('procedure')
    def procedures(self, p: P) -> dict[str, list[Quadruple]]:
        return p.procedure

    @_('PROCEDURE proc_head IS local_variables BEGIN commands END')
    def procedure(self, p: P) -> dict[str, list[Quadruple]]:
        """This procedure should somehow connect proc_head with declarations and commands together"""
        name, declarations = p.proc_head
        _tac = [ParamTAC("$ret")]
        _tac.extend((ParamTAC(declaration) for declaration in declarations))
        _tac.extend((LocalTAC(var) for var in p.local_variables))
        _tac.extend(p.commands)
        _tac.append(ReturnTAC())
        return {name: _tac}

    @_('PROGRAM IS local_variables BEGIN commands END')
    def main(self, p: P) -> dict[str, list[Quadruple]]:
        _tac = []
        _tac.extend((LocalTAC(var) for var in p.local_variables))
        _tac.extend(p.commands)
        _tac.append(ReturnTAC())

        return {"PROG": _tac}

    @_('VAR declarations')
    def local_variables(self, p: P) -> list[str]:
        return p.declarations

    @_('')
    def local_variables(self, p) -> list[str]:
        return []

    @_('commands command')
    def commands(self, p: P) -> list[Quadruple]:
        _tac = p.commands
        _tac.extend(p.command)
        return _tac

    @_('command')
    def commands(self, p: P) -> list[Quadruple]:
        """Shouldn't it be the same as command"""
        return p.command

    @_('ID ASSIGN expression SEMICOLON')
    def command(self, p: P) -> list[Quadruple]:
        return [AssignTAC(p.ID, *p.expression)]

    @_('IF condition THEN commands ELSE commands ENDIF')
    def command(self, p: P) -> list[Quadruple]:
        ifclosed_etiquette = self.labels.get_ifclosed()
        _tac = p.condition[0]
        _tac.extend(p.commands0)
        _tac.append(GotoTAC(ifclosed_etiquette))
        _tac.append(LabelTAC(p.condition[2]))
        _tac.extend(p.commands1)
        _tac.append(LabelTAC(ifclosed_etiquette))

        return _tac

    @_('IF condition THEN commands ENDIF')
    def command(self, p: P) -> list[Quadruple]:
        _tac = p.condition[0]
        _tac.extend(p.commands)
        _tac.append(LabelTAC(p.condition[2]))
        return _tac

    @_('WHILE condition DO commands ENDWHILE')
    def command(self, p: P) -> list[Quadruple]:
        _tac = p.condition[0]
        _tac.extend(p.commands)
        _tac.append(GotoTAC(p.condition[1]))
        _tac.append(LabelTAC(p.condition[2]))
        return _tac

    @_('REPEAT commands UNTIL condition SEMICOLON')
    def command(self, p: P) -> list[Quadruple]:
        _tac = [LabelTAC(p.condition[2])]
        _tac.extend(p.commands)
        _tac.extend(p.condition[0])
        return _tac

    @_('proc_head SEMICOLON')
    def command(self, p: P) -> list[Quadruple]:
        return_etiquette = self.labels.get_return()
        name, declarations = p.proc_head
        _tac = [CallTAC(name, [return_etiquette] + declarations),
                LabelTAC(return_etiquette)]
        return _tac

    @_('READ ID SEMICOLON')
    def command(self, p: P) -> list[Quadruple]:
        return [ReadTAC(p.ID)]

    @_('WRITE value SEMICOLON')
    def command(self, p: P) -> list[Quadruple]:
        return [WriteTAC(p.value)]

    @_('ID LPAR declarations RPAR')
    def proc_head(self, p: P) -> tuple[str, list[str]]:
        return p.ID, p.declarations

    @_('declarations COMMA ID')
    def declarations(self, p: P) -> list[str]:
        decs = p.declarations
        return decs + [p.ID]

    @_('ID')
    def declarations(self, p: P) -> list[str]:
        return [p.ID]

    @_('value')
    def expression(self, p: P) -> tuple[str, str, str]:

        return p.value, "", ""

    @_('value ARIT_OP value')
    def expression(self, p: P) -> tuple[str, str, str]:
        val0, arit_op, val1 = p.value0, p.ARIT_OP, p.value1
        if val0.isdecimal() and val1.isdecimal():
            if arit_op == "/":
                arit_op = "//"
            evaluated = eval(f"{val0} {arit_op} {val1}")
            if arit_op == "-":
                evaluated = max(evaluated, 0)
            return evaluated, "", ""

        if val0.isdecimal() and arit_op in ["+", "*"]:
            val0, val1 = val1, val0

        if arit_op in ["+", "-"] and val1 == "0":
            arit_op, val1 = "", ""
        elif arit_op in ["*", "/"] and val1 == "1":
            arit_op, val1 = "", ""
        elif (arit_op == "*" and val1 == "0") or (arit_op == "%" and val1 == "1"):
            val0, arit_op, val1 = "0", "", ""

        return val0, arit_op, val1

    @_('value COND_OP value')
    def condition(self, p: P) -> tuple[list[Quadruple], str, str]:
        val0, cond_op, val1 = p.value0, p.COND_OP, p.value1
        cond_op = self.cond_negate[cond_op]
        taut = None
        if val0.isdecimal() and val1.isdecimal():
            taut = eval(f"{val0} {cond_op} {val1}")
        if val0 == val1:
            taut = cond_op in ["=", ">=", "<="]
        if val0.isdecimal():
            val0, cond_op, val1 = val1, self.cond_reverse[cond_op], val0
        if val1 == "0":
            if cond_op == "<":
                taut = False
            elif cond_op == ">=":
                taut = True

        cond_etiquette = self.labels.get_cond()
        aftergoto_etiquette = self.labels.get_aftergoto()
        gotocond_etiquette = self.labels.get_gotocond()
        _tac: list[Quadruple] = []
        if cond_op != "=":
            if taut is not None:
                _tac = [GotoTAC(gotocond_etiquette, cond_etiquette)] if taut else [LabelTAC(cond_etiquette)]
            else:
                _tac = [IfGotoTAC(gotocond_etiquette, val0, cond_op, val1, cond_etiquette)]
        else:
            if val1 != "0":
                _tac = [IfGotoTAC(aftergoto_etiquette, val0, "<", val1, cond_etiquette)]
            _tac.append(IfGotoTAC(gotocond_etiquette, val0, "<=", val1, cond_etiquette))
        _tac.append(LabelTAC(aftergoto_etiquette))
        return _tac, cond_etiquette, gotocond_etiquette

    @_('NUM')
    def value(self, p: P) -> str:
        return p.NUM

    @_('ID')
    def value(self, p: P) -> str:
        return p.ID
