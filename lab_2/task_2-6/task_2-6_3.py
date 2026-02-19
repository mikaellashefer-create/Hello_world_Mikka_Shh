# Группа крови донора и пациента
donor = input("Введите группу крови донора (A, B, AB или O): ").upper()
recipient = input("Введите группу крови пациента (A, B, AB или O): ").upper()

valid_groups = ['A', 'B', 'AB', 'O']

if donor not in valid_groups or recipient not in valid_groups:
    print("Ошибка: введите корректную группу крови (A, B, AB или O)")
else:
    # Переливание
    if donor == recipient or donor == 'O':
        print(f"Кровь группы {donor} можно перелить пациенту с группой {recipient}")
    else:
        print(f"Кровь группы {donor} НЕЛЬЗЯ перелить пациенту с группой {recipient}")