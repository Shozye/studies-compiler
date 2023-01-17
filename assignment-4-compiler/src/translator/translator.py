import copy
from collections import defaultdict
from pprint import pprint
from typing import Any

from .Flags import Flag
from .commands import SET, STORE, Command
from .constant_functions import get_multiply_information
from .procedure import ProcedureTranslator, VariableInfo, ProcedureInformation
from ..tac_models.models import Quadruple





class Translator:
    tac: dict[str, list[Quadruple]]
    translated_procedures: dict[str, ProcedureInformation]
    symbols: dict[str, dict[str, int]]
    translated_tac: list[Command]
    fully_translated_tac: list[Command]
    procedure_first_commands: dict[str, str]

    def __init__(self, tac: dict[str, list[Quadruple]]):
        self.tac = tac
        self.translated_procedures = dict()
        self.flags = set()
        self.translated_tac = list()
        self.fully_translated_tac = list()
        self.procedure_first_commands = dict()
        self.symbols = defaultdict(dict)
        self.free_memory_index = 1

    def translate_all(self):
        for proc, proc_tac in self.tac.items():
            procedure_translator = ProcedureTranslator(proc)
            procedure_translator.run(proc_tac)
            self.translated_procedures[proc] = procedure_translator.info
            self.flags.update(procedure_translator.info.flags)
        pprint(self.translated_procedures)
        self.set_global_symbols()
        self._join_all_procedures()
        self._translate_labels()

    def _translate_labels(self):
        labels = dict()
        for i, cmd in enumerate(self.translated_tac):
            if cmd.label != "":
                labels[cmd.label] = str(i)
        for i, cmd in enumerate(self.translated_tac):
            if cmd.arg.startswith("#"):
                cmd = Command("", cmd.directive, self.procedure_first_commands[cmd.arg[1:-1]])
            else:
                cmd = Command("", cmd.directive, labels.get(cmd.arg, cmd.arg))
            self.fully_translated_tac.append(cmd)

    def update_symbols(self, procedure: str, symbols: dict[str, VariableInfo]):
        for name in symbols:
            self.symbols[procedure][name] = self.get_free_index()

    def update_translated_tac(self, info: ProcedureInformation):
        self.procedure_first_commands[info.name] = str(len(self.translated_tac))
        for command in info.translated:
            copied = Command(command.label, command.directive, command.arg)
            if copied.directive in ["JUMP", "JPOS", "JZERO"] or copied.arg == "" or copied.arg.isdecimal() or copied.arg.startswith("E_"):
                pass
            elif copied.arg.startswith("*") and command.arg.endswith("*"):  # it means that it is global variable
                copied.arg = str(self.symbols["GLOBAL"][copied.arg])
            elif copied.arg.startswith("#"):  # it also means that it is STORE
                target_procedure, var_order = copied.arg[1:-1].split("#")
                copied.arg = str(self.symbols[target_procedure]["$ret"] + int(var_order))
            else:
                copied.arg = str(self.symbols[info.name][copied.arg])
            self.translated_tac.append(copied)

    def _join_all_procedures(self):
        new_translated_procedures = {"PROG": self.translated_procedures["PROG"]}
        for procname, info in self.translated_procedures.items():
            if procname != "PROG":
                new_translated_procedures[procname] = info
        self.translated_procedures = new_translated_procedures
        for name, info in self.translated_procedures.items():
            self.update_symbols(name, info.symbols)
        for info in self.translated_procedures.values():
            self.update_translated_tac(info)

    def get_free_index(self):
        free_index = self.free_memory_index
        self.free_memory_index += 1
        return free_index

    def set_global_symbols(self):
        self.symbols["GLOBAL"]["*SAVED_0*"] = 0
        if Flag.p1 in self.flags:
            self.symbols["GLOBAL"]["*SAVED_1*"] = self.get_free_index()
        if Flag.one in self.flags:
            self.symbols["GLOBAL"]["*one*"] = self.get_free_index()
            self.translated_tac.extend([SET("1"), STORE(str(self.symbols["GLOBAL"]["*one*"]))])
        if Flag.div in self.flags:
            pass
        if Flag.mul in self.flags:
            self.translated_procedures["!mul"] = get_multiply_information()
        if Flag.mod in self.flags:
            pass
