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
