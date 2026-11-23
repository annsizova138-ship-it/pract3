"""Модель памяти УВМ: одна память для команд и данных."""
from errors import VmError
from spec import ADDRESS_BITS

MEMORY_SIZE = 1 << ADDRESS_BITS


class Memory:
    """Память: адрес -> значение, ячейки без записи содержат ноль."""

    def __init__(self):
        """Создаёт пустую память."""
        self.cells = {}

    def check(self, address):
        """Проверяет, что адрес лежит в пределах памяти."""
        if address not in range(MEMORY_SIZE):
            raise VmError(
                f"адрес {address} вне памяти (0..{MEMORY_SIZE - 1})")

    def read(self, address):
        """Возвращает значение ячейки."""
        self.check(address)
        return self.cells.get(address, 0)

    def write(self, address, value):
        """Записывает значение в ячейку."""
        self.check(address)
        self.cells[address] = value

    def load(self, data, start=0):
        """Размещает байты программы в памяти, начиная с адреса start."""
        for offset, byte in enumerate(data):
            self.write(start + offset, byte)

    def dump(self, first, last):
        """Возвращает пары (адрес, значение) от first до last включительно."""
        return [(address, self.read(address))
                for address in range(first, last + 1)]
