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

# СДЕЛАТЬ: документацию, обработку исключений, выход из программы и фильтрацию по дате

import csv
from datetime import datetime

FILE = "notes.csv"
ID = 0

def find_note():
    user_input = input("Введите слово/выражение, по которому надо вывести заметку: ")
    with open(FILE, 'r', encoding='utf-8') as file:
        file_reader = csv.DictReader(file, delimiter = ";")

        for row in file_reader:
            for value in row.values():
                value_casefold = value.casefold()
                if user_input.casefold() in value_casefold:
                    print("---------------------------------------------------------")
                    print(f'ID заметки - {row["ID"]}')
                    print(f'Заголовок заметки - {row["Заголовок"]}')
                    print(f'Текст заметки - {row["Текст заметки"]}')
                    print(f'Дата/время создания или последнего изменения заметки - {row["Дата/время создания или последнего изменения заметки"]}')
                    print("---------------------------------------------------------")

def edit_note():
    global ID

    notes_copy = copy_file()
    id_set = set()
    print("---------------------------------------------------------")

    edit_id = int(input("Введите ID заметки, которую нужно изменить: "))
    for row in notes_copy:
        id_set.add(row['ID'])
    
    if str(edit_id) not in id_set:
        print("Нет заметки с таким ID")
    else:
        for row in notes_copy:
            if row['ID'] == str(edit_id):
                current_datetime = datetime.now().replace(microsecond=0)

                row['Заголовок'] = input("Введите заголовок: ")
                row['Текст заметки'] = input("Введите текст заметки: ")
                row['Дата/время создания или последнего изменения заметки'] = current_datetime
    print("---------------------------------------------------------")
    
    
    with open(FILE, 'w', encoding='utf-8') as file:
        names = ["ID", "Заголовок", "Текст заметки", "Дата/время создания или последнего изменения заметки"]
        file_writer = csv.DictWriter(file, delimiter = ";", lineterminator="\r", fieldnames=names)

        if file.tell() == 0:
            file_writer.writeheader()
        for dict in notes_copy:
            file_writer.writerow({"ID": dict['ID'], "Заголовок": dict['Заголовок'], 
                    "Текст заметки": dict['Текст заметки'], "Дата/время создания или последнего изменения заметки": 
                    dict['Дата/время создания или последнего изменения заметки']})


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

def copy_file():
    res_list = list()

    with open(FILE, encoding='utf-8') as r_file:
        file_reader = csv.DictReader(r_file, delimiter = ";")

        for row in file_reader:
            res_list.append(row)

    return res_list

def delete_note():
    global ID

    id_set = set()
    notes_copy = copy_file()
    print("---------------------------------------------------------")

    delete_id = int(input("Введите ID заметки, которую нужно удалить: "))
    for row in notes_copy:
        id_set.add(row['ID'])

    if str(delete_id) not in id_set:
        print("Нет заметки с таким ID")
    else:
        for row in notes_copy:
            if row['ID'] == str(delete_id):
                row.clear()

        notes_copy = [i for i in notes_copy if i]
        with open(FILE, 'w', encoding='utf-8') as copy_f:
            names = ["ID", "Заголовок", "Текст заметки", "Дата/время создания или последнего изменения заметки"]
            file_writer = csv.DictWriter(copy_f, delimiter = ";", lineterminator="\r", fieldnames=names)

            if copy_f.tell() == 0:
                file_writer.writeheader()
            for dict in notes_copy:
                file_writer.writerow({"ID": dict['ID'], "Заголовок": dict['Заголовок'], 
                        "Текст заметки": dict['Текст заметки'], "Дата/время создания или последнего изменения заметки": 
                        dict['Дата/время создания или последнего изменения заметки']})


def read_file():
    with open(FILE, encoding='utf-8') as r_file:
        file_reader = csv.DictReader(r_file, delimiter = ";")

        for row in file_reader:
            print("---------------------------------------------------------")
            print(f'ID заметки - {row["ID"]}')
            print(f'Заголовок заметки - {row["Заголовок"]}')
            print(f'Текст заметки - {row["Текст заметки"]}')
            print(f'Дата/время создания или последнего изменения заметки - {row["Дата/время создания или последнего изменения заметки"]}')
            print("---------------------------------------------------------")

            
def add_note():
    global ID

    print("---------------------------------------------------------")
    with open(FILE, mode="a", encoding='utf-8') as w_file:
        names = ["ID", "Заголовок", "Текст заметки", "Дата/время создания или последнего изменения заметки"]
        file_writer = csv.DictWriter(w_file, delimiter = ";", lineterminator="\r", fieldnames=names)
        current_datetime = datetime.now().replace(microsecond=0)
        file_writer.writerow({"ID": ID, "Заголовок": input("Введите заголовок заметки: "), 
                              "Текст заметки": input("Введите текст заметки: "),
                              "Дата/время создания или последнего изменения заметки": current_datetime})
    ID += 1
    print("---------------------------------------------------------")


def hello_menu():
    print("---------------------------------------------------------")
    print("Добро пожаловать в NOTES!")
    print("Выберите действие:")
    print("Вывести все заметки - 1")
    print("Добавить заметку - 2")
    print("Удалить заметку - 3")
    print("Изменить заметку - 4")
    print("Поиск по ключевым словам - 5")
    print("Завершить работу NOTES - 6")
    print("Напечатать варианты действий снова - 7")
    print("---------------------------------------------------------")

def main():
    global ID

    with open(FILE, mode="a", encoding='utf-8') as w_file:
        names = ["ID", "Заголовок", "Текст заметки", "Дата/время создания или последнего изменения заметки"]
        file_writer = csv.DictWriter(w_file, delimiter = ";", lineterminator="\r", fieldnames=names)
        if w_file.tell() == 0:
            file_writer.writeheader()
            ID = 1
        else:
            last_line = get_last_line().split(';')
            if len(last_line) > 1 and last_line[0].isdigit():
                ID = int(last_line[0]) + 1
            else:
                ID = 1
    
    flag = True
    hello_menu()

    while(flag):
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

main()