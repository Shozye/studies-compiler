from ..tac_models.models import Quadruple
from .validator import Validator


def validate(tac: dict[str, list[Quadruple]]):
    Validator().run(tac)
