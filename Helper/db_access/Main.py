import mimetypes
import os
import sqlite3

from django.http import HttpResponse
from xlsxwriter import Workbook

GenderMass = ["студенки", "студента"]

# Функция создания базы данных, запускать только один раз при ее создании
def First_Init():
    conn = sqlite3.connect(os.path.abspath("Helper\db_access\db_s.db"))
    cursor = conn.cursor()
    # Создание таблицы
    cursor.execute("""  CREATE TABLE comments ( 
                        post_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
                        surname TEXT NOT NULL, 
                        name TEXT NOT NULL, 
                        lname TEXT NOT NULL, 
                        group2 TEXT NOT NULL, 
                        number TEXT NULL, 
                        typeconcession TEXT NOT NULL, 
                        gender TEXT NULL);""")
    conn.commit()
    conn.close()
    return

# Функция добавления данных в БД, если такой записи нету
def Insert_Data(gender, group, surname, name, lastname, number, typeconcession):
    gender = GenderMass[int(gender)]
    conn = sqlite3.connect(os.path.abspath("Helper\db_access\db_s.db"))
    cursor = conn.cursor()
    StringSQLtext = "SELECT * FROM comments WHERE surname = '"+surname+"' AND name = '"+name+"' AND lname = '"+lastname+"' AND group2 = '"+group+"' AND number = '"+number+"' AND typeconcession = '"+typeconcession+"' AND gender = '"+gender+"'"
    cursor.execute(StringSQLtext)
    mysel = cursor.fetchall()
    if mysel != []:
        return
    # Создание таблицы
    StringSQLtext = "INSERT INTO comments ( surname, name, lname, group2, number, typeconcession, gender ) VALUES ( '"+surname+"', '"+name+"', '"+lastname+"', '"+group+"', '"+number+"', '"+typeconcession+"', '"+gender+"' ); "
    cursor.execute(StringSQLtext)
    conn.commit()
    conn.close()
    return

# Функция генерации экселя по данным из БД
def Get_Data():
    conn = sqlite3.connect(os.path.abspath("Helper\db_access\db_s.db"))
    c = conn.cursor()
    workbook = Workbook('db_accel.xlsx')
    worksheet = workbook.add_worksheet()
    c.execute("select * from comments")
    mysel = c.execute("select * from comments ")
    for i, row in enumerate(mysel):
        for j, value in enumerate(row):
            worksheet.write(i, j, row[j])
    workbook.close()
    conn.close()
    File_Path = os.path.abspath('db_accel.xlsx')
    fp = open(File_Path, "rb")
    response = HttpResponse(fp.read())
    fp.close()
    file_type = mimetypes.guess_type(File_Path)
    if file_type is None:
        file_type = 'application/octet-stream'
    response['Content-Type'] = file_type
    response['Content-Length'] = str(os.stat(File_Path).st_size)
    response['Content-Disposition'] = "attachment; filename=Spisok_Podavshix.xlsx"

    # Чистка временнойго файла
    os.remove(File_Path)
    return response

if __name__ == '__main__':
    First_Init()