"""Спецификация учебной виртуальной машины (вариант 20)."""
from typing import NamedTuple

OP_LOAD = 44
OP_READ = 223
OP_WRITE = 174
OP_MAX = 169

COMMAND_SIZE = 5
OPCODE_BITS = 8
CONSTANT_BITS = 31
ADDRESS_BITS = 25

OPERAND_WIDTHS = {
    OP_LOAD: CONSTANT_BITS,
    OP_READ: ADDRESS_BITS,
    OP_WRITE: ADDRESS_BITS,
    OP_MAX: ADDRESS_BITS,
}


class Command(NamedTuple):
    """Команда в промежуточном представлении: поля A и B."""

    a: int
    b: int


def operand_limit(opcode):
    """Возвращает число, на единицу большее максимума поля B команды."""
    return 1 << OPERAND_WIDTHS[opcode]
