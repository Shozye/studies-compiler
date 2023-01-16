import os
from collections import defaultdict

from ..tac_models.utils import write_to_file
from ..tac_models.models import Quadruple, TAC
from .gebalang_lexer import GebalangLexer
from .gebalang_parser import GebalangParser


def _clear_labels(tacs: dict[str, list[Quadruple]]) -> dict[str, list[Quadruple]]:
    new_tacs = defaultdict(list)
    next_label_index = 0
    for proc, proc_tacs in tacs.items():
        labels: dict[str, str] = dict()

        for i in range(len(proc_tacs)):
            tac = proc_tacs[i]
            if tac.label:
                if tac.label not in labels:
                    labels[tac.label] = f"E_{next_label_index}"
                    next_label_index += 1

            if tac.type in [TAC.GOTO, TAC.IFGOTO]:
                if tac.res not in labels:
                    labels[tac.res] = f"E_{next_label_index}"
                    next_label_index += 1
            if tac.type == TAC.LABEL:  # and i < len(proc_tacs) - 1 but every procedure ends with return
                next_tac = proc_tacs[i + 1]
                if not next_tac.label:
                    next_tac.label = tac.label
                elif next_tac.label not in labels:
                    labels[next_tac.label] = labels[tac.label]

        for tac in proc_tacs:
            if tac.type in [TAC.GOTO, TAC.IFGOTO]:
                tac.res = labels[tac.res]
            if tac.type == TAC.CALL:
                for i, arg in enumerate(tac.arg2):
                    if arg.startswith("E_"):
                        tac.arg2[i] = labels[arg]
            if tac.label != "":
                tac.label = labels[tac.label]
            if tac.type != TAC.LABEL:
                new_tacs[proc].append(tac)
    return dict(new_tacs)


def get_tac(text: str, test_run_folder: str) -> dict[str, list[Quadruple]]:
    lexer = GebalangLexer()
    parser = GebalangParser()
    parser.parse(lexer.tokenize(text))

    write_to_file(parser.tac, os.path.join(test_run_folder, "scratch.tac.raw"))
    tac = _clear_labels(parser.tac)
    return tac
