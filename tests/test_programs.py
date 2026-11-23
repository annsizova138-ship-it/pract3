"""Тесты примеров программ: ассемблирование и выполнение."""
import os
import unittest

from encoding import encode_program
from files import read_text
from machine import Machine
from syntax import parse_program

EXAMPLES = os.path.join(os.path.dirname(__file__), "..", "examples")


def run_example(name):
    """Ассемблирует и выполняет пример; возвращает машину."""
    text = read_text(os.path.join(EXAMPLES, name))
    machine = Machine(encode_program(parse_program(text)))
    machine.run()
    return machine


def values(machine, first, count):
    """Возвращает count значений памяти, начиная с адреса first."""
    rows = machine.memory.dump(first, first + count - 1)
    return [value for _, value in rows]


class ProgramTests(unittest.TestCase):
    """Проверки примеров из папки examples."""

    def test_copy_array(self):
        """Массив скопирован с адреса 200 на адрес 210."""
        machine = run_example("copy_array.asm")
        self.assertEqual(values(machine, 200, 5), [11, 22, 33, 44, 55])
        self.assertEqual(values(machine, 210, 5), [11, 22, 33, 44, 55])

    def test_max_demo(self):
        """Результаты max() сохранены в память."""
        machine = run_example("max_demo.asm")
        self.assertEqual(values(machine, 300, 3), [7, 19, 3])
        self.assertEqual(values(machine, 310, 4), [19, 19, 100, 19])

    def test_vector_max_examples(self):
        """Вектор длины 6 после поэлементного max() с числом 14."""
        cases = {
            "vector_max_1.asm": [14, 14, 14, 14, 14, 14],
            "vector_max_2.asm": [20, 14, 14, 100, 14, 15],
            "vector_max_3.asm": [14, 14, 15, 2000000000, 14, 14],
        }
        for name, expected in cases.items():
            with self.subTest(name):
                machine = run_example(name)
                self.assertEqual(values(machine, 400, 6), expected)


if __name__ == "__main__":
    unittest.main()
