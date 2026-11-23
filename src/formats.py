"""Текстовые представления команд для вывода на экран."""


def format_fields(command):
    """Возвращает поля команды в виде 'A=44, B=260'."""
    return f"A={command.a}, B={command.b}"
