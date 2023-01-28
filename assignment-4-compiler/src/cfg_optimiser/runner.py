from .DeadCodeRemover import DeadCodeRemover
from ..control_flow_graph.cfg import ICFG


def optimise_icfg(icfg: ICFG):
    optimisers = [DeadCodeRemover]
    for optimiser in optimisers:
        current = optimiser(icfg)
        current.optimise()

