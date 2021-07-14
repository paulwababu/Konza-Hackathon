from django.shortcuts import render, HttpResponse
import requests
from django.shortcuts import render, redirect
from datetime import datetime
from PIL import Image
from datetime import date, timedelta, datetime
from django.db.models import Sum, Count
from .models import CarWash
from django.core.paginator import Paginator
# Create your views here.

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        json = {
            "username":username,
            "email":"paulkiragu621@gmail.com",
            "password":password,
        }
        response = requests.post("https://alienxconnections.tk/api/v1/rest-auth/login/", json=json)
        print(response.json)
        if response.status_code == 200:
            print(response.json())
            request.session['user'] = username
            token = response.json()
            access_token = token['key']
            request.session['access_token'] = access_token
            request.session['user'] = username
            return redirect('hom')
    return render(request, 'login.html')


def hom(request):
    try:
        token = request.session['access_token']
        print(token)
    except:
        return render(request, "home2.html")
    if request.method == 'POST':
        # Read the image
        myfile = request.FILES['file']
        files = {'upload': myfile.read()}
        response = requests.post(
                'https://api.platerecognizer.com/v1/plate-reader/',
                files=files,
                headers={'Authorization': 'Token 8fbd82dc536e9a755503979990d867b6746718a4'})
        #print(response.json())
        raw = response.json()
        cleaned = raw.get('results')
        for cleaner in cleaned:
            plate = cleaner['plate']
            vehicletype = cleaner['vehicle']['type']
        data = {
            'licensePlate':plate,
            'vehicleType':vehicletype,
            'amountPaid':200,
        }
        response2 = requests.post("https://alienxconnections.tk/api/v1/carwash/", json=data ,headers={'Authorization': f'Token {token}'})
        print(response2.json())
    return render(request, 'index.html')

def reports(request):
    try:
        token = request.session['access_token']
    except:
        return render(request, "home2.html")
    response2 = requests.get('https://alienxconnections.tk/api/v1/carwash', headers={'Authorization': f'Token {token}'})
    raw = response2.json()
    cleanerData = raw.get('results')
    print(raw)
    ###############################PAGINATE###############################
    p = Paginator(cleanerData, 10)
    ##print(p.count)#shows number of items in page
    pageNum = request.GET.get('page', 1)
    page1 = p.page(pageNum)

    #cars washed daily
    today = date.today()
    d1 = today.strftime("%Y-%m-%d")
    response3 = requests.get('https://alienxconnections.tk/api/v1/carwash?search='+d1, headers={'Authorization': f'Token {token}'})
    carsWashedDaily = response3.json()
    carsWashed = carsWashedDaily['count']
    
    #money collected daily
    moneyCollected = CarWash.objects.filter(created_date__date=today)
    mymula = moneyCollected.aggregate(Sum("amountPaid"))
    mula = (mymula.get('amountPaid__sum') or 0)

    #cars washed weekly
    startdate = datetime.today()
    enddate = startdate - timedelta(days=6)
    carsWashedWeekly = CarWash.objects.filter(created_date__range=[enddate, startdate])
    carsWashedWeek = carsWashedWeekly.count()

    #amount collected weekly
    mymulaWeekly = carsWashedWeekly.aggregate(Sum("amountPaid"))
    mulaWeekly = (mymulaWeekly.get('amountPaid__sum') or 0)

    username = request.session['user']

    #search form
    if request.method == 'POST':
        tSearch = request.POST['toSearch']
        print(tSearch)
        toSach = requests.get('https://alienxconnections.tk/api/v1/carwash?search='+tSearch, headers={'Authorization': f'Token {token}'})
        sach = toSach.json()
        sachNew = sach.get('results')
        p = Paginator(sachNew, 10)
        ##print(p.count)#shows number of items in page
        pageNum = request.GET.get('page', 1)
        page1 = p.page(pageNum)

        context2 = {
            "mulaWeekly":mulaWeekly,
            "carsWashedWeekly":carsWashedWeek,
            "moneyCollected":mula,
            "carsWashed":carsWashed,
            "username":username,
            "page1":page1
        }
        return render(request, 'reports.html', context2)
    context = {
        "mulaWeekly":mulaWeekly,
        "carsWashedWeekly":carsWashedWeek,
        "moneyCollected":mula,
        "carsWashed":carsWashed,
        "username":username,
        "page1":page1
    }
    return render(request, 'reports.html', context)

#redirect view
def home2(request):
    return render(request, "home2.html")

#logout view
def logout(request):
    try:
        token = request.session['access_token']
    except:
        return render(request, "home2.html")
    json={"token": f'{token}', "userId": "1"}
    headers = {'Authorization': f'Token {token}'}
    response3 = requests.post('https://alienxconnections.tk/api/v1/rest-auth/logout/', json=json, headers=headers)
    print(response3.status_code)
    del request.session['user']
    del request.session['access_token']
    return redirect('login')
