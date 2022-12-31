from typing import Union
from sly import Parser

from .gebalang_lexer import GebalangLexer
from .tac_labels import Labels
from .to_tac_models import (
    BaseTAC,
    FlowTAC, AssignTAC,
    CommandTAC, WriteTAC, ReadTAC, PushTAC, CallTAC, ReturnTAC, LocalTAC, ParamTAC
)


def proc_etiquette(name):
    return f"P_{name}"


class GebalangParser(Parser):
    tokens = GebalangLexer.tokens
    tac: list[Union[AssignTAC, FlowTAC, CommandTAC]]

    def __init__(self):
        self.tac = []
        self.cond_reverse = {"<=": ">", ">=": "<", "<": ">=", ">": "<=", "=": "!=", "!=": "="}
        self.labels = Labels()

    @_('procedures main')
    def program_all(self, p):
        """here should be something like gather the three address code bitch"""
        self.tac = p.procedures
        self.tac.extend(p.main)

    @_('main')
    def program_all(self, p):
        """This is program without any procedures"""
        self.tac = p.main

    @_('procedures procedure')
    def procedures(self, p):
        _tac = p.procedures
        _tac.extend(p.procedure)
        return _tac

    @_('procedure')
    def procedures(self, p):
        return p.procedure

    @_('PROCEDURE proc_head IS local_variables BEGIN commands END')
    def procedure(self, p):
        """This procedure should somehow connect proc_head with declarations and commands together"""
        name, declarations = p.proc_head
        _tac = [BaseTAC(proc_etiquette(name))]
        for var in declarations:
            _tac.append(ParamTAC(var))
        _tac.append(ParamTAC("$ret"))
        for var in p.local_variables:
            _tac.append(LocalTAC(var))
        _tac.extend(p.commands)
        _tac.append(ReturnTAC())
        return _tac

    @_('PROGRAM IS local_variables BEGIN commands END')
    def main(self, p):
        _tac = [BaseTAC(proc_etiquette("PROG"))]
        for var in p.local_variables:
            _tac.append(LocalTAC(var))
        _tac.extend(p.commands)
        _tac.append(ReturnTAC())
        return _tac

    @_('VAR declarations')
    def local_variables(self, p):
        return p.declarations

    @_('')
    def local_variables(self, p):
        return []

    @_('commands command')
    def commands(self, p):
        _tac = p.commands
        _tac.extend(p.command)
        return _tac

    @_('command')
    def commands(self, p):
        """Shouldn't it be the same as command"""
        return p.command

    @_('ID ASSIGN expression SEMICOLON')
    def command(self, p):
        return [AssignTAC(p.ID, *p.expression)]

    @_('IF condition THEN commands ELSE commands ENDIF')
    def command(self, p):
        else_etiquette = self.labels.get_else()
        endif_etiquette = self.labels.get_endif()
        _tac = [FlowTAC(else_etiquette, *p.condition, self.labels.get_if())]
        _tac.extend(p.commands0)
        _tac.append(FlowTAC(endif_etiquette))
        _tac.append(BaseTAC(else_etiquette))
        _tac.extend(p.commands1)
        _tac.append(BaseTAC(endif_etiquette))
        return _tac

    @_('IF condition THEN commands ENDIF')
    def command(self, p):
        endif_etiquette = self.labels.get_endif()
        _tac = [FlowTAC(endif_etiquette, *p.condition, self.labels.get_if())]
        _tac.extend(p.commands)
        _tac.append(BaseTAC(endif_etiquette))
        return _tac

    @_('WHILE condition DO commands ENDWHILE')
    def command(self, p):
        while_etiquette = self.labels.get_while()
        endwhile_etiquette = self.labels.get_endwhile()
        _tac = [FlowTAC(endwhile_etiquette, *p.condition, while_etiquette)]
        _tac.extend(p.commands)
        _tac.append(FlowTAC(while_etiquette))
        _tac.append(BaseTAC(endwhile_etiquette))
        return _tac

    @_('REPEAT commands UNTIL condition SEMICOLON')
    def command(self, p):
        repeat_etiquette = self.labels.get_repeat()
        _tac = [BaseTAC(repeat_etiquette)]
        _tac.extend(p.commands)
        _tac.append(FlowTAC(repeat_etiquette, *p.condition, self.labels.get_until()))
        return _tac

    @_('proc_head SEMICOLON')
    def command(self, p):
        name, declarations = p.proc_head
        _tac = []
        for declaration in declarations:
            _tac.append(PushTAC(declaration))
        return_etiquette = self.labels.get_return()
        _tac.append(PushTAC(return_etiquette))
        _tac.append(CallTAC(proc_etiquette(name)))
        _tac.append(BaseTAC(return_etiquette))
        return _tac

    @_('READ ID SEMICOLON')
    def command(self, p):
        return [ReadTAC(p.ID)]

    @_('WRITE value SEMICOLON')
    def command(self, p):
        return [WriteTAC(p.value)]

    @_('ID LPAR declarations RPAR')
    def proc_head(self, p):
        return p.ID, p.declarations

    @_('declarations COMMA ID')
    def declarations(self, p):
        decs = p.declarations
        return decs + [p.ID]

    @_('ID')
    def declarations(self, p):
        return [p.ID]

    @_('value')
    def expression(self, p):
        return "", p.value, ""

    @_('value ARIT_OP value')
    def expression(self, p):
        return p.ARIT_OP, p.value0, p.value1

    @_('value COND_OP value')
    def condition(self, p):
        return self.cond_reverse[p.COND_OP], p.value0, p.value1

    @_('NUM')
    def value(self, p):
        return p.NUM

    @_('ID')
    def value(self, p):
        return p.ID
