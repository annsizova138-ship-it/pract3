"""Язык ассемблера УВМ: разбор текста программы в список команд."""
import re

from errors import AsmError
from spec import OP_LOAD, OP_MAX, OP_READ, OP_WRITE, Command, operand_limit

COMMENT = "#"
AUTO_BASE = 0
FIRST_LINE = 1
FORMS = (
    (re.compile(r"acc\s*=\s*max\(\s*acc\s*,\s*mem\[(.+)\]\s*\)"), OP_MAX),
    (re.compile(r"acc\s*=\s*mem\[(.+)\]"), OP_READ),
    (re.compile(r"mem\[(.+)\]\s*=\s*acc"), OP_WRITE),
    (re.compile(r"acc\s*=\s*(.+)"), OP_LOAD),
)


def parse_number(text, number):
    """Переводит запись числа (10, 0x1F, 0b101) в целое число."""
    try:
        return int(text.strip(), AUTO_BASE)
    except ValueError as err:
        raise AsmError(
            f"строка {number}: некорректное число '{text.strip()}'") from err


def check_operand(opcode, operand, number):
    """Проверяет, что операнд помещается в поле B команды."""
    limit = operand_limit(opcode)
    if operand not in range(limit):
        raise AsmError(
            f"строка {number}: значение {operand} вне диапазона "
            f"0..{limit - 1}")


def parse_line(text, number):
    """Разбирает одну команду и возвращает Command."""
    for form, opcode in FORMS:
        match = form.fullmatch(text)
        if match:
            operand = parse_number(match.group(1), number)
            check_operand(opcode, operand, number)
            return Command(opcode, operand)
    raise AsmError(f"строка {number}: неизвестная команда: {text}")


def parse_program(text):
    """Разбирает текст программы в список команд."""
    commands = []
    for number, raw in enumerate(text.splitlines(), start=FIRST_LINE):
        line = raw.split(COMMENT, 1)[0].strip()
        if line:
            commands.append(parse_line(line, number))
    return commands
