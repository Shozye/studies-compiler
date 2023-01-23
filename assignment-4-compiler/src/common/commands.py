class Command:
    directive: str
    arg: str
    label: str

    def __init__(self, label: str, directive: str, arg: str = ""):
        self.directive = directive
        self.arg = arg
        self.label = label

    def __repr__(self):
        return f"{self.directive} {self.arg}" if self.arg else f"{self.directive}"


def write_commands_to_file(path: str, commands: list[Command]):
    text = ""
    for command in commands:
        text += f"{command}\n"
    with open(path, 'w+', encoding='utf-8') as file:
        file.write(text)


""" ======== INPUT / OUTPUT ======== """


class GET(Command):
    def __init__(self, i: str, label: str = ""):
        super().__init__(label, "GET", i)


class PUT(Command):
    def __init__(self, i: str, label: str = ""):
        super().__init__(label, "PUT", i)


""" ======== MEMORY ======== """


class LOAD(Command):
    def __init__(self, i: str, label: str = ""):
        super().__init__(label, "LOAD", i)


class STORE(Command):
    def __init__(self, i: str, label: str = ""):
        super().__init__(label, "STORE", i)


class LOADI(Command):
    def __init__(self, i: str, label: str = ""):
        super().__init__(label, "LOADI", i)


class STOREI(Command):
    def __init__(self, i: str, label: str = ""):
        super().__init__(label, "STOREI", i)


""" ======== ARITHMETIC ======== """


class ADD(Command):
    def __init__(self, i: str, label: str = ""):
        super().__init__(label, "ADD", i)


class SUB(Command):
    def __init__(self, i: str, label: str = ""):
        super().__init__(label, "SUB", i)


class ADDI(Command):
    def __init__(self, i: str, label: str = ""):
        super().__init__(label, "ADDI", i)


class SUBI(Command):
    def __init__(self, i: str, label: str = ""):
        super().__init__(label, "SUBI", i)


class SET(Command):
    def __init__(self, x: str, label: str = ""):
        super().__init__(label, "SET", x)


class HALF(Command):
    def __init__(self, label: str = ""):
        super().__init__(label, "HALF")


""" ======== CONDITIONAL ======== """


class JUMP(Command):
    def __init__(self, i: str, label: str = ""):
        super().__init__(label, "JUMP", i)


class JPOS(Command):
    def __init__(self, i: str, label: str = ""):
        super().__init__(label, "JPOS", i)


class JZERO(Command):
    def __init__(self, i: str, label: str = ""):
        super().__init__(label, "JZERO", i)


class JUMPI(Command):
    def __init__(self, i: str, label: str = ""):
        super().__init__(label, "JUMPI", i)


""" ======== OUTPUT ======== """


class HALT(Command):
    def __init__(self, label: str = ""):
        super().__init__(label, "HALT")
