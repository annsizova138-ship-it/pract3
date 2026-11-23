# Пример 2: числа вокруг 14
# Вектор длины 6 по адресам 400..405 и число 14.
# Для каждого элемента: mem[i] = max(14, mem[i]); результат остаётся в векторе.
# Шаг 1: записать исходный вектор в память
acc = 20
mem[400] = acc
acc = 5
mem[401] = acc
acc = 14
mem[402] = acc
acc = 100
mem[403] = acc
acc = 0
mem[404] = acc
acc = 15
mem[405] = acc
# Шаг 2: поэлементно max() с числом 14
acc = 14
acc = max(acc, mem[400])
mem[400] = acc
acc = 14
acc = max(acc, mem[401])
mem[401] = acc
acc = 14
acc = max(acc, mem[402])
mem[402] = acc
acc = 14
acc = max(acc, mem[403])
mem[403] = acc
acc = 14
acc = max(acc, mem[404])
mem[404] = acc
acc = 14
acc = max(acc, mem[405])
mem[405] = acc
