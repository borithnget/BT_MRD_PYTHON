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
            elif id == 2:
                ws_pipe_url = "http://127.0.0.1:8000/en/api/watersupplypipe/"
                payload_pipe = {
                    "watersupply_id" : res_json['data']['id'],
                    "is_active": True,
                    "source_type_of_water": request.POST["source_type_of_water"],
                    "abilty_of_produce_water":request.POST["abilty_of_produce_water"],
                    "underground_pool_storage": request.POST["underground_pool_storage"],
                    "pool_air": request.POST["pool_air"],
                    "pool_filter": request.POST["pool_filter"],
                    "number_of_link": request.POST["number_of_link"],
                    "water_quality_check": request.POST["water_quality_check"],
                    "status": request.POST["status"],
                    "status_no_reason":request.POST["status_no_reason"]                  
                }
                response_pipe_json = requests.post(ws_pipe_url, json=payload_pipe, headers=headers).json()
            elif id == 3:
                ws_kiosk_url = "http://127.0.0.1:8000/en/api/watersupplykiosk/"
                payload_kiosk = {               
                    "watersupply_id": res_json['data']['id'],
                    "is_active": True,
                    "source_type_of_water": request.POST["source_type_of_water"],
                    "abilty_of_produce_water": request.POST["abilty_of_produce_water"],
                    "filter_system": request.POST["filter_system"],
                    "water_quality_checking": request.POST["water_quality_checking"],
                    "status": request.POST["status"],
                    "status_no_reason": request.POST["status_no_reason"]                      
                }
                response_kiosk_json = requests.post(ws_kiosk_url, json=payload_kiosk, headers=headers).json()
            elif id == 4:
                ws_community_pond_url = "http://127.0.0.1:8000/en/api/watersupplycommunitypond/"
                payload_community_pond = {
                    "watersupply_id": res_json['data']['id'],
                    "is_active": True,
                    "width": request.POST["width"],
                    "length": request.POST["length"],
                    "height": request.POST["height"],
                    "pool_filter": request.POST["pool_filter"],
                    "type_of_pond": request.POST["type_of_pond"],
                    "is_summer_has_water": request.POST["is_summer_has_water"],
                    "status": request.POST["status"],
                    "status_no_reason": request.POST["status_no_reason"]  
                }
                response_community_pond_json = requests.post(ws_community_pond_url, json=payload_community_pond, headers=headers).json()
            elif id == 5:
                ws_rain_water_harvesting_url = "http://127.0.0.1:8000/en/api/watersupplyrainwaterharvesting/"
                payload_rain_water_harvesting = {
                    "watersupply_id": res_json['data']['id'],
                    "is_active": True,
                    "type_of_using": request.POST["type_of_using"],
                    "capacity_35m3": request.POST["capacity_35m3"],
                    "capacity_4m3": request.POST["capacity_4m3"],
                    "capacity_of_rain_water_harvesting": request.POST["capacity_of_rain_water_harvesting"],
                    "status": request.POST["status"],
                    "status_no_reason": request.POST["status_no_reason"]  
                }
                response_rain_water_harvesting_json = requests.post(ws_rain_water_harvesting_url, json=payload_rain_water_harvesting, headers=headers).json()
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

def user_register(request):
    
    if request.method == "POST":
        
        url = "http://127.0.0.1:8000/en/api/register/"
        is_data_entry = request.POST.get('is_data_entry', False)
        
        payload = {
            "username": request.POST["username"],
            "email": request.POST["email"],
            "password": request.POST["password"],
            "is_data_entry": bool(is_data_entry)
        }       
        print(payload)
        headers = {'Content-Type': 'application/json'}
        #response = requests.post(url1, json=payload, headers=headers)
        response = requests.post(url, json=payload, headers=headers).json()
        
        print(response)
        
        return redirect("user_index")
        
    return render(request, 'users/register.html')

#END USER SECTION
