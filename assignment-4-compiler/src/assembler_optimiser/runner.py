from .EquivalenceLoadAddSwapper import EquivalenceLoadAddSwapper
from .RedundantLoadOptimiser import RedundantLoadOptimiser
from .RedundantSet0Optimiser import RedundantSet0Optimiser
from ..control_flow_graph.cfg import ICFG


def optimise_assembler(icfg: ICFG):
    RedundantLoadOptimiser(icfg).optimise()
    EquivalenceLoadAddSwapper(icfg).swap()
    RedundantLoadOptimiser(icfg).optimise()
    EquivalenceLoadAddSwapper(icfg).swap()
    RedundantLoadOptimiser(icfg).optimise()
    RedundantSet0Optimiser(icfg).optimise()


