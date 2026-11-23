"""Чтение и запись файлов с понятными сообщениями об ошибках."""
from errors import FileError

TEXT_ENCODING = "utf-8-sig"


def read_text(path):
    """Читает текстовый файл целиком."""
    try:
        with open(path, encoding=TEXT_ENCODING) as handle:
            return handle.read()
    except (OSError, UnicodeDecodeError) as err:
        raise FileError(f"не удалось прочитать {path}: {err}") from err


def write_bytes(path, data):
    """Записывает двоичный файл."""
    try:
        with open(path, "wb") as handle:
            handle.write(data)
    except OSError as err:
        raise FileError(f"не удалось записать {path}: {err}") from err


def read_bytes(path):
    """Читает двоичный файл целиком."""
    try:
        with open(path, "rb") as handle:
            return handle.read()
    except OSError as err:
        raise FileError(f"не удалось прочитать {path}: {err}") from err


def write_text(path, text):
    """Записывает текстовый файл в кодировке UTF-8."""
    try:
        with open(path, "w", encoding="utf-8", newline="") as handle:
            handle.write(text)
    except OSError as err:
        raise FileError(f"не удалось записать {path}: {err}") from err
