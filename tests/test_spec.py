"""Тесты из спецификации УВМ: промежуточное представление и байты."""
import os
import unittest

from encoding import encode_program
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

    def test_spec_file_bytes(self):
        """Файл examples/spec_tests.asm даёт байты из спецификации."""
        text = read_text(os.path.join(EXAMPLES, "spec_tests.asm"))
        expected = bytes([
            0x2C, 0x04, 0x01, 0x00, 0x00,
            0xDF, 0x3E, 0x02, 0x00, 0x00,
            0xAE, 0x98, 0x00, 0x00, 0x00,
            0xA9, 0x71, 0x00, 0x00, 0x00,
        ])
        self.assertEqual(encode_program(parse_program(text)), expected)


if __name__ == "__main__":
    unittest.main()
