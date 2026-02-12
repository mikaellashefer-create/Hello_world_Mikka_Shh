# Ввод последовательности
dna_sequence = input("Введите последовательность ДНК: ").strip()

dna_upper = dna_sequence.upper()

# Подсчет нуклеотидов
count_A = dna_upper.count('A')
count_T = dna_upper.count('T')
count_G = dna_upper.count('G')
count_C = dna_upper.count('C')

# Общая длина последовательности
total_length = len(dna_upper)

# Вывод результатов
print("\n=== Анализ последовательности ДНК ===\n")
print(f"Последовательность в верхнем регистре: {dna_upper}\n")
print("Подсчёт нуклеотидов:")
print(f"A: {count_A}")
print(f"T: {count_T}")
print(f"G: {count_G}")
print(f"C: {count_C}\n")
print(f"Общая длина: {total_length} нуклеотидов")
print("\nПроцентное содержание:")
print(f"A: {(count_A / total_length * 100):.1f}%")
print(f"T: {(count_T / total_length * 100):.1f}%")
print(f"G: {(count_G / total_length * 100):.1f}%")
print(f"C: {(count_C / total_length * 100):.1f}%")