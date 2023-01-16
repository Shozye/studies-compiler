from typing import Optional

from .cfg_models import BasicBlock, OutEdge, ProceduralEdge
from .utils import write_to_file
from ..tac_models.models import Quadruple, TAC


def _get_leaders(tacs: list[Quadruple]) -> list[int]:
    """Leaders are the starting points of basic blocks. TAC is a leader iff it is one of the following:
    1. The first statement of program or procedure.
    2. Statement that is target of a conditional or unconditional GOTO statement # every target has label
    3. Statement that immediately follows a conditional or unconditional GOTO statement
    4. Statement that immediately follows a method invocation statement # all of them have return label
    credits. page 423"""
    leaders = set()
    leaders_label = []
    labels = dict()
    for i, tac in enumerate(tacs):
        if not leaders:
            leaders.add(i)  # 1.
        if tac.type in [TAC.GOTO, TAC.IFGOTO, TAC.CALL]:
            leaders.add(i + 1)  # 3. 4.
            if tac.type != TAC.CALL:
                leaders_label.append(tac.res)  # 2a.

        if tac.label:
            labels[tac.label] = i  # helper to 2
    for label in leaders_label:
        leaders.add(labels[label])  # 2b.

    return sorted(list(leaders))


class CFG:
    """Class represents Procedure Control Flow Graph of one process
    credits: https://www.researchgate.net/publication/273445077_Designing_and_Implementing_Control_Flow_Graph_for_Magic_4th_Generation_Language"""
    nodes: dict[int, BasicBlock]  # basic blocks with their indexes
    edges: dict[int, Optional[OutEdge]]  # edge is between two basic blocks id's
    outer_procedural_edges: list[tuple[int, str]]  # edge is between block_id and procedure_name

    def __init__(self, tacs: list[Quadruple]):
        """ We make CFG by finding leaders of TAC, and then we create basic blocks by
        starting with leader and extending up to the next leader.
        @param tacs: list of tacs that start with proc_start and end with ReturnTAC
        """
        self.nodes = {}
        self._make_nodes(tacs)
        start_label_to_basic_block = {}
        self.edges = {}
        self.outer_procedural_edges = []
        for i, node in self.nodes.items():
            label = node.tacs[0].label
            if label:
                start_label_to_basic_block[label] = i

        for i, node in self.nodes.items():
            last = node.tacs[-1]
            if last.type == TAC.RETURN:
                self.edges[i] = None
            elif last.type == TAC.IFGOTO:
                self.edges[i] = OutEdge(start_label_to_basic_block[last.res], i + 1, last.op, last.arg1, last.arg2)
            elif last.type == TAC.GOTO:
                self.edges[i] = OutEdge(start_label_to_basic_block[last.res])
            elif last.type == TAC.CALL:
                self.edges[i] = OutEdge(i + 1)
                self.outer_procedural_edges.append((i, last.arg1))
            else:
                self.edges[i] = OutEdge(i + 1)  # case when there was some loop

    def _make_nodes(self, tacs):
        leaders = _get_leaders(tacs)
        for i, leader_index in enumerate(leaders):
            last_index = leaders[i + 1] if i + 1 < len(leaders) else len(tacs)
            self.nodes[i] = BasicBlock(i, tacs[leader_index:last_index])

    def get_tac(self) -> list[Quadruple]:
        tac = []
        for node in self.nodes.values():
            tac.extend(node.tacs)
        return tac


class ICFG:
    """Class represents InterProcedural Control Flow Graph
    credits: https://www.researchgate.net/publication/273445077_Designing_and_Implementing_Control_Flow_Graph_for_Magic_4th_Generation_Language"""
    cfgs: dict[str, CFG]  # key: procedure name
    procedural_edges: list[ProceduralEdge]

    def __init__(self, tacs: dict[str, list[Quadruple]], output_dir: str, filename: str):
        self.cfgs = {proc_name: CFG(tac) for proc_name, tac in tacs.items()}
        self.procedural_edges = self._make_procedural_edges()

        write_to_file({key: self.cfgs[key].nodes.values() for key in self.cfgs},
                      {key: self.cfgs[key].edges for key in self.cfgs},
                      {(pedge.proc1, pedge.node1): pedge for pedge in self.procedural_edges},
                      f"{output_dir}/{filename}.mr")

    def get_tac(self) -> dict[str, list[Quadruple]]:
        return {proc: cfg.get_tac() for proc, cfg in self.cfgs.items()}

    def _make_procedural_edges(self) -> list[ProceduralEdge]:
        proc_edges = []
        for proc_name, cfg in self.cfgs.items():
            for out_edge in cfg.outer_procedural_edges:
                proc_edges.append(ProceduralEdge(proc_name, *out_edge))
        return proc_edges
