"""Тесты языка ассемблера: разбор текста в команды."""
import unittest

from errors import AsmError
from spec import Command
from syntax import parse_line, parse_program


class ParseLineTests(unittest.TestCase):
    """Проверки разбора одной команды."""

    def test_load_constant(self):
        """acc = число - загрузка константы."""
        self.assertEqual(parse_line("acc = 260", 1), Command(44, 260))

    def test_read(self):
        """acc = mem[адрес] - чтение из памяти."""
        self.assertEqual(parse_line("acc = mem[574]", 1), Command(223, 574))

    def test_write(self):
        """mem[адрес] = acc - запись в память."""
        self.assertEqual(parse_line("mem[152] = acc", 1), Command(174, 152))

    def test_max(self):
        """acc = max(acc, mem[адрес]) - бинарная операция."""
        line = "acc = max(acc, mem[113])"
        self.assertEqual(parse_line(line, 1), Command(169, 113))

    def test_spaces_and_numbers(self):
        """Пробелы свободные, числа - десятичные и шестнадцатеричные."""
        self.assertEqual(parse_line("acc=0x10", 1), Command(44, 16))
        self.assertEqual(
            parse_line("acc  =  max( acc ,mem[ 0b11 ] )", 1),
            Command(169, 3))
        self.assertEqual(parse_line("mem[0x1F]=acc", 1), Command(174, 31))

    def test_limits(self):
        """Наибольшие значения полей B принимаются."""
        self.assertEqual(
            parse_line("acc = 2147483647", 1), Command(44, 2**31 - 1))
        self.assertEqual(
            parse_line("mem[33554431] = acc", 1), Command(174, 2**25 - 1))

    def test_errors(self):
        """Ошибочные строки дают AsmError."""
        bad = ["acc", "mem[1] = 5", "acc = abc", "acc = -1",
               "acc = 2147483648", "acc = mem[33554432]",
               "mem[x] = acc", "acc = max(acc, mem[1]", "acc = 010",
               "mem[1] = mem[2]", "load 5"]
        for line in bad:
            with self.subTest(line):
                with self.assertRaises(AsmError):
                    parse_line(line, 1)


class ParseProgramTests(unittest.TestCase):
    """Проверки разбора целой программы."""

    def test_comments_and_blank_lines(self):
        """Комментарии и пустые строки пропускаются."""
        text = "# заголовок\n\nacc = 1  # одна\n   \nmem[2] = acc\n"
        self.assertEqual(
            parse_program(text), [Command(44, 1), Command(174, 2)])

    def test_empty_program(self):
        """Пустая программа - пустой список."""
        self.assertEqual(parse_program("# ничего\n"), [])

    def test_error_has_line_number(self):
        """В сообщении об ошибке указан номер строки."""
        with self.assertRaises(AsmError) as caught:
            parse_program("acc = 1\n\nfoo\n")
        self.assertIn("строка 3", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
