from .models import Quadruple, TAC


def get_tac_repr(tac: Quadruple, label_pad: int):
    label = tac.label.ljust(label_pad)
    if tac.type == TAC.CALL:
        right_side = f"CALL {tac.arg1}({', '.join(tac.arg2)})"
    elif tac.type == TAC.IFGOTO:
        right_side = f"IF {tac.arg1} {tac.op} {tac.arg2} GOTO {tac.res}"
    elif tac.type == TAC.GOTO:
        right_side = f"GOTO {tac.res}"
    elif tac.type == TAC.ASSIGN:
        right_side = f"{tac.res} := {tac.arg1} {tac.op} {tac.arg2}"
    else:
        right_side = f"{tac.op} {tac.arg1} {tac.arg2}"
    return f"{label} | {right_side}"


def write_to_file(tacs: dict[str, list[Quadruple]], path: str):
    max_label = 0
    for proc in tacs:
        proc_tacs = tacs[proc]
        for tac in proc_tacs:
            max_label = max(max_label, len(tac.label))

    text = ""
    for proc in tacs:
        proc_tacs = tacs[proc]
        text += f"{'='*(max_label+2)} {proc} {'='*(max_label+2)}\n"
        for tac in proc_tacs:
            text += f"{get_tac_repr(tac, max_label)}\n"

    with open(path, 'w+') as file:
        file.write(text)
