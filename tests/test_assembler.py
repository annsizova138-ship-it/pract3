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

    def test_test_mode_prints_fields(self):
        """Режим тестирования выводит поля и значения команд."""
        code, out, _ = run_main(
            "--source", SPEC_FILE, "--output", "out.bin", "--test")
        self.assertEqual(code, EXIT_OK)
        self.assertEqual(
            out.splitlines(),
            ["A=44, B=260", "A=223, B=574", "A=174, B=152", "A=169, B=113"])

    def test_normal_mode(self):
        """Без режима тестирования выводится число команд."""
        code, out, _ = run_main("--source", SPEC_FILE, "--output", "out.bin")
        self.assertEqual(code, EXIT_OK)
        self.assertIn("4", out)

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
