import re
import threading

from django.contrib.sites import requests
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from Helper import settings
from Helper.generadeword.Main import CreateWord
from Helper.db_access.Main import Insert_Data, Get_Data as Data_Base
from Helper.rsa_path.Main import Get_Path

from django.conf import settings
from g_recaptcha.validate_recaptcha import validate_captcha
# путь для получения данных, выдается в шифрованном виде
Patch_Of_Get = "Non"

@validate_captcha
def Set_Data(request):
    name = request.GET.get('name', '')
    lname = request.GET.get('lname', '')
    surname = request.GET.get('surname', '')
    group = request.GET.get('group', '')
    number = request.GET.get('number', '')
    typeconcession = request.GET.get('typeconcession', '')
    gender = request.GET.get('gender', '')
    # урезание строки
    gender = re.sub(" +", ' ', gender.strip())
    group = re.sub(" +", ' ', group.strip())
    surname = re.sub(" +", ' ', surname.strip())
    name = re.sub(" +", ' ', name.strip())
    lname = re.sub(" +", ' ', lname.strip())
    number = re.sub(" +", ' ', number.strip())
    typeconcession = re.sub(" +", ' ', typeconcession.strip())
    respons = CreateWord(gender, group, surname, name, lname, number, typeconcession)
    if respons != "Error Gender" and respons != "Error NoData" and respons != "Error Len":
        t = threading.Thread(target=Insert_Data, args=(gender, group, surname, name, lname, number, typeconcession))
        t.daemon = True
        t.start()
        return respons
    return HttpResponse(respons)

# Рендер главной страницы
@validate_captcha
def Index(request):
    return render(request, '123.html')

# Перенапрвление на главную страницу
def Any_Page(request):
    return redirect("/index")

# Запрос на создание ссылки для загрузки
def Get_Data(request):
    (Patch,Patch_Cript) = Get_Path()
    global Patch_Of_Get
    Patch_Of_Get = Patch
    print("Генерация динамической ссылки для загрузки")
    threading.Timer(10, Clear_Page).start()
    return HttpResponse(Patch_Cript)

# Удаление ссылки на загрузку
def Clear_Page():
    print("Очистка динамической ссылки для загрузки")
    global Patch_Of_Get
    Patch_Of_Get = "Non"
    return

# Выдача данных из базы данных
def Page_Return_Data(request, path):
    global Patch_Of_Get
    if path == Patch_Of_Get and Patch_Of_Get != "Non":
        Patch_Of_Get = "Non"
        return Data_Base()
    return redirect("/index")


