#Письмена
name_of_the_nutrient_medium = input("Название питательной среды: ")
agar_concentration = input("Концентрация агара: ")
sterilization_temperature = input("Температура стерилизации: ")

#Создание файла
with open("recipe.txt", 'w', encoding="utf-8") as file:
    file.write(f"{name_of_the_nutrient_medium}\n")
    file.write(f"  - Концентрация агара: {agar_concentration}%\n")
    file.write(f"  - Температура стерилизации: {sterilization_temperature}\n")

    # Все супер
    print("Файл "recipe.txt" успешно сформирован!")