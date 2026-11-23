"""Тесты командной строки интерпретатора и формата дампа."""
import contextlib
import io
import os
import tempfile
import unittest

from encoding import encode_program
from formats import format_csv
from interpreter import EXIT_ERROR, EXIT_OK, EXIT_USAGE, main
from spec import Command


def run_main(*argv):
    """Запускает main; возвращает (код, stdout, stderr)."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = main(list(argv))
    return code, out.getvalue(), err.getvalue()


def write_program(folder, commands):
    """Записывает программу во временную папку и возвращает путь."""
    path = os.path.join(folder, "p.bin")
    with open(path, "wb") as handle:
        handle.write(encode_program(commands))
    return path


class FormatTests(unittest.TestCase):
    """Проверки формата CSV."""

    def test_csv(self):
        """Заголовок и строки 'адрес,значение'."""
        self.assertEqual(
            format_csv([(1, 10), (2, 20)]), "address,value\n1,10\n2,20\n")


class InterpreterCliTests(unittest.TestCase):
    """Проверки main."""

    def test_dump_file(self):
        """Дамп сохраняется в CSV-файл и выводится на экран."""
        with tempfile.TemporaryDirectory() as folder:
            binary = write_program(
                folder, [Command(44, 42), Command(174, 300)])
            dump = os.path.join(folder, "d.csv")
            code, out, _ = run_main(
                "--binary", binary, "--dump", dump, "--range", "299", "301")
            with open(dump, encoding="utf-8") as handle:
                content = handle.read()
        self.assertEqual(code, EXIT_OK)
        self.assertEqual(content, "address,value\n299,0\n300,42\n301,0\n")
        self.assertIn("Выполнено команд: 2", out)

    def test_hex_range(self):
        """Адреса диапазона можно писать в шестнадцатеричном виде."""
        with tempfile.TemporaryDirectory() as folder:
            binary = write_program(folder, [Command(44, 5)])
            dump = os.path.join(folder, "d.csv")
            code, out, _ = run_main(
                "--binary", binary, "--dump", dump, "--range", "0x0", "0x1")
        self.assertEqual(code, EXIT_OK)
        self.assertIn("0,44", out)

    def test_parameter_errors(self):
        """Ошибки параметров: код 2 и сообщение."""
        with tempfile.TemporaryDirectory() as folder:
            binary = write_program(folder, [Command(44, 1)])
            dump = os.path.join(folder, "d.csv")
            common = ["--binary", binary, "--dump", dump]
            bad = [
                [],
                common,
                ["--binary", "no.bin", "--dump", dump, "--range", "0", "1"],
                ["--binary", binary, "--dump", "no_dir/d.csv",
                 "--range", "0", "1"],
                common + ["--range", "5", "1"],
                common + ["--range", "a", "1"],
                common + ["--range", "0", "99999999"],
                common + ["--range", "1"],
            ]
            for argv in bad:
                with self.subTest(argv):
                    code, _, err = run_main(*argv)
                    self.assertEqual(code, EXIT_USAGE)
                    self.assertIn("Ошибка параметров", err)

    def test_runtime_error(self):
        """Ошибка выполнения: код 1."""
        with tempfile.TemporaryDirectory() as folder:
            binary = write_program(folder, [Command(1, 0)])
            dump = os.path.join(folder, "d.csv")
            code, _, err = run_main(
                "--binary", binary, "--dump", dump, "--range", "0", "1")
        self.assertEqual(code, EXIT_ERROR)
        self.assertIn("Ошибка", err)


if __name__ == "__main__":
    unittest.main()
