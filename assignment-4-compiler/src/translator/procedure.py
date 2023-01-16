from dataclasses import dataclass, field
from typing import Callable

from .Flags import Flag
from .commands import *
from ..tac_models.models import Quadruple, TAC


@dataclass
class VariableInfo:
    id: int
    is_param: bool = False


@dataclass
class ProcedureInformation:
    name: str
    symbols: dict[str, VariableInfo] = field(default_factory=dict)
    max_variable_index: int = -1
    flags: set[Flag] = field(default_factory=set)
    translated: list[Command] = field(default_factory=list)

    def add_param(self, param: str):
        self.max_variable_index += 1
        self.symbols[param] = VariableInfo(self.max_variable_index, True)

    def add_local(self, local: str):
        self.max_variable_index += 1
        self.symbols[local] = VariableInfo(self.max_variable_index, False)

    def _add_command(self, command: Command):
        self.translated.append(command)

    def add_commands(self, *params: Command):
        for command in params:
            self._add_command(command)


class ProcedureTranslator:
    def __init__(self, proc: str):
        self.info = ProcedureInformation(proc)

    def run(self, tacs: list[Quadruple]):
        func_mapping: dict[TAC, Callable] = {
            TAC.READ: self.read,
            TAC.WRITE: self.write,
            TAC.PARAM: self.param,
            TAC.LOCAL: self.local,
            TAC.CALL: self.call,
            TAC.RETURN: self.return_,
            TAC.IFGOTO: self.ifgoto,
            TAC.GOTO: self.goto,
            TAC.ASSIGN: self.assign
        }
        for tac in tacs:
            func_mapping[tac.type](tac)

    def param(self, tac: Quadruple):
        self.info.add_param(tac.arg1)

    def local(self, tac: Quadruple):
        self.info.add_local(tac.arg1)

    def read(self, tac: Quadruple):
        if self.info.symbols[tac.arg1].is_param:
            self.info.add_commands(GET("*SAVED_0*", tac.label), STOREI(tac.arg1))
        else:
            self.info.add_commands(GET(tac.arg1, tac.label))

    def write(self, tac: Quadruple):
        if tac.arg1.isdecimal():
            self.info.add_commands(SET(tac.arg1, tac.label), PUT("*SAVED_0*"))
        elif self.info.symbols[tac.arg1].is_param:
            self.info.add_commands(LOADI(tac.arg1, tac.label), PUT("*SAVED_0*"))
        else:
            self.info.add_commands(PUT(tac.arg1, tac.label))

    def call(self, tac: Quadruple):
        self.info.add_commands(SET(tac.arg2[0], tac.label),
                               STORE(f"#{tac.arg1}#{0}#"))
        for i, arg in enumerate(tac.arg2[1:], start=1):
            self.info.add_commands(SET(arg),
                                   STORE(f"#{tac.arg1}#{i}#"))
        self.info.add_commands(JUMP(f"#{tac.arg1}#"))

    def assign(self, tac: Quadruple):
        {"+": self.add, "-": self.sub, "*": self.mul, "/": self.div, "%": self.mod, "": self.nothing}[tac.op](tac)

    def nothing(self, tac: Quadruple):
        self.info.add_commands(
            SET(tac.arg1, tac.label) if tac.arg1.isdecimal() else self._GEN_LOAD(tac.arg1, tac.label),
            self._GEN_STORE(tac.res))

    def add(self, tac: Quadruple):
        self.info.add_commands(
            SET(tac.arg2, tac.label) if tac.arg2.isdecimal() else self._GEN_LOAD(tac.arg2, tac.label),
            self._GEN_ADD(tac.arg1),
            self._GEN_STORE(tac.res))

    def sub(self, tac: Quadruple):
        if tac.arg2.isdecimal():
            self.info.flags.add(Flag.p1)
            self.info.add_commands(SET(tac.arg2, tac.label),
                                   STORE("*SAVED_1*"),
                                   self._GEN_LOAD(tac.arg1),
                                   self._GEN_SUB("*SAVED_1*"))
        else:
            self.info.add_commands(self._GEN_LOAD(tac.arg1, tac.label),
                                   self._GEN_SUB(tac.arg2))
        self.info.add_commands(self._GEN_STORE(tac.res))

    def mul(self, tac: Quadruple):
        self.info.flags.add(Flag.mul)

    def div(self, tac: Quadruple):
        self.info.flags.add(Flag.div)

    def mod(self, tac: Quadruple):
        self.info.flags.add(Flag.mod)

    def ifgoto(self, tac: Quadruple):
        {">": self.grt, "<": self.les, ">=": self.geq, "<=": self.leq, "!=": self.neq}[tac.op](tac)

    def goto(self, tac: Quadruple):
        self.info.add_commands(JUMP(tac.res, tac.label))

    def return_(self, tac: Quadruple):
        self.info.add_commands(HALT(tac.label) if self.info.name == "PROG" else JUMPI("$ret", tac.label))

    def is_param(self, arg: str) -> bool:
        if arg.startswith("*") and arg.endswith("*"):
            return False
        return self.info.symbols[arg].is_param

    def _GEN(self, commandi, command, arg: str, label: str) -> Command:
        return commandi(arg, label) if self.is_param(arg) else command(arg, label)

    def _GEN_SUB(self, arg: str, label: str = "") -> Command:
        return self._GEN(SUBI, SUB, arg, label)

    def _GEN_ADD(self, arg: str, label: str = "") -> Command:
        return self._GEN(ADDI, ADD, arg, label)

    def _GEN_LOAD(self, arg: str, label: str = "") -> Command:
        return self._GEN(LOADI, LOAD, arg, label)

    def _GEN_STORE(self, arg: str, label: str = "") -> Command:
        return self._GEN(STOREI, STORE, arg, label)

    def _ADD_ONE(self) -> Command:
        self.info.flags.add(Flag.one)
        return ADD("*one*")

    def les(self, tac):
        self.info.add_commands(
            SET(tac.arg2, tac.label) if tac.arg2.isdecimal() else self._GEN_LOAD(tac.arg2, tac.label),
            self._GEN_SUB(tac.arg1),
            JPOS(tac.res))

    def geq(self, tac):
        self.info.add_commands(
            SET(tac.arg2, tac.label) if tac.arg2.isdecimal() else self._GEN_LOAD(tac.arg2, tac.label),
            self._GEN_SUB(tac.arg1),
            JZERO(tac.res))

    def grt(self, tac, add_label=True):
        label = tac.label if add_label else ""
        if tac.arg2.isdecimal():
            self.info.add_commands(SET(tac.arg2, label),
                                   self._ADD_ONE(),
                                   self._GEN_SUB(tac.arg1),
                                   JZERO(tac.res))
        else:
            self.info.add_commands(self._GEN_LOAD(tac.arg1, label),
                                   self._GEN_SUB(tac.arg2),
                                   JPOS(tac.res))

    def leq(self, tac):
        if tac.arg2.isdecimal():
            self.info.add_commands(SET(tac.arg2, tac.label),
                                   self._ADD_ONE(),
                                   self._GEN_SUB(tac.arg1),
                                   JPOS(tac.res))
        else:
            self.info.add_commands(self._GEN_LOAD(tac.arg1, tac.label),
                                   self._GEN_SUB(tac.arg2),
                                   JZERO(tac.res))

    def neq(self, tac):
        self.les(tac)
        self.grt(tac, add_label=False)
