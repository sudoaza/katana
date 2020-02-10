from katana.unit import PrintableDataUnit, NotApplicable
from katana.units.esoteric.brainfuck import evaluate_brainfuck

import re

from typing import Any

p_mappings = [
    "pikachu",
    "pikapi",
    "pichu",
    "pika",
    "pipi",
    "chu",
    "ka",
    "pi",
]

r_mappings = [b".", b",", b"<", b"[", b">", b"]", b"-", b"+"]

regex_finder = "({})".format("|".join([x for x in p_mappings]))


class Unit(PrintableDataUnit):

    # Fill in your groups
    GROUPS = ["esoteric", "pikalang"]

    # Default priority is 50
    PRIORITY = 40

    def __init__(self, *args, **kwargs):
        super(PrintableDataUnit, self).__init__(*args, **kwargs)

        # Grab the pikalang commands from the targets
        self.pika_commands = re.findall(bytes(regex_finder, "utf-8"), self.target.raw)

        if len(self.pika_commands) <= 5:
            raise NotApplicable("not enough pikalang")

    def evaluate(self, case: Any):

        # Convert the found pikalang commands to brainfuck
        new_brainfuck = []
        for p in self.pika_commands:
            new_brainfuck.append(r_mappings[p_mappings.index(p.decode("utf-8"))])

        # Try to run the brainfuck code
        try:
            output = evaluate_brainfuck(new_brainfuck, None)
        except (ValueError, TypeError):
            return  # if it fails, give up!

        if output:
            self.manager.register_data(self, output)
