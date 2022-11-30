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
            "construction_date": request.POST["construction_date"],
            "water_supply_code" : request.POST["water_supply_code"],
            "total_family" : request.POST["total_family"],
            "utm_x": request.POST["utm_x"],
            "utm_y":request.POST["utm_y"],
            "source_budget":request.POST["source_budget"],
            "constructed_by":request.POST["constructed_by"],
            "management_type":request.POST["management_type"],
            "managed_by":request.POST["managed_by"],
            "beneficiary_total_people":request.POST["beneficiary_total_people"],
            "beneficiary_total_women":request.POST["beneficiary_total_women"],
            "beneficiary_total_family":request.POST["beneficiary_total_family"],
            "beneficiary_total_family_poor_1":request.POST["beneficiary_total_family_poor_1"],
            "beneficiary_total_family_poor_2":request.POST["beneficiary_total_family_poor_2"],
            "beneficiary_total_family_vulnerable":request.POST["beneficiary_total_family_vulnerable"],
            "beneficiary_total_family_indigenous":request.POST["beneficiary_total_family_indigenous"]

        }

        print(payload)
        headers = {'Content-Type': 'application/json'}
        #response = requests.post(url1, json=payload, headers=headers)
        response = requests.post(url1, json=payload, headers=headers)
        res_json  = response.json()
        print(res_json)
        
        if 'status' in res_json:

            if id == 1:#Well
                ws_well_url = "http://127.0.0.1:8000/en/api/watersupplywell/"
                payload_well = {
                    "watersupply_id" : res_json['data']['id'],
                    "well_type" : request.POST['well_type'],
                    "well_height": request.POST['well_height'],
                    "well_filter_height" : request.POST["well_filter_height"],
                    "well_water_supply" : request.POST["well_water_supply"],
                    "well_nirostatic": request.POST["well_nirostatic"],
                    "well_watar_quality": request.POST["well_watar_quality"],
                    "well_water_quality_check" : request.POST["well_water_quality_check"],
                    "well_status": request.POST["well_status"],
                    "well_status_reason":request.POST["well_status_reason"],
                    "well_nirodynamic": request.POST["well_nirodynamic"],
                    "is_active": True,
                }
                response_well = requests.post(ws_well_url, json=payload_well, headers=headers)
                well_res_json = response_well.json()
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
