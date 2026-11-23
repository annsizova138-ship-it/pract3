"""Машинный код УВМ: перевод команды в 5 байт и обратно."""
from spec import BYTE_MASK, COMMAND_SIZE, OPCODE_BITS, Command

BYTE_ORDER = "little"


def encode(command):
    """Переводит команду в 5 байт (поле A - младший байт)."""
    value = command.a | (command.b << OPCODE_BITS)
    return value.to_bytes(COMMAND_SIZE, BYTE_ORDER)


def decode(data):
    """Переводит 5 байт в команду (поля A и B)."""
    value = int.from_bytes(data, BYTE_ORDER)
    return Command(value & BYTE_MASK, value >> OPCODE_BITS)


def encode_program(commands):
    """Переводит список команд в машинный код программы."""
    return b"".join(encode(command) for command in commands)
