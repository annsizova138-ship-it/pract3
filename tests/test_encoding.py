"""Тесты машинного кода: тестовые последовательности спецификации."""
import unittest

from encoding import decode, encode, encode_program
from formats import format_bytes
from spec import Command

SPEC_BYTES = [
    (Command(44, 260), [0x2C, 0x04, 0x01, 0x00, 0x00]),
    (Command(223, 574), [0xDF, 0x3E, 0x02, 0x00, 0x00]),
    (Command(174, 152), [0xAE, 0x98, 0x00, 0x00, 0x00]),
    (Command(169, 113), [0xA9, 0x71, 0x00, 0x00, 0x00]),
]


class EncodingTests(unittest.TestCase):
    """Проверки encode и decode."""

    def test_spec_bytes(self):
        """Байты команд совпадают со спецификацией."""
        for command, expected in SPEC_BYTES:
            with self.subTest(command):
                self.assertEqual(list(encode(command)), expected)

    def test_decode_inverse(self):
        """decode возвращает исходную команду."""
        for command, expected in SPEC_BYTES:
            with self.subTest(command):
                self.assertEqual(decode(bytes(expected)), command)

    def test_largest_constant(self):
        """Наибольшая константа занимает биты 8-38."""
        self.assertEqual(
            list(encode(Command(44, 2**31 - 1))),
            [0x2C, 0xFF, 0xFF, 0xFF, 0x7F])

    def test_largest_address(self):
        """Наибольший адрес занимает биты 8-32."""
        self.assertEqual(
            list(encode(Command(174, 2**25 - 1))),
            [0xAE, 0xFF, 0xFF, 0xFF, 0x01])

    def test_program_size(self):
        """Каждая команда занимает 5 байт."""
        commands = [command for command, _ in SPEC_BYTES]
        self.assertEqual(len(encode_program(commands)), 20)

    def test_format_bytes(self):
        """Байты выводятся как в спецификации."""
        self.assertEqual(
            format_bytes(bytes([0x2C, 0x04, 0x01, 0x00, 0x00])),
            "0x2C, 0x04, 0x01, 0x00, 0x00")


if __name__ == "__main__":
    unittest.main()
