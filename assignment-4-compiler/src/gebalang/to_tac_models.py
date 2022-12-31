from typing import Optional


class BaseTAC:
    LABEL_PAD = 10
    EXPR_PAD = 1
    ASSIGN_PAD = 1
    COMMAND_PAD = 6
    ID_PAD = 1

    def __init__(
        self,
        label: Optional[str]
    ):
        self.label = label

    def __repr__(self):
        label = self.label
        BaseTAC.LABEL_PAD = max(BaseTAC.LABEL_PAD, len(label))

        return f"{label.ljust(BaseTAC.LABEL_PAD, ' ')} | "


class ExprTAC(BaseTAC):
    def __init__(
        self,
        res: str,
        op: str,
        arg1: str,
        arg2: str,
        label: Optional[str]
    ):
        super().__init__(label)
        self.res = res
        self.arg1 = arg1
        self.op = op
        self.arg2 = arg2

    def __repr__expr__(self):
        s = f"{self.arg1} {self.op} {self.arg2}".strip()
        BaseTAC.EXPR_PAD = max(len(s), BaseTAC.EXPR_PAD)
        return s.ljust(BaseTAC.EXPR_PAD, " ")


class FlowTAC(ExprTAC):

    def __init__(
        self,
        res: str,
        op: str = "",
        arg1: str = "",
        arg2: str = "",
        label: str = ""
    ):
        super().__init__(res, op, arg1, arg2, label)

    def __repr__(self):
        if self.arg1 == "":
            return f"{super().__repr__()}GOTO {self.res}"
        return f"{super().__repr__()}IF {self.__repr__expr__()} GOTO {self.res}"


class AssignTAC(ExprTAC):
    def __init__(
        self,
        res: str,
        op: str,
        arg1: str,
        arg2: str,
        label: str = ""
    ):
        super().__init__(res, op, arg1, arg2, label)

    def __repr__(self):
        label = super().__repr__()
        assign = self.res.ljust(BaseTAC.ASSIGN_PAD, " ")
        BaseTAC.ASSIGN_PAD = max(BaseTAC.ASSIGN_PAD, len(assign))
        return f"{label}{self.res} := {self.__repr__expr__()}"


class CommandTAC(BaseTAC):
    def __init__(
        self,
        command: str,
        identifier: str,
        label: str = ""
    ):
        super().__init__(label)
        self.command = command
        self.identifier = identifier

    def __repr__(self):
        label = super().__repr__()
        command = self.command.ljust(BaseTAC.COMMAND_PAD, ' ')
        identifier = self.identifier.ljust(BaseTAC.ID_PAD, ' ')
        BaseTAC.COMMAND_PAD = max(BaseTAC.COMMAND_PAD, len(command))
        BaseTAC.ID_PAD = max(BaseTAC.ID_PAD, len(identifier))
        return f"{label}{command} {identifier}"


class PushTAC(CommandTAC):
    def __init__(
        self,
        identifier: str,
        label: str = ""
    ):
        super().__init__("PUSH", identifier, label)


class WriteTAC(CommandTAC):
    def __init__(
        self,
        identifier: str,
        label: str = ""
    ):
        super().__init__("WRITE", identifier, label)


class ReadTAC(CommandTAC):
    def __init__(
        self,
        identifier: str,
        label: str = ""
    ):
        super().__init__("READ", identifier, label)


class CallTAC(CommandTAC):
    def __init__(
        self,
        identifier: str,
        label: str = ""
    ):
        super().__init__("CALL", identifier, label)


class ParamTAC(CommandTAC):
    def __init__(
        self,
        identifier: str,
        label: str = ""
    ):
        super().__init__("PARAM", identifier, label)


class LocalTAC(CommandTAC):
    def __init__(
        self,
        identifier: str,
        label: str = ""
    ):
        super().__init__("LOCAL", identifier, label)


class ReturnTAC(CommandTAC):
    def __init__(self, label: str = ""):
        super().__init__("RETURN", '', label)

