import os
import sys

from src.optimiser.optimiser import Optimiser
from src.gebalang.runner import get_tac
from src.tac_models.utils import write_to_file
from src.tac_validator.runner import validate
from src.tac_validator.exceptions import TACException
from src.translator.translator import Translator
from src.translator.commands import write_commands_to_file


def main():
    test_run_folder = "output"
    if not os.path.exists(test_run_folder):
        os.mkdir(test_run_folder)

    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    filename = os.path.basename(filepath).split(".")[0]

    with open(filepath, encoding='utf-8') as file:
        data = file.read()
    tac = get_tac(data, test_run_folder)
    write_to_file(tac, os.path.join(test_run_folder, f"{filename}.tac"))
    try:
        validate(tac)
    except TACException as e:
        print("ERROR:", e.__repr__())
        sys.exit(1)

    optimiser = Optimiser(tac, test_run_folder, filename)
    tac = optimiser.get_tac()
    write_to_file(tac, os.path.join(test_run_folder, f"optimised.tac"))

    translator = Translator(tac)
    translator.translate_all()
    write_commands_to_file(os.path.join(test_run_folder, f"compiled.tac"), translator.fully_translated_tac)


if __name__ == "__main__":
    main()
