"""Общая основа разбора параметров командной строки."""
import argparse
import os
import re

from errors import ConfigError

HELP_TITLES = {
    "usage:": "использование:",
    "optional arguments:": "параметры:",
    "options:": "параметры:",
}


def translate_error(message):
    """Переводит типичные сообщения argparse на русский язык."""
    prefix = "unrecognized arguments:"
    if message.startswith(prefix):
        return "неизвестные параметры:" + message[len(prefix):]
    match = re.fullmatch(r"argument (\S+): expected one argument", message)
    if match:
        return f"для параметра {match.group(1)} нужно указать значение"
    match = re.fullmatch(r"argument (\S+): expected 2 arguments", message)
    if match:
        return f"для параметра {match.group(1)} нужно указать два значения"
    return message


class Parser(argparse.ArgumentParser):
    """Парсер, который сообщает об ошибках исключением ConfigError."""

    def error(self, message):
        """Бросает ConfigError вместо завершения программы."""
        raise ConfigError(translate_error(message))

    def format_help(self):
        """Возвращает справку с русскими заголовками разделов."""
        text = super().format_help()
        for english, russian in HELP_TITLES.items():
            text = text.replace(english, russian)
        return text


def make_parser(prog, description):
    """Создаёт парсер с русской справкой."""
    parser = Parser(
        prog=prog, description=description, allow_abbrev=False,
        add_help=False)
    parser.add_argument(
        "-h", "--help", action="help", help="показать эту справку и выйти")
    return parser


def require_value(value, option):
    """Проверяет, что обязательный параметр задан."""
    if not value:
        raise ConfigError(f"не задан параметр {option}")
    return value


def require_file(path, option):
    """Проверяет, что параметр задан и указывает на существующий файл."""
    require_value(path, option)
    if not os.path.isfile(path):
        raise ConfigError(f"{option}: файл не найден: {path}")
    return path


def require_output(path, option):
    """Проверяет, что параметр задан и папка для файла существует."""
    require_value(path, option)
    folder = os.path.dirname(path) or "."
    if not os.path.isdir(folder):
        raise ConfigError(f"{option}: папка не найдена: {folder}")
    return path
