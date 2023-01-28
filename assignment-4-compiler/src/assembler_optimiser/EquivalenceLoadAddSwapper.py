from ..common.commands import LOAD, LOADI, ADDI, ADD
from ..common.cfg_models import BasicBlock
from ..control_flow_graph.cfg import ICFG


class EquivalenceLoadAddSwapper:
    """Swapping """
    def __init__(self, icfg: ICFG):
        self.icfg = icfg

    def swap(self):
        for proc_name, cfg in self.icfg.cfgs.items():
            if proc_name.startswith("!"):
                continue
            #print(proc_name)
            for bb in cfg.nodes.values():
                self._swap_in_bb(bb)

    def _swap_in_bb(self, bb: BasicBlock):
        possible_load_swaps = set()
        prev_command = bb.commands[0]
        for i, command in enumerate(bb.commands[1:], start=1):
            if prev_command.is_load and command.is_add:
                possible_load_swaps.add(i-1)
            prev_command = command
        #print(possible_load_swaps, bb.index)

        new_commands = []
        i = 0
        while i < len(bb.commands):
            if i in possible_load_swaps:
                load_command = bb.commands[i]
                add_command = bb.commands[i+1]
                if add_command.is_i:
                    new_load_command = LOADI(add_command.arg, add_command.label)
                else:
                    new_load_command = LOAD(add_command.arg, add_command.label)

                if load_command.is_i:
                    new_add_command = ADDI(load_command.arg, load_command.label)
                else:
                    new_add_command = ADD(load_command.arg, load_command.label)
                new_commands.extend([new_load_command, new_add_command])

                i += 2
            else:
                new_commands.append(bb.commands[i])
                i += 1
        bb.set_commands(new_commands)



