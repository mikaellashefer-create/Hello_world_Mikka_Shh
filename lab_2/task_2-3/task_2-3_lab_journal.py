# Сбор данных
researcher_name = input()
date = input()
experiment_name = input()
conclusion = input()

# Создание файла
with open('journal.txt', 'w', encoding='utf-8') as file:

    # Верхняя граница рамки
    file.write("╔" + "═" * 50 + "╗\n")

    # Заголовок
    file.write("║" + " " * 50 + "║\n")
    file.write("║" + " ЭЛЕКТРОННЫЙ ЛАБОРАТОРНЫЙ ЖУРНАЛ ".center(50) + "║\n")
    file.write("║" + " " * 50 + "║\n")

    # Разделитель
    file.write("╠" + "═" * 50 + "╣\n")

    # Внутри рамки
    file.write("║" + f" ФИО исследователя: {researcher_name}".ljust(50) + "║\n")
    file.write("║" + f" Дата: {date}".ljust(50) + "║\n")
    file.write("║" + " " * 50 + "║\n")
    file.write("║" + f" Эксперимент: {experiment_name}".ljust(50) + "║\n")
    file.write("║" + " " * 50 + "║\n")
    file.write("║" + " Вывод:".ljust(50) + "║\n")
    file.write("║" + f" {conclusion}".ljust(50) + "║\n")

    # Нижняя граница рамки
    file.write("╚" + "═" * 50 + "╝\n")

#Кто молодец? Я молодец!!
print("Лабораторный журнал успешно создан!!!!!!")