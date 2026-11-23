"""Ассемблер УВМ: командная строка."""
import sys
from dataclasses import dataclass

from cli import make_parser, require_file, require_output
from errors import ConfigError, UvmError
from files import read_text
from formats import format_fields
from syntax import parse_program

EXIT_OK = 0
EXIT_ERROR = 1
EXIT_USAGE = 2


@dataclass
class Config:
    """Параметры ассемблера."""

    source: str
    output: str
    test: bool


def parse_args(argv=None):
    """Разбирает и проверяет параметры командной строки."""
    parser = make_parser(
        "assembler", "Ассемблер учебной виртуальной машины (вариант 20)")
    parser.add_argument(
        "--source", metavar="ФАЙЛ", help="исходный файл с программой")
    parser.add_argument(
        "--output", metavar="ФАЙЛ", help="двоичный файл-результат")
    parser.add_argument(
        "--test", action="store_true", help="режим тестирования")
    args = parser.parse_args(argv)
    return Config(
        source=require_file(args.source, "--source"),
        output=require_output(args.output, "--output"),
        test=args.test)


def run(config):
    """Работа этапа 1: перевод программы в промежуточное представление."""
    commands = parse_program(read_text(config.source))
    if config.test:
        for command in commands:
            print(format_fields(command))
    else:
        print(f"Оттранслировано команд: {len(commands)}")


def main(argv=None):
    """Запускает ассемблер; возвращает код выхода."""
    try:
        run(parse_args(argv))
    except ConfigError as err:
        print(f"Ошибка параметров: {err}", file=sys.stderr)
        print("Подсказка: python src/assembler.py --help", file=sys.stderr)
        return EXIT_USAGE
    except UvmError as err:
        print(f"Ошибка: {err}", file=sys.stderr)
        return EXIT_ERROR
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
