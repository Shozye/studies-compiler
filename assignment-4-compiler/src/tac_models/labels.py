from collections import defaultdict


class Labels:
    """Class used to provide user with unique labels for Three Address Code"""
    def __init__(self):
        self.counts = defaultdict(int)

    def _get(self, name: str):
        self.counts[name] += 1
        return f"E_{name.upper()}_{self.counts[name] - 1}"

    def get_ifclosed(self):
        return self._get("ifclosed")

    def get_return(self):
        return self._get("return")

    def get_aftergoto(self):
        return self._get("aftergoto")

    def get_cond(self):
        return self._get("cond")

    def get_gotocond(self):
        return self._get("gotocond")

