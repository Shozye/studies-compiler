class Labels:
    def __init__(self):
        vars = ["if", "else", "while", "repeat", "until",
                "return", "endif", "endwhile"]
        self.counts = {
            var: 0 for var in vars
        }

    def _get(self, name: str):
        self.counts[name] += 1
        return f"E_{name.upper()}_{self.counts[name] - 1}"

    def get_if(self):
        return self._get("if")

    def get_else(self):
        return self._get("else")

    def get_while(self):
        return self._get("while")

    def get_repeat(self):
        return self._get("repeat")

    def get_until(self):
        return self._get("until")

    def get_return(self):
        return self._get("return")

    def get_endif(self):
        return self._get("endif")

    def get_endwhile(self):
        return self._get("endwhile")

