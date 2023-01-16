from typing import Optional

from .cfg_models import BasicBlock, OutEdge, ProceduralEdge
from ..tac_models.utils import get_tac_repr


def write_to_file(
    nodes: dict[str, list[BasicBlock]],
    inner_edges: dict[str, dict[int, Optional[OutEdge]]],
    procedural_edges: dict[tuple[str, int], str],
    path: str
):
    max_label = 0
    for proc in nodes:
        lbb = nodes[proc]
        for bb in lbb:
            for tac in bb.tacs:
                max_label = max(max_label, len(tac.label))
    with open(path, 'w+') as file:
        for proc in nodes:
            lbb = nodes[proc]
            edges = inner_edges[proc]
            file.write(f"===== {proc} =====\n")
            for bb in lbb:
                file.write(f"{bb}")
                file.write("" if edges[bb.index] is None else f" {edges[bb.index]}")
                file.write(f" {procedural_edges[(proc, bb.index)]}"
                           if procedural_edges.get((proc, bb.index)) is not None else "")
                file.write("\n")
                for tac in bb.tacs:
                    file.write(f"{get_tac_repr(tac, max_label)}\n")
