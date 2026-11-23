"""Тесты модели памяти УВМ."""
import unittest

from errors import VmError
from memory import MEMORY_SIZE, Memory


class MemoryTests(unittest.TestCase):
    """Проверки Memory."""

    def test_empty_cells_are_zero(self):
        """Ячейки без записи содержат ноль."""
        self.assertEqual(Memory().read(12345), 0)

    def test_write_and_read(self):
        """Записанное значение читается обратно."""
        memory = Memory()
        memory.write(100, 777)
        self.assertEqual(memory.read(100), 777)

    def test_address_limits(self):
        """Адреса за пределами памяти дают VmError."""
        memory = Memory()
        memory.write(MEMORY_SIZE - 1, 1)
        for address in (-1, MEMORY_SIZE):
            with self.subTest(address):
                with self.assertRaises(VmError):
                    memory.read(address)
                with self.assertRaises(VmError):
                    memory.write(address, 1)

    def test_load_program(self):
        """Программа размещается с адреса 0 в той же памяти."""
        memory = Memory()
        memory.load(bytes([1, 2, 3]))
        self.assertEqual(memory.dump(0, 3), [(0, 1), (1, 2), (2, 3), (3, 0)])

    def test_dump_is_inclusive(self):
        """Дамп включает оба конца диапазона."""
        memory = Memory()
        memory.write(5, 50)
        memory.write(7, 70)
        self.assertEqual(memory.dump(5, 7), [(5, 50), (6, 0), (7, 70)])


if __name__ == "__main__":
    unittest.main()
