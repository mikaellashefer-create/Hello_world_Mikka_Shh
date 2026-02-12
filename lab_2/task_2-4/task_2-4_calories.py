# Ввод данных
protein = float(input("Масса белков в продукте:"))
fat = float(input("Масса жиров в продукте:"))
carbohydrates = float(input("Масса углеволов в продукте:"))

# Расчет общей калорийности
calories = (protein * 4) + (fat * 9) + (carbohydrates * 4)

# Вывод результата с помощью f-строки
print(f"Калорийность: {calories:.1f} ккал")