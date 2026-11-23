"""Тесты командной строки ассемблера."""
import contextlib
import io
import os
import tempfile
import unittest

from assembler import EXIT_ERROR, EXIT_OK, EXIT_USAGE, main, parse_args
from errors import ConfigError

EXAMPLES = os.path.join(os.path.dirname(__file__), "..", "examples")
SPEC_FILE = os.path.join(EXAMPLES, "spec_tests.asm")


def run_main(*argv):
    """Запускает main; возвращает (код, stdout, stderr)."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = main(list(argv))
    return code, out.getvalue(), err.getvalue()


class AssemblerCliTests(unittest.TestCase):
    """Проверки main."""

    def test_test_mode_prints_bytes(self):
        """Режим тестирования выводит байты, как в спецификации."""
        with tempfile.TemporaryDirectory() as folder:
            output = os.path.join(folder, "out.bin")
            code, out, _ = run_main(
                "--source", SPEC_FILE, "--output", output, "--test")
        self.assertEqual(code, EXIT_OK)
        self.assertEqual(out.splitlines()[:4], [
            "0x2C, 0x04, 0x01, 0x00, 0x00",
            "0xDF, 0x3E, 0x02, 0x00, 0x00",
            "0xAE, 0x98, 0x00, 0x00, 0x00",
            "0xA9, 0x71, 0x00, 0x00, 0x00"])

    def test_binary_file_and_size(self):
        """Двоичный файл записан, его размер выведен."""
        with tempfile.TemporaryDirectory() as folder:
            output = os.path.join(folder, "out.bin")
            code, out, _ = run_main(
                "--source", SPEC_FILE, "--output", output)
            with open(output, "rb") as handle:
                data = handle.read()
        self.assertEqual(code, EXIT_OK)
        self.assertEqual(len(data), 20)
        self.assertEqual(data[:5], bytes([0x2C, 0x04, 0x01, 0x00, 0x00]))
        self.assertIn("Размер двоичного файла: 20 байт", out)

    def test_parameter_errors(self):
        """Ошибки параметров: сообщение и код 2."""
        bad = [
            [],
            ["--source", SPEC_FILE],
            ["--output", "out.bin"],
            ["--source", "no_such.asm", "--output", "out.bin"],
            ["--source", SPEC_FILE, "--output", "no_dir/out.bin"],
            ["--source", SPEC_FILE, "--output", "out.bin", "--bogus"],
            ["--source"],
        ]
        for argv in bad:
            with self.subTest(argv):
                code, _, err = run_main(*argv)
                self.assertEqual(code, EXIT_USAGE)
                self.assertIn("Ошибка параметров", err)

    def test_syntax_error(self):
        """Ошибка в программе: код 1 и номер строки."""
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "bad.asm")
            with open(path, "w", encoding="utf-8") as handle:
                handle.write("acc = 1\nfoo\n")
            code, _, err = run_main(
                "--source", path, "--output", os.path.join(folder, "o.bin"))
        self.assertEqual(code, EXIT_ERROR)
        self.assertIn("строка 2", err)

    def test_unknown_option_message(self):
        """Сообщение о неизвестном параметре по-русски."""
        with self.assertRaises(ConfigError) as caught:
            parse_args(["--bogus"])
        self.assertIn("неизвестные параметры", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
