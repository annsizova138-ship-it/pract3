"""Текстовые представления для вывода на экран и в файлы."""
import csv
import io

CSV_HEADER = ("address", "value")


def format_fields(command):
    """Возвращает поля команды в виде 'A=44, B=260'."""
    return f"A={command.a}, B={command.b}"


def format_bytes(data):
    """Возвращает байты в виде '0x2C, 0x04, 0x01, 0x00, 0x00'."""
    return ", ".join(f"0x{byte:02X}" for byte in data)


def format_csv(rows):
    """Возвращает дамп памяти (пары адрес, значение) в формате CSV."""
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(CSV_HEADER)
    writer.writerows(rows)
    return buffer.getvalue()
