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
    context = {
        'GOOGLE_RECAPTCHA_SITE_KEY': settings.GOOGLE_RECAPTCHA_SITE_KEY,
    }

    return render(request, '123.html', context)

# Рендер главной страницы
def Any_Page(request):
    return redirect("/index")

# Обработка выдачи данных
def Get_Data(request):
    (Patch,Patch_Cript) = Get_Path()
    global Patch_Of_Get
    Patch_Of_Get = Patch
    print("Генерация динамической ссылки для загрузки")
    threading.Timer(1, Clear_Page).start()
    return HttpResponse(Patch_Cript)

def Clear_Page():
    print("Очистка динамической ссылки для загрузки")
    global Patch_Of_Get
    Patch_Of_Get = "Non"
    return

def Page_Return_Data(request, path):
    global Patch_Of_Get
    if path == Patch_Of_Get and Patch_Of_Get != "Non":
        Patch_Of_Get = "Non"
        return Data_Base()
    return redirect("/index")

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def grecaptcha_verify(request):
    if request.method == 'POST':
        response = {}
        data = request.POST
        captcha_rs = data.get('g-recaptcha-response')
        url = "https://www.google.com/recaptcha/api/siteverify"
        params = {
            'secret': settings.RECAPTCHA_SECRET_KEY,
            'response': captcha_rs,
            'remoteip': get_client_ip(request)
        }
        verify_rs = requests.get(url, params=params, verify=True)
        verify_rs = verify_rs.json()
        response["status"] = verify_rs.get("success", False)
        response['message'] = verify_rs.get('error-codes', None) or "Unspecified error."
        return HttpResponse(response)