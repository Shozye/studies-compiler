from .cfg import ICFG
from ..tac_models.models import Quadruple


class Optimiser:
    def __init__(self, tac: dict[str, list[Quadruple]], output_dir: str, filename: str):
        self.icfg = ICFG(tac, output_dir, filename)

    def get_tac(self) -> dict[str, list[Quadruple]]:
        return self.icfg.get_tac()

