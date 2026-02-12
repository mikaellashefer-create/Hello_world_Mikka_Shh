# Объем раствора
volume = float(input("Введите нужный объем физиологического раствора (мл): "))

# Расчет массы соли
salt_mass = volume * 0.009

# Запись рецепта
with open("recipe.txt", "w", encoding="utf-8") as file:
    file.write("ОТЧЕТ ПО ПРИГОТОВЛЕНИЮ:\n")
    file.write("-" * 23 + "\n")
    file.write(f"Общий объем:{volume:.2f} мл\n")
    file.write(f"Масса соли:\t{salt_mass:.2f} г\n")
    file.write(f"Объем воды:\t{volume:.2f} мл\n")

#Ecgtiyj
print("Рецепт успешно сохранен в файл recipe.txt!")