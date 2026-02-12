# Ввод данных
total_capsules = int(input("Введите общее количество произведенных капсул (целое число): "))
pack_capacity = int(input("Введите количество капсул в одной упаковке: "))

# Расчет
full_packs = total_capsules // pack_capacity
remaining_capsules = total_capsules % pack_capacity

# Вывод
print("\n--- Отчет фасовочного цеха ---\n")
print(f"Полных упаковок:\t{full_packs}")
print(f"Остаток капсул:\t\t{remaining_capsules}")