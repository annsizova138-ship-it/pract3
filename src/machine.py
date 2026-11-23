"""Виртуальная машина: основной цикл интерпретатора."""
from encoding import decode
from errors import VmError
from memory import Memory
from spec import (COMMAND_SIZE, OP_LOAD, OP_MAX, OP_READ, OP_WRITE,
                  operand_limit)


class Machine:
    """УВМ: общая память, регистр-аккумулятор и счётчик команд."""

    def __init__(self, program):
        """Загружает программу (байты) в память с адреса 0."""
        if len(program) % COMMAND_SIZE:
            raise VmError(
                f"размер программы {len(program)} не кратен "
                f"{COMMAND_SIZE} байтам")
        self.memory = Memory()
        self.memory.load(program)
        self.size = len(program)
        self.acc = 0
        self.pc = 0
        self.steps = 0
        self.handlers = {
            OP_LOAD: self.op_load,
            OP_READ: self.op_read,
            OP_WRITE: self.op_write,
            OP_MAX: self.op_max,
        }

    def fetch(self):
        """Читает из памяти 5 байт очередной команды."""
        cells = [self.memory.read(self.pc + offset)
                 for offset in range(COMMAND_SIZE)]
        try:
            return bytes(cells)
        except ValueError as err:
            raise VmError(
                f"в области команд по адресу {self.pc} записано "
                "значение, которое не является байтом") from err

    def op_load(self, operand):
        """Загрузка константы: acc = B."""
        self.acc = operand

    def op_read(self, operand):
        """Чтение значения из памяти: acc = mem[B]."""
        self.acc = self.memory.read(operand)

    def op_write(self, operand):
        """Запись значения в память: mem[B] = acc."""
        self.memory.write(operand, self.acc)

    def op_max(self, operand):
        """Бинарная операция: acc = max(acc, mem[B])."""
        self.acc = max(self.acc, self.memory.read(operand))

    def execute(self, command):
        """Выполняет одну команду в промежуточном представлении."""
        handler = self.handlers.get(command.a)
        if handler is None:
            raise VmError(
                f"неизвестная или не поддерживаемая команда A={command.a} "
                f"по адресу {self.pc}")
        if command.b not in range(operand_limit(command.a)):
            raise VmError(
                f"поле B={command.b} вне диапазона для A={command.a} "
                f"по адресу {self.pc}")
        handler(command.b)

    def step(self):
        """Читает, декодирует и выполняет одну команду."""
        self.execute(decode(self.fetch()))
        self.pc += COMMAND_SIZE
        self.steps += 1

    def run(self):
        """Выполняет программу до конца области команд."""
        while self.pc < self.size:
            self.step()
