# Копирование массива из 5 элементов: адрес 200 -> адрес 210
# Шаг 1: заполнить исходный массив
acc = 11
mem[200] = acc
acc = 22
mem[201] = acc
acc = 33
mem[202] = acc
acc = 44
mem[203] = acc
acc = 55
mem[204] = acc
# Шаг 2: скопировать элементы
acc = mem[200]
mem[210] = acc
acc = mem[201]
mem[211] = acc
acc = mem[202]
mem[212] = acc
acc = mem[203]
mem[213] = acc
acc = mem[204]
mem[214] = acc
