import mimetypes
import os
import random
from django.http import HttpResponse
from docxtpl import DocxTemplate

TemplateMass1 = ["очной", "заочной", "очно-заочной"]
TemplateMass2 = ["очную", "заочную", "очно-заочную"]
GenderMass = ["студенки", "студента"]
ConcessionMass = ["студент-сирота", "cтудент-инвалид", "cтудент, имеющий детей", "cтудент из многодетной семьи", "cтудент-участник военных действий", "cтудент-чернобылец", "cтудент, имеющий родителей-инвалидов, родителей-пенсионеров", "cтудент из неполной семьи", "cтудент из малоимущей семьи", "cтудент, находящийся на диспансерном учёте с хроническими заболеваниями", "студент, проживающий в общежитии"]

# Выбор зам декана по курсу
def chooseDirector(group):
    director = group[4]
    director = {
        '1': "И.А. Коновал",
        '2': "Т.В. Гаранина",
        '3': "И.М. Самойлова",
        '4': "Н.Ю. Лахметкина",
        '5': "Е.В. Бычкова",
    }.get(director, 0)
    return director

# Функкция создания ворд документа по шаблону
def CreateWord(gender, group, surname, name, lastname, number, typeconcession, chooseDoc):
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
    if chooseDoc == '1':
        doc = DocxTemplate("template1.docx")
    elif chooseDoc == '2':
        doc = DocxTemplate("template2.docx")
        #doc = DocxTemplate("BlankMatHelp.docx")
        typeconcession = 10
    else:
        print("chooseDoc error")
        return "Error no chooseDoc"

    if int(typeconcession) < 0 or int(typeconcession) > 10:
        return "Error typeConcession"
    typeconcession = ConcessionMass[int(typeconcession)]

    director = chooseDirector(group)

    context = {'gender': gender,
               'group': group,
               'surname': surname,
               'name': name,
               'lastname': lastname,
               'number': number,
               'typeconcession': typeconcession,
               'director': director}

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
