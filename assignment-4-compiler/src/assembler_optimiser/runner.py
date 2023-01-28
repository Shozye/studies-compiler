from .RedundantLoadOptimiser import RedundantLoadOptimiser
from ..control_flow_graph.cfg import ICFG


def optimise_assembler(icfg: ICFG):
    optimisers = [RedundantLoadOptimiser]
    for optimiser in optimisers:
        current = optimiser(icfg)
        current.optimise()
