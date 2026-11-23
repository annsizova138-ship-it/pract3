"""Тесты из спецификации УВМ: промежуточное представление."""
import os
import unittest

from files import read_text
from spec import Command
from syntax import parse_program

EXAMPLES = os.path.join(os.path.dirname(__file__), "..", "examples")
SPEC_COMMANDS = [
    Command(44, 260),
    Command(223, 574),
    Command(174, 152),
    Command(169, 113),
]


class SpecTests(unittest.TestCase):
    """Ассемблер выдаёт те же поля и значения, что в спецификации."""

    def test_spec_file(self):
        """Файл examples/spec_tests.asm даёт тесты из спецификации."""
        text = read_text(os.path.join(EXAMPLES, "spec_tests.asm"))
        self.assertEqual(parse_program(text), SPEC_COMMANDS)

    def test_each_command_alone(self):
        """Каждая команда спецификации по отдельности."""
        lines = ["acc = 260", "acc = mem[574]", "mem[152] = acc",
                 "acc = max(acc, mem[113])"]
        for line, expected in zip(lines, SPEC_COMMANDS):
            with self.subTest(line):
                self.assertEqual(parse_program(line), [expected])


if __name__ == "__main__":
    unittest.main()
