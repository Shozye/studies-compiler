import enum
from dataclasses import dataclass
from typing import Union


class TAC(enum.Enum):
    # commands
    READ = "READ"
    WRITE = "WRITE"
    PARAM = "PARAM"
    LOCAL = "LOCAL"
    RETURN = "RETURN"
    CALL = "CALL"
    # flow
    IFGOTO = "IFGOTO"
    GOTO = "GOTO"
    # others
    ASSIGN = "ASSIGN"
    LABEL = "LABEL"


@dataclass
class Quadruple:
    type: TAC
    op: str = ""
    arg1: str = ""
    arg2: Union[str, list[str]] = ""
    res: str = ""
    label: str = ""


class LabelTAC(Quadruple):
    def __init__(self, label: str):
        super().__init__(type=TAC.LABEL, label=label)


class ReadTAC(Quadruple):
    def __init__(self, arg: str, label: str = ""):
        super().__init__(type=TAC.READ, op=TAC.READ.name, arg1=arg, label=label)


class WriteTAC(Quadruple):
    def __init__(self, arg: str, label: str = ""):
        super().__init__(type=TAC.WRITE, op=TAC.WRITE.name, arg1=arg, label=label)


""" ======================= FUNCTIONS TAC ======================= """


class ParamTAC(Quadruple):
    def __init__(self, arg: str, label: str = ""):
        super().__init__(type=TAC.PARAM, op=TAC.PARAM.name, arg1=arg, label=label)


class LocalTAC(Quadruple):
    def __init__(self, arg: str, label: str = ""):
        super().__init__(type=TAC.LOCAL, op=TAC.LOCAL.name, arg1=arg, label=label)


class ReturnTAC(Quadruple):
    def __init__(self, label: str = ""):
        super().__init__(type=TAC.RETURN, op=TAC.RETURN.name, label=label)


class CallTAC(Quadruple):
    def __init__(self, arg: str, params: list[str], label: str = ""):
        super().__init__(type=TAC.CALL, op=TAC.CALL.name, arg1=arg, arg2=params, label=label)


""" ==================== FUNCTIONS TAC END ====================== """


class GotoTAC(Quadruple):
    def __init__(self, res: str, label: str = ""):
        super().__init__(type=TAC.GOTO, res=res, label=label)


class AssignTAC(Quadruple):
    def __init__(self, res: str, arg1: str, op: str = "", arg2: str = "", label: str = ""):
        super().__init__(type=TAC.ASSIGN, res=res, arg1=arg1, op=op, arg2=arg2, label=label)


class IfGotoTAC(Quadruple):
    def __init__(self, res: str, arg1: str, op: str, arg2: str, label: str = ""):
        super().__init__(type=TAC.IFGOTO, res=res, arg1=arg1, op=op, arg2=arg2, label=label)
