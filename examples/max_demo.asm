# Демонстрация max(): результаты сохраняются в память
# Исходные данные: mem[300]=7, mem[301]=19, mem[302]=3
acc = 7
mem[300] = acc
acc = 19
mem[301] = acc
acc = 3
mem[302] = acc
# Случай 1: max(7, 19) = 19 -> mem[310]
acc = mem[300]
acc = max(acc, mem[301])
mem[310] = acc
# Случай 2: max(19, 3) = 19 -> mem[311]
acc = mem[301]
acc = max(acc, mem[302])
mem[311] = acc
# Случай 3: аккумулятор больше значения в памяти: max(100, 19) = 100 -> mem[312]
acc = 100
acc = max(acc, mem[301])
mem[312] = acc
# Случай 4: максимум из трёх: max(max(7, 19), 3) = 19 -> mem[313]
acc = mem[300]
acc = max(acc, mem[301])
acc = max(acc, mem[302])
mem[313] = acc
