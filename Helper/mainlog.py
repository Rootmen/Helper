
# Переход на get/ страницу если есть все параметры, иначе очередной рендер + дублирование ввода в cmd
from django.http import HttpResponse
from django.shortcuts import render
from Helper.generadeword.Main import CreateWord
from Helper.db_access.Main import Insert_Data, Get_Data as Data_Base


# Обработка получения данных
def Set_Data(request):
    name = request.GET.get('name', '')
    lname = request.GET.get('lname', '')
    surname = request.GET.get('surname', '')
    group = request.GET.get('group', '')
    number = request.GET.get('number', '')
    typeconcession = request.GET.get('typeconcession', '')
    gender = request.GET.get('gender', '')
    respons = CreateWord(gender, group, surname, name, lname, number, typeconcession)
    if respons != "Error Gender" and respons != "Error NoData" and respons != "Error Len":
        Insert_Data(gender, group, surname, name, lname, number, typeconcession)
        return respons
    return HttpResponse(respons)

# Рендер главной страницы
def Index(request):
    return render(request, '123.html')

# Обработка выдачи данных
def Get_Data(request):
    return Data_Base()