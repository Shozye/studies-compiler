from ..tac_models.models import Quadruple


class BasicBlock:
    """Class represents block of code that always follows from first to last line without any jumps and branching"""

    def __init__(self, index: int, tacs: list[Quadruple]):
        self.index = index
        self.tacs = tacs

    def __repr__(self):
        return f"BasicBlock(id={self.index}, len(tacs)={len(self.tacs)})"


class OutEdge:
    def __init__(self, if_true: int, if_false: int = -1, op: str = "", arg1: str = "", arg2: str = ""):
        self.if_true = if_true
        self.if_false = if_false
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2

    def __repr__(self):
        if self.if_false != -1:
            return f"OutEdge({self.if_true}, {self.if_false})"
        return f"OutEdge({self.if_true})"


class ProceduralEdge:
    def __init__(self, proc1: str, node1: int, proc2: str):
        self.proc1 = proc1
        self.node1 = node1
        self.proc2 = proc2

    def __repr__(self):
        return f"ProceduralEdge( {self.proc1}, {self.node1} -> {self.proc2}) )"
