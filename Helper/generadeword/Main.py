import mimetypes
import os
import random
from django.http import HttpResponse
from docxtpl import DocxTemplate

TemplateMass1 = ["очной", "заочной", "очно-заочной"]
TemplateMass2 = ["очную", "заочную", "очно-заочную"]
GenderMass = ["студенки", "студента"]


# Функкция создания ворд документа по шаблону
def CreateWord(gender, group, surname, name, lastname, number, typeconcession):
    # Проверка на пустоту
    if gender is None or group is None or surname is None or name is None or lastname is None or number is None or typeconcession is None:
        return "Error NoData"
    # Проверка наличия данных
    if gender == '' or group == '' or surname == '' or name == '' or lastname == '' or number == '' or typeconcession == '':
        return "Error NoData"
    # Проверка длинны полученных данных, ограничение 128 символов
    if len(group) > 128 or len(group) > 128 or len(group) > 128 or len(group) > 128 or len(group) > 128 or len(
            group) > 128:
        return "Error Len"

    # Проверка полученного пола, и перевод его в текст
    if gender != "1" and gender != "0":
        return "Error Gender"
    gender = GenderMass[int(gender)]

    # Задание параметров для шаблона и сохранение результата
    random.seed()
    doc = DocxTemplate("template1.docx")
    context = {'gender': gender,
               'group': group,
               'surname': surname,
               'name': name,
               'lastname': lastname,
               'number': number,
               'typeconcession': typeconcession}
    doc.render(context)
    LogFile = True
    File_Path = ""
    while LogFile:
        try:
            File_Path = "temp" + str(random.randint(1, 10000)) + ".docx"
            file = open(File_Path)
            file.close()
        except IOError as e:
            break

    # Формирование ответа для пользователя
    doc.save(File_Path)
    File_Path = os.path.abspath(File_Path)
    fp = open(File_Path, "rb")
    response = HttpResponse(fp.read())
    fp.close()
    file_type = mimetypes.guess_type(File_Path)
    if file_type is None:
        file_type = 'application/octet-stream'
    response['Content-Type'] = file_type
    response['Content-Length'] = str(os.stat(File_Path).st_size)
    response['Content-Disposition'] = "attachment; filename=Zaiavlenui_Na_matpomosh.docx"

    # Чистка временнойго файла
    os.remove(File_Path)
    return response
