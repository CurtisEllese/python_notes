# Реализовать консольное приложение заметки, с 
# 1. сохранением, 
# 2. чтением, 
# 3. добавлением, 
# 4. редактированием и 
# 5. удалением 
# заметок. Заметка должна содержать 
# 1. идентификатор, 
# 2. заголовок, 
# 3. тело заметки и 
# 4. дату/время создания или последнего изменения заметки. 
# Сохранение заметок необходимо сделать в формате json или csv формат (разделение полей рекомендуется делать через точку с запятой).
# При чтении списка заметок реализовать фильтрацию по дате.

import csv
from datetime import datetime
import pandas as pd
import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)


FILE = "notes.csv"
ID = 0

# Метод для принудительного выхода из порграммы
def quit_program():
    user_input = input("Выйти в главное меню: впишите Q (капсом), остаться в этом режиме нажмите Enter: ")
    return True if user_input == "Q" else False

# Метод для поиска заметки по символам
def find_note():
    if quit_program(): return # Метод для принудительного выхода из порграммы

    user_input = input("Введите слово/выражение, по которому надо вывести заметку: ")
    notes = list() # Создание списка для включения вхождений по ключевому слову

    with open(FILE, 'r', encoding='utf-8') as file:
        file_reader = csv.DictReader(file, delimiter = ";")

        for row in file_reader: # Проходимся по файлу: строка -> словарь
            for value in row.values(): # Проходимся по значениям в словаре
                value_casefold = value.casefold()
                if user_input.casefold() in value_casefold and row not in notes: # Если вхождение совпадает со значением и не находится в списке, то:
                    notes.append(row) # добавляем строку в список

        if len(notes): # Если список не пустой, то выводим все значения
            for dict in notes:
                print("---------------------------------------------------------")
                print(f'ID заметки - {dict["ID"]}')
                print(f'Заголовок заметки - {dict["Заголовок"]}')
                print(f'Текст заметки - {dict["Текст заметки"]}')
                print(f'Дата/время создания или последнего изменения заметки - {dict["Дата/время создания или последнего изменения заметки"]}')
                print("---------------------------------------------------------")
        else: print("Нет заметки с таким ключевым словом") # Если список пустой, выводим сообщение об этом

# Метод по изменению заметки
def edit_note():
    if quit_program(): return # Метод для принудительного выхода из порграммы

    global ID # Использование глобальной переменной

    notes_copy = copy_file() # Копирование файла: csv_file -> list of dict
    id_set = set() # Создание множества для занесения всех ID файла

    print("---------------------------------------------------------")
    edit_id = int(input("Введите ID заметки, которую нужно изменить: "))

    for row in notes_copy:
        id_set.add(row['ID']) # Добавление всех ID во множество
    
    if str(edit_id) not in id_set: # Если нет введенного ID во множестве, то
        print("Нет заметки с таким ID") # вывести сообщение об этом
    else:
        for row in notes_copy: # Проходимся по скопированному файлу
            if row['ID'] == str(edit_id): # Если ID совпадает, то
                current_datetime = datetime.now().replace(microsecond=0) # меняем дату и время
                # Меняем все данные
                row['Заголовок'] = input("Введите заголовок: ")
                row['Текст заметки'] = input("Введите текст заметки: ")
                row['Дата/время создания или последнего изменения заметки'] = current_datetime
        print("---------------------------------------------------------")
        
        # Открываем файл для записи
        with open(FILE, 'w', encoding='utf-8') as file:
            names = ["ID", "Заголовок", "Текст заметки", "Дата/время создания или последнего изменения заметки"]
            file_writer = csv.DictWriter(file, delimiter = ";", lineterminator="\r", fieldnames=names)

            # Если файл пустой, записываем заголовки
            if file.tell() == 0:
                file_writer.writeheader()
            # Проходимся по скопированному файлу и переносим данные
            for dict in notes_copy:
                file_writer.writerow({"ID": dict['ID'], "Заголовок": dict['Заголовок'], 
                        "Текст заметки": dict['Текст заметки'], "Дата/время создания или последнего изменения заметки": 
                        dict['Дата/время создания или последнего изменения заметки']})

# Метод получения последней строки
def get_last_line():
    try:
        with open(FILE, 'r', encoding='utf-8') as file:
            last_line = None
            for line in file:  # Читаем файл построчно
                last_line = line.strip()  # Удаляем лишние символы (включая символы новой строки)

            return last_line

    except FileNotFoundError:
        print("Файл не найден.")
    except IOError:
        print("Ошибка при чтении файла.")

# Метод копирования файла
def copy_file():
    res_list = list() # Создаем список для занесения результата

    with open(FILE, encoding='utf-8') as r_file:
        file_reader = csv.DictReader(r_file, delimiter = ";")

        for row in file_reader:
            res_list.append(row) # Копируем каждую строчку в список

    return res_list

# Метод удаления заметки
def delete_note():
    if quit_program(): return # Метод для принудительного выхода из порграммы

    global ID # Использование глобальной переменной

    id_set = set() # Создаем множество для всех ID
    notes_copy = copy_file() # Копируем файл

    print("---------------------------------------------------------")
    delete_id = int(input("Введите ID заметки, которую нужно удалить: "))
    # Добавление всех ID во множество
    for row in notes_copy:
        id_set.add(row['ID'])

    if str(delete_id) not in id_set: # Если нет введенного ID во множестве, то
        print("Нет заметки с таким ID")  # вывести сообщение об этом
    else:
        for row in notes_copy:  # Проходимся по скопированному файлу
            if row['ID'] == str(delete_id): # Если ID совпадает, то
                row.clear() # Очищаем все данные о заметке

        notes_copy = [i for i in notes_copy if i] # Добавляем все не пустые словари в список

        # Переносим все значения в файл
        with open(FILE, 'w', encoding='utf-8') as copy_f:
            names = ["ID", "Заголовок", "Текст заметки", "Дата/время создания или последнего изменения заметки"]
            file_writer = csv.DictWriter(copy_f, delimiter = ";", lineterminator="\r", fieldnames=names)

            if copy_f.tell() == 0:
                file_writer.writeheader()
            for dict in notes_copy:
                file_writer.writerow({"ID": dict['ID'], "Заголовок": dict['Заголовок'], 
                        "Текст заметки": dict['Текст заметки'], "Дата/время создания или последнего изменения заметки": 
                        dict['Дата/время создания или последнего изменения заметки']})

# Метод для сортировки заметок по дате
def filter_notes_by_date():
    # Загружаем CSV файл в DataFrame
    df = pd.read_csv(FILE, delimiter=';')

    # Преобразуем столбец 'Дата/время создания или последнего изменения заметки' в формат даты/времени
    df['Дата/время создания или последнего изменения заметки'] = pd.to_datetime(df['Дата/время создания или последнего изменения заметки'])

    # Сортируем DataFrame по столбцу с датами от меньшей к большей
    df.sort_values(by='Дата/время создания или последнего изменения заметки', inplace=True)

    # Сохраняем отфильтрованные данные в новый CSV файл
    df.to_csv(FILE, index=False, sep=';')

# Метод для вывода всех данных с файла
def read_file():
    filter_notes_by_date() # Сначала сортируем по дате

    with open(FILE, mode='r', encoding='utf-8') as r_file:
        reader = csv.DictReader(r_file, delimiter=';',  lineterminator="\r")

        for row in reader:
            print("---------------------------------------------------------")
            print(f'ID заметки - {row["ID"]}')
            print(f'Заголовок заметки - {row["Заголовок"]}')
            print(f'Текст заметки - {row["Текст заметки"]}')
            print(f'Дата/время создания или последнего изменения заметки - {row["Дата/время создания или последнего изменения заметки"]}')
            print("---------------------------------------------------------")

# Метод для добавления заметки
def add_note():
    if quit_program(): return # Метод для принудительного завершения программы

    global ID # Использование глобальной переменной

    print("---------------------------------------------------------")
    with open(FILE, mode="a", encoding='utf-8') as w_file:
        names = ["ID", "Заголовок", "Текст заметки", "Дата/время создания или последнего изменения заметки"]
        file_writer = csv.DictWriter(w_file, delimiter = ";", lineterminator="\r", fieldnames=names)
        current_datetime = datetime.now().replace(microsecond=0) # Получаем текущую дату и время
        # Запрашиваем данные у пользователя
        file_writer.writerow({"ID": ID, "Заголовок": input("Введите заголовок заметки: "), 
                              "Текст заметки": input("Введите текст заметки: "),
                              "Дата/время создания или последнего изменения заметки": current_datetime})
    ID += 1 # Увеличиваем номер ID
    print("---------------------------------------------------------")

# Метод для отображения меню
def hello_menu():
    print(Fore.CYAN + Back.BLACK + "---------------------------------------------------------")
    print(Fore.CYAN + Back.BLACK + "Добро пожаловать в NOTES!")
    print(Fore.CYAN + Back.BLACK + "Выберите действие:")
    print(Fore.CYAN + Back.BLACK + "Вывести все заметки - 1")
    print(Fore.CYAN + Back.BLACK + "Добавить заметку - 2")
    print(Fore.CYAN + Back.BLACK + "Удалить заметку - 3")
    print(Fore.CYAN + Back.BLACK + "Изменить заметку - 4")
    print(Fore.CYAN + Back.BLACK + "Поиск по ключевым словам - 5")
    print(Fore.CYAN + Back.BLACK + "Завершить работу NOTES - 6")
    print(Fore.CYAN + Back.BLACK + "Напечатать варианты действий снова - 7")
    print(Fore.CYAN + Back.BLACK + "---------------------------------------------------------")

# Основной метод для старта программы
def main():
    global ID # Использование глобальной переменной

    with open(FILE, mode="a", encoding='utf-8') as w_file:
        names = ["ID", "Заголовок", "Текст заметки", "Дата/время создания или последнего изменения заметки"]
        file_writer = csv.DictWriter(w_file, delimiter = ";", lineterminator="\r", fieldnames=names)
        if w_file.tell() == 0: # Если файл пустой, то добавляем заголовки и устанавливаем ID = 1
            file_writer.writeheader()
            ID = 1
        else: # Иначе: получаем последнюю строку и получаем из него номер ID
            last_line = get_last_line().split(';')
            if len(last_line) > 1 and last_line[0].isdigit(): # Если длина последней строки больше 1 элемента И первый символ этой строки - число, то
                ID = int(last_line[0]) + 1 # Устанавливаем номер следующий в порядке
            else: 
                ID = 1
    
    flag = True # Устанавливаем флаг для выхода из программы
    hello_menu() # Запускаем главное меню

    while(flag): # Пока флаг = истина, запрашиваем действия от пользователя
        try:
            choosen_mode = int(input("Введите номер режима: "))
            print("***                                                   ***")
            match choosen_mode:
                case 1:
                    read_file()
                case 2:
                    add_note()
                case 3:
                    delete_note()
                case 4:
                    edit_note()
                case 5:
                    find_note()
                case 6:
                    flag = False
                case 7:
                    hello_menu()

        except ValueError: # Если ввели не число: запрашиваем снова
            print("Введите число от 1 до 7.")
        except Exception as e: # При возникновении ошибки выводим:
            print(f"Возникла ошибка: {e}")

main() # Вызов основного метода