"""Тесты интерпретатора: загрузка, память, операция max()."""
import unittest

from encoding import encode_program
from errors import VmError
from machine import Machine
from spec import Command


def run_program(*commands):
    """Выполняет программу из команд и возвращает машину."""
    machine = Machine(encode_program(list(commands)))
    machine.run()
    return machine


class MachineTests(unittest.TestCase):
    """Проверки Machine."""

    def test_load_constant(self):
        """A=44 кладёт константу в аккумулятор."""
        machine = run_program(Command(44, 260))
        self.assertEqual(machine.acc, 260)

    def test_write_then_read(self):
        """Запись в память и чтение обратно через аккумулятор."""
        machine = run_program(
            Command(44, 99), Command(174, 500),
            Command(44, 0), Command(223, 500))
        self.assertEqual(machine.memory.read(500), 99)
        self.assertEqual(machine.acc, 99)

    def test_step_count(self):
        """Счётчик выполненных команд."""
        machine = run_program(Command(44, 1), Command(174, 300))
        self.assertEqual(machine.steps, 2)

    def test_empty_program(self):
        """Пустая программа ничего не делает."""
        machine = Machine(b"")
        machine.run()
        self.assertEqual(machine.steps, 0)

    def test_program_size_not_multiple(self):
        """Размер программы не кратен 5 - ошибка."""
        with self.assertRaises(VmError):
            Machine(b"\x2c\x00\x00")

    def test_max_memory_larger(self):
        """max(): в памяти значение больше аккумулятора."""
        machine = run_program(
            Command(44, 30), Command(174, 400),
            Command(44, 10), Command(169, 400))
        self.assertEqual(machine.acc, 30)

    def test_max_accumulator_larger(self):
        """max(): аккумулятор больше значения в памяти."""
        machine = run_program(
            Command(44, 5), Command(174, 400),
            Command(44, 50), Command(169, 400))
        self.assertEqual(machine.acc, 50)

    def test_max_with_empty_cell(self):
        """max(): ячейка без записи равна нулю."""
        machine = run_program(Command(44, 8), Command(169, 777))
        self.assertEqual(machine.acc, 8)

    def test_max_large_values(self):
        """max(): работает с наибольшей 31-битной константой."""
        top = 2**31 - 1
        machine = run_program(
            Command(44, top), Command(174, 400),
            Command(44, 1), Command(169, 400))
        self.assertEqual(machine.acc, top)

    def test_unknown_command(self):
        """Неизвестный код команды - ошибка."""
        with self.assertRaises(VmError):
            run_program(Command(1, 0))

    def test_operand_out_of_range(self):
        """Поле B больше допустимого - ошибка."""
        with self.assertRaises(VmError):
            Machine(bytes([0xAE, 0xFF, 0xFF, 0xFF, 0x7F])).run()

    def test_program_lives_in_memory(self):
        """Команды лежат в той же памяти, что и данные."""
        machine = Machine(encode_program([Command(44, 260)]))
        self.assertEqual(machine.memory.dump(0, 4), [
            (0, 0x2C), (1, 0x04), (2, 0x01), (3, 0x00), (4, 0x00)])


if __name__ == "__main__":
    unittest.main()
