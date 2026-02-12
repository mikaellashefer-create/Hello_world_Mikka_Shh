#Ввод буковок
operator_name = input("Имя оператора: ")
current_pressure_sensor_value = input("Текущее занчение датчика давления: ")

#Создание файла
with open("sensor_log.txt", "w", encoding="utf-8") as file:
    file.write(f"ОПЕРАТОР\tЗНАЧЕНИЕ\n")
    file.write(f"{operator_name}\t\t\t{current_pressure_sensor_value}")

#Мы молодцы
    print("Данные успешно сохранены в sensor_log.txt!!!!")