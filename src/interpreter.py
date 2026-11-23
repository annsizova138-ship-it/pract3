"""Интерпретатор УВМ: командная строка."""
import sys
from dataclasses import dataclass

from cli import make_parser, require_file, require_output
from errors import ConfigError, UvmError
from files import read_bytes, write_text
from formats import format_csv
from machine import Machine
from memory import MEMORY_SIZE

EXIT_OK = 0
EXIT_ERROR = 1
EXIT_USAGE = 2
AUTO_BASE = 0


@dataclass
class Config:
    """Параметры интерпретатора."""

    binary: str
    dump: str
    first: int
    last: int


def parse_address(text, option):
    """Переводит адрес (10, 0x1F) в число и проверяет границы памяти."""
    try:
        address = int(text, AUTO_BASE)
    except ValueError as err:
        raise ConfigError(
            f"{option}: нужен адрес (целое число), получено '{text}'"
        ) from err
    if address not in range(MEMORY_SIZE):
        raise ConfigError(
            f"{option}: адрес {address} вне памяти (0..{MEMORY_SIZE - 1})")
    return address


def parse_range(values):
    """Разбирает пару адресов диапазона дампа."""
    if not values:
        raise ConfigError("не задан параметр --range")
    first = parse_address(values[0], "--range")
    last = parse_address(values[1], "--range")
    if first > last:
        raise ConfigError("--range: начало больше конца диапазона")
    return first, last


def parse_args(argv=None):
    """Разбирает и проверяет параметры командной строки."""
    parser = make_parser(
        "interpreter", "Интерпретатор учебной виртуальной машины")
    parser.add_argument(
        "--binary", metavar="ФАЙЛ", help="двоичный файл с программой")
    parser.add_argument(
        "--dump", metavar="ФАЙЛ", help="файл для дампа памяти (CSV)")
    parser.add_argument(
        "--range", nargs=2, metavar=("НАЧАЛО", "КОНЕЦ"),
        help="диапазон адресов дампа (включительно)")
    args = parser.parse_args(argv)
    first, last = parse_range(args.range)
    return Config(
        binary=require_file(args.binary, "--binary"),
        dump=require_output(args.dump, "--dump"),
        first=first, last=last)


def run(config):
    """Выполняет программу и сохраняет дамп памяти в CSV."""
    machine = Machine(read_bytes(config.binary))
    machine.run()
    text = format_csv(machine.memory.dump(config.first, config.last))
    write_text(config.dump, text)
    print(f"Выполнено команд: {machine.steps}")
    print(f"Дамп памяти {config.first}..{config.last} "
          f"сохранён в {config.dump}")
    print(text, end="")


def main(argv=None):
    """Запускает интерпретатор; возвращает код выхода."""
    try:
        run(parse_args(argv))
    except ConfigError as err:
        print(f"Ошибка параметров: {err}", file=sys.stderr)
        print("Подсказка: python src/interpreter.py --help", file=sys.stderr)
        return EXIT_USAGE
    except UvmError as err:
        print(f"Ошибка: {err}", file=sys.stderr)
        return EXIT_ERROR
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
