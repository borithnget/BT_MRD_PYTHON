from email import header
from urllib import response
from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
import json
from rest_framework.parsers import JSONParser
import datetime
# Create your views here.
MAIN_URL = 'http://127.0.0.1:8000/api/' 

def index(request):
    response = requests.get('http://127.0.0.1:8000/en/api/watersupplytype/')
    watersupplytypelist = response.json()
    
    water_supply_url = MAIN_URL + 'watersupply/'
    watersupplylist = requests.get(water_supply_url).json()
    
    return render(request, 'watersupply/watersupplytype.html', {'watersupplytypes': watersupplytypelist, 'watersupplylist':watersupplylist })

def create_watersupply(request, id):
    
    url = MAIN_URL+ 'watersupplytypeoption/?search=' + str(id)
    response = requests.get(url)
    watersupplytypeoptions = response.json()
    
    province_url = MAIN_URL + 'province'
    provinces = requests.get(province_url).json()
    
    if request.method == "POST":
        
        url1 = "http://127.0.0.1:8000/en/api/v2/watersupply"

        payload = {
            "water_supply_type_id": id,
            "province_id": request.POST['province'],
            "district_id": request.POST['district'],
            "created_by":  request.user.id,
            "updated_by":  request.user.id,
            "is_active": True,
            "is_risk_enviroment_area": request.POST['is_risk_enviroment_area'] ,
            "commune_id": request.POST["commune"],
            "village_id": request.POST["village"],
            "construction_date": request.POST["construction_date"]
            
        }

        print(payload)
        headers = {'Content-Type': 'application/json'}
        #response = requests.post(url1, json=payload, headers=headers)
        response = requests.post(url1, json=payload, headers=headers)
        res_json  = response.json()
        print(res_json)
        
        if 'status' in res_json:
            return redirect('index')
    
    return render(request, 'watersupply/create.html', 
                  {'id': id, 
                   'watersupplytypeoptions':watersupplytypeoptions,
                   'provinces': provinces
                   }
                  )

def detail(request, id):
    print(id)
    water_supply_url = MAIN_URL + 'watersupply/' + str(id)
    watersupply = requests.get(water_supply_url).json()
    return render(request, 'watersupply/detail.html', {'watersupply': watersupply})

#START USER SECTION

def user_index(request):
    user_list_url = MAIN_URL + 'userlist/'
    users = requests.get(user_list_url).json()
    return render(request, 'users/index.html' , {'users': users})

#END USER SECTION
