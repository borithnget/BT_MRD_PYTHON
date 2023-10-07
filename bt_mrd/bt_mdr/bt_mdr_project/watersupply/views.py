from email import header
from urllib import response
from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
import json
from rest_framework.parsers import JSONParser
import datetime, time
from qrcode import *
from django.conf import settings
from mdrapp import models
import pandas as pd
import os
from django.core.files.storage import FileSystemStorage

# Create your views here.
# MAIN_URL = 'http://13.212.250.28/api/' 
# MAIN_URL_1 = 'http://13.212.250.28/en/'

MAIN_URL = 'http://127.0.0.1:8000/api/' 
MAIN_URL_1 = 'http://127.0.0.1:8000/en/'

def index(request,id):
    watersupply_type_url = settings.API_ENDPOINT + 'watersupplytype/'
    watersupplytypelist = requests.get(watersupply_type_url).json()

    province_url = settings.API_ENDPOINT + 'province'
    provinces = requests.get(province_url).json()
    
    watersupplylist = []
    # if id ==0:
    #     water_supply_url = settings.API_ENDPOINT + 'watersupplylistbytype/?water_supply_type_id='
    # else:
    #     water_supply_url = settings.API_ENDPOINT + 'watersupplylistbytype/?water_supply_type_id=' + str(id) 
    # print(water_supply_url)
    # watersupplylist = requests.get(water_supply_url).json()

    # print(watersupplylist)

    watersupplytype_response = requests.get(settings.API_ENDPOINT+ 'watersupplytype/'+str(id)).json()

    #menu_permission
    menu_permission = models.MenuPermission.objects.all().filter(menu_id=1)
    
    return render(request, 'watersupply/watersupplytype.html', 
                  {
                      'watersupplytypes': watersupplytypelist,
                   'watersupplytype':watersupplytype_response, 
                   'watersupplylist':watersupplylist, 
                   'watersupplytype_id':id, 
                   'menu_permission':menu_permission ,
                   'provinces' : provinces
                   }
                   )

def create_watersupply(request, id):
    
    url = MAIN_URL+ 'watersupplytypeoption/?search=' + str(id)
    response = requests.get(url)
    watersupplytypeoptions = response.json()
    
    if request.session['user']['is_data_entry']:
        province_url = MAIN_URL + 'province/?id=' + str(request.session['user']['data_entry_province_id'])
        #print(request.user.data_entry_province_id.id)
    else:
        province_url = MAIN_URL + 'province'
    provinces = requests.get(province_url).json()
    #print(provinces)

    watersupplytype_response = requests.get(MAIN_URL+ 'watersupplytype/'+str(id)).json()

    
    if request.method == "POST":
        
        url1 = "http://13.212.250.28/en/api/v2/watersupply"

        main_status = request.POST.get('main_status')
       
        if main_status == '1':    
            print(main_status)
            if request.session['user']['is_head_department']:
                main_status = 9
            elif request.session['user']['is_data_verifier_2']:
                main_status = 7
            elif request.session['user']['is_data_verifier_1']:
                main_status = 5
            elif request.session['user']['is_provincial_department_head']:
                main_status = 2
            elif request.session['user']['is_data_entry']:
                main_status = 1
            
        payload = {
            "water_supply_type_id": id,
            "province_id": request.POST['province'],
            "district_id": request.POST['district'],
            "created_by":  request.session['user']['id'],
            "updated_by":  request.session['user']['id'],#
            "is_active": True,
            "is_risk_enviroment_area": request.POST['is_risk_enviroment_area'] ,
            "commune_id": request.POST["commune"],
            "village_id": request.POST["village"],
            "construction_date": request.POST["construction_date"],
            "water_supply_code" : request.POST["water_supply_code"],
            "total_family" : request.POST["total_family"],
            "utm_x": request.POST.get("utm_x"),
            "utm_y":request.POST.get("utm_y"),
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
            "beneficiary_total_family_indigenous":request.POST["beneficiary_total_family_indigenous"],
            "main_status":main_status,
            "is_water_quality_check": request.POST["is_water_quality_check"],
            "map_unit" : request.POST.get("map_unit"),
            "decimal_degress_lat" : request.POST.get("decimal_degress_lat"),
            "decimal_degress_lng" : request.POST.get("decimal_degress_lng"),
            "mds_x_degress" : request.POST.get("mds_x_degress"),
            "mds_x_minute" : request.POST.get("mds_x_minute"),
            "mds_x_second" : request.POST.get("mds_x_second"),
            "mds_y_degress" : request.POST.get("mds_y_degress"),
            "mds_y_minute" : request.POST.get("mds_y_minute"),
            "mds_y_second" : request.POST.get("mds_y_second")
        }

        print(payload)
        headers = {'Content-Type': 'application/json'}
        #response = requests.post(url1, json=payload, headers=headers)

        response = requests.post(url1, json=payload, headers=headers)
        res_json  = response.json()
        # print(res_json)
        
        if 'status' in res_json:

            #water supply workflow
            ws_workflow = "http://13.212.250.28/en/api/v2/watersupplyworkflow"
            payload_wsworkflow = {
                "watersupply_id": res_json['data']['id'],
                "status_id": main_status,
                "user_id": request.session['user']['id'],
                "remark": ""
            }
            response_ws_workflow = requests.post(ws_workflow, json=payload_wsworkflow, headers=headers).json()

            if id == 1:#Well
                # print(request.POST['well_type'])
                ws_well_url = "http://13.212.250.28/en/api/watersupplywell/"
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
                print(payload_well)
                response_well = requests.post(ws_well_url, json=payload_well, headers=headers)
                well_res_json = response_well.json()                
                # print(well_res_json)
                if 'id' in well_res_json:
                    ws_option_value_url = "http://13.212.250.28/en/api/watersupplywelloptionvalue/"
                    split_well_type_values = request.POST['well_type'].split(',')
                    # print(split_well_type_values)
                    for well_type_value in split_well_type_values:
                        payload_well_option_value ={
                            "water_supply_well_id": well_res_json['id'],
                            "option_id": 1,
                            "value_id":int(well_type_value),
                            "is_active": True
                        }
                        response_well_option_value = requests.post(ws_option_value_url,json=payload_well_option_value, headers=headers).json()
                        print(payload_well_option_value)
            elif id == 2:
                ws_pipe_url = "http://13.212.250.28/en/api/watersupplypipe/"
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
                    "status_no_reason":request.POST["status_no_reason"],
                    "pipe_length": request.POST["pipe_length"],
                    "area_covering": request.POST["area_covering"]               
                }
                response_pipe_json = requests.post(ws_pipe_url, json=payload_pipe, headers=headers).json()
                # print(response_pipe_json)
                if 'id' in response_pipe_json:
                    ws_pipe_option_value_url = "http://13.212.250.28/en/api/watersupplypipoptionvalue/"
                    split_pipe_source_water_values = request.POST['source_type_of_water'].split(',')
                    for pipe_source_water in split_pipe_source_water_values:
                        payload_pipe_option_value = {
                            "water_supply_pipe_id": response_pipe_json['id'],
                            "option_id": 11,
                            "value_id": int(pipe_source_water),
                            "is_active": True
                        }
                        response_pipe_option_value = requests.post(ws_pipe_option_value_url,json=payload_pipe_option_value, headers=headers).json()
                        # print(response_pipe_option_value)

            elif id == 3:
                ws_kiosk_url = "http://13.212.250.28/en/api/watersupplykiosk/"
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
                
                if 'id' in response_kiosk_json:
                    #print(response_kiosk_json)
                    ws_kiosk_option_value_url = "http://13.212.250.28/en/api/watersupplykioskoptionvalue/"
                    #print(ws_kiosk_option_value_url)
                    split_kiosk_source_of_water_values = request.POST['source_type_of_water'].split(',')
                    #print(split_kiosk_source_of_water_values)
                    for kiosk_source_water in split_kiosk_source_of_water_values:
                        payload_kiosk_option_value = {
                            "water_supply_kiosk_id": response_kiosk_json['id'],
                            "option_id": 11,
                            "value_id": int(kiosk_source_water),
                            "is_active": True
                        }
                        #print(payload_kiosk_option_value)
                        response_kiosk_option_value = requests.post(ws_kiosk_option_value_url,json=payload_kiosk_option_value, headers=headers).json()

            elif id == 4:
                ws_community_pond_url = "http://13.212.250.28/en/api/watersupplycommunitypond/"
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
                ws_rain_water_harvesting_url = "http://13.212.250.28/en/api/watersupplyrainwaterharvesting/"
                payload_rain_water_harvesting = {
                    "watersupply_id": res_json['data']['id'],
                    "is_active": True,
                    "type_of_using": request.POST["type_of_using"],
                    "capacity_35m3": 0,
                    "capacity_4m3": 0,
                    "capacity_of_rain_water_harvesting": request.POST["capacity_of_rain_water_harvesting"],
                    "status": request.POST["status"],
                    "status_no_reason": request.POST["status_no_reason"]  ,
                    "water_quality_checking" : request.POST.get("water_quality_checking")
                }
                response_rain_water_harvesting_json = requests.post(ws_rain_water_harvesting_url, json=payload_rain_water_harvesting, headers=headers).json()           
            elif id == 6:
                ws_pipe_private_url = "http://13.212.250.28/en/api/watersupplypipeprivate/"
                payload_pipe_private = {
                    "watersupply_id" : res_json['data']['id'],
                    "is_active": True,
                    "source_type_of_water": request.POST["source_type_of_water"],
                    "abilty_of_produce_water":request.POST["abilty_of_produce_water"],
                    "underground_pool_storage": request.POST["underground_pool_storage"],
                    "pool_air": request.POST["pool_air"],
                    "pool_filter": request.POST["pool_filter"],
                    "number_of_link": request.POST["number_of_link"],
                    "water_quality_check": request.POST["well_water_quality_check"],
                    "status": request.POST["status"],
                    "status_no_reason":request.POST["well_status_reason"],
                    "pipe_length": request.POST["pipe_length"],
                    "area_covering": request.POST["area_covering"],
                    "is_has_license": request.POST["is_has_license"],
                    "license_registered_date": request.POST["license_registered_date"],
                    "license_expired_date": request.POST["license_expired_date"]
                }
                response_pipe_private_json = requests.post(ws_pipe_private_url, json=payload_pipe_private, headers=headers).json()
                # print(response_pipe_json)
                if 'id' in response_pipe_private_json:
                    ws_pipe_private_option_value_url = "http://13.212.250.28/en/api/watersupplypipeprivateoptionvalue/"
                    split_pipe_source_water_values = request.POST['source_type_of_water'].split(',')
                    for pipe_source_water in split_pipe_source_water_values:
                        payload_pipe_option_value = {
                            "water_supply_pipe_id": response_pipe_private_json['id'],
                            "option_id": 11,
                            "value_id": int(pipe_source_water),
                            "is_active": True
                        }
                        response_pipe_option_value = requests.post(ws_pipe_private_option_value_url,json=payload_pipe_option_value, headers=headers).json()
            elif id == 7:
                ws_air_water_url = "http://13.212.250.28/en/api/watersupplyairwater/"
                payload_air_water = {               
                    "watersupply_id": res_json['data']['id'],
                    "is_active": True,
                    "source_type_of_water": request.POST["source_type_of_water"],
                    "abilty_of_produce_water": request.POST["abilty_of_produce_water"],
                    "filter_system": request.POST["filter_system"],
                    "water_quality_checking": request.POST["well_water_quality_check"],
                    "status": request.POST["status"],
                    "status_no_reason": request.POST["status_no_reason"]                      
                }
                response_air_water_json = requests.post(ws_air_water_url, json=payload_air_water, headers=headers).json()
                
                if 'id' in response_air_water_json:
                    #print(response_kiosk_json)
                    ws_air_water_option_value_url = "http://13.212.250.28/en/api/watersupplyairwateroptionvalue/"
                    #print(ws_kiosk_option_value_url)
                    split_air_water_source_of_water_values = request.POST['source_type_of_water'].split(',')
                    #print(split_kiosk_source_of_water_values)
                    for air_water_source_water in split_air_water_source_of_water_values:
                        payload_air_water_option_value = {
                            "water_supply_airwater_id": response_air_water_json['id'],
                            "option_id": 11,
                            "value_id": int(air_water_source_water),
                            "is_active": True
                        }
                        print(payload_air_water_option_value)
                        response_air_water_option_value = requests.post(ws_air_water_option_value_url,json=payload_air_water_option_value, headers=headers).json()

            
            #Generate QR CODE
            detail_url = MAIN_URL_1 + "watersupply/detail/" + str(res_json['data']['id'])
            img = make(detail_url)
            img_name = 'qr' + str(time.time()) + '.png'
            img.save(settings.MEDIA_ROOT + '/' + img_name)         
            ws_qr_code_url = "http://13.212.250.28/en/api/watersupplyqrcode/"
            payload_qr_code = {
                "watersupply_id": res_json['data']['id'],
                "qr_code_image_name": img_name
            }
            response_ws_qrcode = requests.post(ws_qr_code_url, json=payload_qr_code, headers=headers).json()

            #if Water Quality Check
            wqc_param_url = "http://13.212.250.28/en/api/watersupplyqualitycheckparameter/"
            wqc_param_ids = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
       
            for param_id in wqc_param_ids:
                wqc_param_id = "wqcparam_" + str(param_id)
                wqc_param_value = request.POST.get(wqc_param_id)

                wqc_param_payload = {
                    "value": wqc_param_value,
                    "is_active": True,
                    "water_supply_id": res_json['data']['id'],
                    "water_quanlity_check_parameter_id": param_id
                }
                response_wqc_param = requests.post(wqc_param_url, json=wqc_param_payload, headers=headers).json()
                # print(wqc_param_value)
            
            return redirect('watersupply_detail', id=res_json['data']['id'])

    key = settings.GOOGLE_API_KEY
    context = {
        'key':key
    }

    water_quality_check_parameter_url = MAIN_URL + "waterquanlitycheck/" 
    water_quality_check_parameters = requests.get(water_quality_check_parameter_url).json()
    
    return render(request, 'watersupply/create.html', 
                  {'id': id, 
                   'watersupplytypeoptions':watersupplytypeoptions,
                   'provinces': provinces,
                   'watersupplytype':watersupplytype_response,
                   'key':key,
                   'water_quality_check_parameters' : water_quality_check_parameters
                   }
                  )

def detail(request, id):
    # print(id)
    water_supply_url = MAIN_URL + 'watersupply/' + str(id)
    watersupply = requests.get(water_supply_url).json()

    water_quality_check_parameter_url = MAIN_URL + "waterquanlitycheck/" 
    water_quality_check_parameters = requests.get(water_quality_check_parameter_url).json()
    
    return render(request, 'watersupply/detail.html', {
        'watersupply': watersupply, 
        'key':settings.GOOGLE_API_KEY,
        'water_quality_check_parameters' : water_quality_check_parameters
        })

def edit(request, id):
    # print(id)
    water_supply_url = MAIN_URL + 'watersupply/' + str(id)
    watersupply = requests.get(water_supply_url).json()

    watersupplyoptions_url = MAIN_URL+ 'watersupplytypeoption/?search=' + str(watersupply['water_supply_type_id']['id'])
    watersupplyoptins = requests.get(watersupplyoptions_url).json()

    if request.session['user']['is_data_entry']:
        province_url = MAIN_URL + 'province/?id=' + str(request.session['user']['data_entry_province_id'])
        #print(request.user.data_entry_province_id.id)
    else:
        province_url = MAIN_URL + 'province'
    provinces = requests.get(province_url).json()

    if request.method == "POST":
        
        url_update = "http://13.212.250.28/en/api/v2/watersupply/"+str(id)

        main_status = request.POST.get('main_status')
        
        if main_status == '1':    
            print(main_status)
            if request.session['user']['is_head_department']:
                main_status = 9
            elif request.session['user']['is_data_verifier_2']:
                main_status = 7
            elif request.session['user']['is_data_verifier_1']:
                main_status = 5
            elif request.session['user']['is_provincial_department_head']:
                main_status = 2
            elif request.session['user']['is_data_entry']:
                main_status = 1

        payload = {
            "id": id,
            "province_id": request.POST['province'],
            "district_id": request.POST['district'],
            "updated_by":  request.session['user']['id'],
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
            "beneficiary_total_family_indigenous":request.POST["beneficiary_total_family_indigenous"],
            "main_status":main_status,
            "is_water_quality_check": request.POST["is_water_quality_check"],
            "map_unit" : request.POST.get("map_unit"),
            "decimal_degress_lat" : request.POST.get("decimal_degress_lat"),
            "decimal_degress_lng" : request.POST.get("decimal_degress_lng"),
            "mds_x_degress" : request.POST.get("mds_x_degress"),
            "mds_x_minute" : request.POST.get("mds_x_minute"),
            "mds_x_second" : request.POST.get("mds_x_second"),
            "mds_y_degress" : request.POST.get("mds_y_degress"),
            "mds_y_minute" : request.POST.get("mds_y_minute"),
            "mds_y_second" : request.POST.get("mds_y_second")

        }
        headers = {'Content-Type': 'application/json'}
        #response = requests.post(url1, json=payload, headers=headers)
        response = requests.put(url_update, json=payload, headers=headers)
        res_json  = response.json()
        if 'status' in res_json:
            #water supply workflow
            ws_workflow = "http://13.212.250.28/en/api/v2/watersupplyworkflow"
            payload_wsworkflow = {
                "watersupply_id": res_json['data']['id'],
                "status_id": main_status ,
                "user_id": request.session['user']['id'],
                "remark": ""
            }
            
            response_ws_workflow = requests.post(ws_workflow, json=payload_wsworkflow, headers=headers).json()
            
            if int(request.POST['water_supply_type']) == 1:
                # print(request.POST['water_supply_type'])
                ws_well_url = "http://13.212.250.28/en/api/watersupplywell/"
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
                # print(payload_well)
                response_well = requests.post(ws_well_url, json=payload_well, headers=headers)
                well_res_json = response_well.json()                
                # print(well_res_json)
                if 'id' in well_res_json:
                    ws_option_value_url = "http://13.212.250.28/en/api/watersupplywelloptionvalue/"
                    split_well_type_values = request.POST['well_type'].split(',')
                    print(split_well_type_values)
                    for well_type_value in split_well_type_values:
                        payload_well_option_value ={
                            "water_supply_well_id": well_res_json['id'],
                            "option_id": 1,
                            "value_id":int(well_type_value),
                            "is_active": True
                        }
                        response_well_option_value = requests.post(ws_option_value_url,json=payload_well_option_value, headers=headers).json()
                        print(payload_well_option_value)
            elif int(request.POST['water_supply_type']) == 2:
                ws_pipe_url = "http://13.212.250.28/en/api/watersupplypipe/"
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
                    "status_no_reason":request.POST["status_no_reason"],
                    "pipe_length": request.POST["pipe_length"],
                    "area_covering": request.POST["area_covering"]               
                }
                response_pipe_json = requests.post(ws_pipe_url, json=payload_pipe, headers=headers).json()
                # print(response_pipe_json)
                if 'id' in response_pipe_json:
                    ws_pipe_option_value_url = "http://13.212.250.28/en/api/watersupplypipoptionvalue/"
                    split_pipe_source_water_values = request.POST['source_type_of_water'].split(',')
                    for pipe_source_water in split_pipe_source_water_values:
                        payload_pipe_option_value = {
                            "water_supply_pipe_id": response_pipe_json['id'],
                            "option_id": 11,
                            "value_id": int(pipe_source_water),
                            "is_active": True
                        }
                        response_pipe_option_value = requests.post(ws_pipe_option_value_url,json=payload_pipe_option_value, headers=headers).json()
                        # print(response_pipe_option_value)
            elif int(request.POST['water_supply_type']) == 3:
                ws_kiosk_url = "http://13.212.250.28/en/api/watersupplykiosk/"
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
                
                if 'id' in response_kiosk_json:
                    #print(response_kiosk_json)
                    ws_kiosk_option_value_url = "http://13.212.250.28/en/api/watersupplykioskoptionvalue/"
                    #print(ws_kiosk_option_value_url)
                    split_kiosk_source_of_water_values = request.POST['source_type_of_water'].split(',')
                    #print(split_kiosk_source_of_water_values)
                    for kiosk_source_water in split_kiosk_source_of_water_values:
                        payload_kiosk_option_value = {
                            "water_supply_kiosk_id": response_kiosk_json['id'],
                            "option_id": 11,
                            "value_id": int(kiosk_source_water),
                            "is_active": True
                        }
                        #print(payload_kiosk_option_value)
                        response_kiosk_option_value = requests.post(ws_kiosk_option_value_url,json=payload_kiosk_option_value, headers=headers).json()

            elif int(request.POST['water_supply_type']) == 4:
                ws_community_pond_url = "http://13.212.250.28/en/api/watersupplycommunitypond/"
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
            elif int(request.POST['water_supply_type']) == 5:
                ws_rain_water_harvesting_url = "http://13.212.250.28/en/api/watersupplyrainwaterharvesting/"
                payload_rain_water_harvesting = {
                    "watersupply_id": res_json['data']['id'],
                    "is_active": True,
                    "type_of_using": request.POST["type_of_using"],
                    "capacity_35m3": 0,
                    "capacity_4m3": 0,
                    "capacity_of_rain_water_harvesting": request.POST["capacity_of_rain_water_harvesting"],
                    "status": request.POST["status"],
                    "status_no_reason": request.POST["status_no_reason"]  ,
                    "water_quality_checking" : request.POST.get("water_quality_checking")
                }
                response_rain_water_harvesting_json = requests.post(ws_rain_water_harvesting_url, json=payload_rain_water_harvesting, headers=headers).json()
            
            elif int(request.POST['water_supply_type']) == 6:
                ws_pipe_private_url = "http://13.212.250.28/en/api/watersupplypipeprivate/"
                payload_pipe_private = {
                    "watersupply_id" : res_json['data']['id'],
                    "is_active": True,
                    "source_type_of_water": request.POST["source_type_of_water"],
                    "abilty_of_produce_water":request.POST["abilty_of_produce_water"],
                    "underground_pool_storage": request.POST["underground_pool_storage"],
                    "pool_air": request.POST["pool_air"],
                    "pool_filter": request.POST["pool_filter"],
                    "number_of_link": request.POST["number_of_link"],
                    "water_quality_check": request.POST["well_water_quality_check"],
                    "status": request.POST["status"],
                    "status_no_reason":request.POST["well_status_reason"],
                    "pipe_length": request.POST["pipe_length"],
                    "area_covering": request.POST["area_covering"],
                    "is_has_license": request.POST["is_has_license"],
                    "license_registered_date": request.POST["license_registered_date"],
                    "license_expired_date": request.POST["license_expired_date"]
                }
                response_pipe_private_json = requests.post(ws_pipe_private_url, json=payload_pipe_private, headers=headers).json()
                # print(response_pipe_json)
                if 'id' in response_pipe_private_json:
                    ws_pipe_private_option_value_url = "http://13.212.250.28/en/api/watersupplypipeprivateoptionvalue/"
                    split_pipe_source_water_values = request.POST['source_type_of_water'].split(',')
                    for pipe_source_water in split_pipe_source_water_values:
                        payload_pipe_option_value = {
                            "water_supply_pipe_id": response_pipe_private_json['id'],
                            "option_id": 11,
                            "value_id": int(pipe_source_water),
                            "is_active": True
                        }
                        response_pipe_option_value = requests.post(ws_pipe_private_option_value_url,json=payload_pipe_option_value, headers=headers).json()
            elif int(request.POST['water_supply_type']) == 7:
                ws_air_water_url = "http://13.212.250.28/en/api/watersupplyairwater/"
                payload_air_water = {               
                    "watersupply_id": res_json['data']['id'],
                    "is_active": True,
                    "source_type_of_water": request.POST["source_type_of_water"],
                    "abilty_of_produce_water": request.POST["abilty_of_produce_water"],
                    "filter_system": request.POST["filter_system"],
                    "water_quality_checking": request.POST["well_water_quality_check"],
                    "status": request.POST["status"],
                    "status_no_reason": request.POST["status_no_reason"]                      
                }
                response_air_water_json = requests.post(ws_air_water_url, json=payload_air_water, headers=headers).json()
                
                if 'id' in response_air_water_json:
                    #print(response_kiosk_json)
                    ws_air_water_option_value_url = "http://13.212.250.28/en/api/watersupplyairwateroptionvalue/"
                    #print(ws_kiosk_option_value_url)
                    split_air_water_source_of_water_values = request.POST['source_type_of_water'].split(',')
                    #print(split_kiosk_source_of_water_values)
                    for air_water_source_water in split_air_water_source_of_water_values:
                        payload_air_water_option_value = {
                            "water_supply_airwater_id": response_air_water_json['id'],
                            "option_id": 11,
                            "value_id": int(air_water_source_water),
                            "is_active": True
                        }
                        print(payload_air_water_option_value)
                        response_air_water_option_value = requests.post(ws_air_water_option_value_url,json=payload_air_water_option_value, headers=headers).json()


            #if Water Quality Check
            wqc_param_url = "http://13.212.250.28/en/api/watersupplyqualitycheckparameter/"
            wqc_param_ids = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
       
            for param_id in wqc_param_ids:
                wqc_param_id = "wqcparam_" + str(param_id)
                wqc_param_value = request.POST.get(wqc_param_id)

                wqc_param_payload = {
                    "value": wqc_param_value,
                    "is_active": True,
                    "water_supply_id": res_json['data']['id'],
                    "water_quanlity_check_parameter_id": param_id
                }
                response_wqc_param = requests.post(wqc_param_url, json=wqc_param_payload, headers=headers).json()
                # print(wqc_param_value)

            return redirect('watersupply_detail', id=id)

    water_quality_check_parameter_url = MAIN_URL + "waterquanlitycheck/" 
    water_quality_check_parameters = requests.get(water_quality_check_parameter_url).json()

    return render(request, 'watersupply/edit.html', {
        'watersupply': watersupply, 
        'key':settings.GOOGLE_API_KEY,
        'watersupplytypeoptions':watersupplyoptins,
        'provinces': provinces,
        'water_quality_check_parameters' : water_quality_check_parameters
        })

def watersupply_myreqeust(request):
    # water_supply_my_request_url = MAIN_URL + "watersupplybyuser/?search="+str(request.session['user']['id'])
    # watersupplylist = requests.get(water_supply_my_request_url).json()
    return render(request, 'watersupply/myrequest.html')

def watersupply_myapproval(request):

    if request.session['user']['is_provincial_department_head']:
        my_approval_url = MAIN_URL+"watersupplybyprovince/?province_id="+ str(request.session['user']['provincial_department_head_province_id']) +"&main_status=1 "
        watersupplylist = requests.get(my_approval_url).json()
        # print(watersupplylist)
        return render(request, 'watersupply/myapproval.html',{'watersupplylist': watersupplylist})
    if request.session['user']['is_data_verifier_1']:
        my_approval_url = MAIN_URL+"watersupplybyprovince/?province_id=&main_status=2"
        watersupplylist = requests.get(my_approval_url).json()
        return render(request, 'watersupply/myapproval.html',{'watersupplylist': watersupplylist})
    if request.session['user']['is_data_verifier_2']:
        my_approval_url = MAIN_URL+"watersupplybyprovince/?province_id=&main_status=5"
        watersupplylist = requests.get(my_approval_url).json()
        return render(request, 'watersupply/myapproval.html',{'watersupplylist': watersupplylist})
    if request.session['user']['is_head_department']:
        #my_approval_url = MAIN_URL+"watersupplybyprovince/?province_id=&main_status=7"
        my_approval_url = MAIN_URL + "watersupplybyprovinceandmultiplestatus/?main_status=7%2C12&province_id="
        watersupplylist = requests.get(my_approval_url).json()
        return render(request, 'watersupply/myapproval.html',{'watersupplylist': watersupplylist})
    else:
        water_supply_url = MAIN_URL + 'watersupply/'
        watersupplylist = requests.get(water_supply_url).json()

    return render(request, 'watersupply/myapproval.html',{'watersupplylist': watersupplylist})

def watersupply_myapprovalhistory(request):
    myapproval_history_url = MAIN_URL + "watersupplyworkflow/?watersupply_id=&user_id="+str(request.session['user']['id'])
    watersupplylist = requests.get(myapproval_history_url).json()

    return render(request, 'watersupply/myapprovalhistory.html', {'watersupplylist': watersupplylist})

#START USER SECTION

def user_index(request):
    user_list_url = MAIN_URL + 'userlist/'
    users = requests.get(user_list_url).json()
    return render(request, 'users/index.html' , {'users': users})


def user_register(request):
    
    if request.method == "POST":
        
        url = "http://13.212.250.28/en/api/register/"
        is_data_entry = request.POST.get('is_data_entry', False)
        is_head_department= request.POST.get('is_head_department', False)
        is_provincial_department_head = request.POST.get('is_provincial_head_department', False)
        is_data_verifier_1= request.POST.get('is_data_verifier_1', False)
        is_data_verifier_2 = request.POST.get('is_data_verifier_2', False)
        is_partner= request.POST.get('is_partner', False)
        data_entry_province_id = request.POST.get('data_entry_province_id','')
        provincial_department_head_province_id = request.POST.get('provincial_department_head_province_id','')
 
        payload = {
            "username": request.POST["username"],
            "email": request.POST["email"],
            "password": request.POST["password"],
            "is_data_entry": bool(is_data_entry),
            "is_head_department": bool(is_head_department),
            "is_provincial_department_head": bool(is_provincial_department_head),
            "is_data_verifier_1": bool(is_data_verifier_1),
            "is_data_verifier_2": bool(is_data_verifier_2),
            "is_partner": bool(is_partner),
            "data_entry_province_id": data_entry_province_id,
            "provincial_department_head_province_id": provincial_department_head_province_id,
            "first_name" : request.POST["first_name"],
            "last_name" : request.POST["last_name"]
        }       
        print(payload)
        headers = {'Content-Type': 'application/json'}
        #response = requests.post(url1, json=payload, headers=headers)
        response = requests.post(url, json=payload, headers=headers).json()
        
        #print(response)
        
        return redirect("user_index")
        
    return render(request, 'users/register.html')

def user_main_account(request):

    action_type=0
    token = ''
    error_msg = []
    old_password_msgs = []
    password_msgs = []
    password2_msgs = []

    if request.method == "POST":
        token = request.session['token']
        user_id = request.session['user']['id']
        action_type = request.POST.get('action_type',0)
        old_password = request.POST.get('old_password',"")
        new_password = request.POST.get('new_password',"")
        new_password1 = request.POST.get('new_password1',"")

        reset_password_url = settings.API_ENDPOINT+ "change_password/"+str(user_id)+"/"
        print(reset_password_url)
        reset_password_payload = {
            
            "old_password":old_password,
            "password":new_password,
            "password2":new_password1
        }
        print(reset_password_payload)
        headers = {
            'Content-Type': 'application/json',
            'Authorization' : 'Token ' + token
            }
        response = requests.put(reset_password_url, json=reset_password_payload, headers=headers).json()
        if 'old_password' in response:
            #old_password_msgs = []
            if 'old_password' in response['old_password']:
                old_password_msgs.append(response['old_password']['old_password'])
            else:
                old_password_msgs.append(response['old_password'])
            
        if 'password' in response:
            #password_msgs = []
            password_msgs.append(response['password'])

        if 'password2' in response:
            #password2_msgs = []
            password2_msgs.append(response['password2'])

        error_msg.append(old_password_msgs)
        error_msg.append(password_msgs)
        error_msg.append(password2_msgs)

        #print(error_msg)

        return render(request, 'users/main_account.html',{ 
            'action_type':action_type,
            'token':token, 
            'response' : response, 
            'error_msg':error_msg,
            'old_password_msgs' : old_password_msgs,
            'password_msgs' : password_msgs,
            'password2_msgs' : password2_msgs
            })
        # print(response)

    return render(request, 'users/main_account.html',{ 'action_type':action_type,'token':token })

#END USER SECTION

def qr_gen(request):
    if request.method == "POST":
        data = request.POST['data']
        img = make(data)
        img_name = 'qr' + str(time.time()) + '.png'
        img.save(settings.MEDIA_ROOT + '/' + img_name)
        return render(request, 'watersupply/qrcode.html', {'img_name': img_name})
    return render(request, 'watersupply/qrcode.html')

def report_water_supply_map(request):

    return render(request, 'report/water_supply_map.html', { 'key':settings.GOOGLE_API_KEY})

#START REPORT SECITON 
def report_well_by_province(request):
    if request.session['user']['is_data_entry']:
        province_url = MAIN_URL + 'province/?id=' + str(request.session['user']['data_entry_province_id'])
        #print(request.user.data_entry_province_id.id)
    else:
        province_url = MAIN_URL + 'province'
    provinces = requests.get(province_url).json()
    return render(request, 'report/report_well_by_project.html', { "provinces": provinces })

def report_well_by_province_token(request, token):
    province_url = MAIN_URL + 'province'
    provinces = requests.get(province_url).json()
    return render(request, 'report/report_well_by_project.html', { "provinces": provinces })

def report_water_supply_coverage(request):
    url = MAIN_URL + 'watersupplytype/'
    watersupplytypelist = requests.get(url).json()

    if request.session['user']['is_data_entry']:
        province_url = MAIN_URL + 'province/?id=' + str(request.session['user']['data_entry_province_id'])
        #print(request.user.data_entry_province_id.id)
    else:
        province_url = MAIN_URL + 'province'
    provinces = requests.get(province_url).json()
    
    return render(request, "report/report_water_supply_coverage.html", { 
        "watersupplytypelist": watersupplytypelist ,
        "provinces" : provinces
        });

def report_water_supply_coverage_token(request, token):
    url = MAIN_URL + 'watersupplytype/'
    watersupplytypelist = requests.get(url).json()
    province_url = MAIN_URL + 'province'       
    provinces = requests.get(province_url).json()
    
    return render(request, "report/report_water_supply_coverage.html", { 
        "watersupplytypelist": watersupplytypelist ,
        "provinces" : provinces
        });


#END REPORT SECTION

def import_rural_water_supply(request):

    if request.method == 'POST' and request.FILES['myfile']:   
        try:   
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            
            
            #filename = fs.save(myfile.name, myfile)
            filename = fs.save(settings.MEDIA_ROOT + '/' + str(time.time())+ '_' + myfile.name, myfile )
            #print(filename)
            uploaded_file_url = fs.url(filename)  
            
            #GET EVERY SHEET            
            # excel_sheets = pd.read_excel(settings.MEDIA_ROOT + '/' + filename, None) 
            # sheet_number = 0   
            # for sheet in excel_sheets.keys():
                
            #     empexceldata = pd.read_excel(settings.MEDIA_ROOT + '/' + filename, sheet_name=sheet_number)  
            
            #     dbframe = empexceldata
            #     PriceList = []
            #     for dbframe in dbframe.itertuples():
            #         PriceList.append(dbframe)
                    
            #     sheet_number = sheet_number + 1
            
            #url1 = "http://13.212.250.28/en/api/v2/watersupply"
            url1 = settings.API_ENDPOINT + 'v2/watersupply'

            #GET ONLY FIRST SHEET ## WELL
            PriceList = []
            SucessImported = []
            ErrorImported = []
            VillageErrorImported = []
            empexceldata = pd.read_excel(settings.MEDIA_ROOT + '/' + filename) 
            dbframe = empexceldata 
            counter = 0

            for dbframe in dbframe.itertuples():
                PriceList.append(dbframe)
                # Submit data to Database
                if counter > 10 :
                    #url1 = "http://13.212.250.28/en/api/v2/watersupply"
                    url1 = settings.API_ENDPOINT + 'v2/watersupply'

                    if pd.isnull(dbframe[1]) == False and pd.isnull(dbframe[2]) == False:
                        
                        total_family = 0
                        beneficiary_total_people = 0 #28
                        beneficiary_total_women = 0 #29
                        beneficiary_total_family = 0 #30
                        beneficiary_total_family_poor_1 = 0 #31
                        beneficiary_total_family_poor_2 = 0 #32
                        beneficiary_total_family_vulnerable = 0 #33
                        beneficiary_total_family_indigenous = 0 #34

                        water_supply_code = ''
                        construction_date = '2023-01-01'
                        is_water_supply_code_exist= False

                        if dbframe[7] == '' or pd.isnull(dbframe[7]):
                            water_supply_code = ''
                        else:
                            water_supply_code = dbframe[7]

                            check_exist_watersupply_url = MAIN_URL + 'watersupplycheckisexist/' + str(water_supply_code) + '/'
                            result_exist = requests.get(check_exist_watersupply_url).json()
                            if 'is_exist' in result_exist:
                                if result_exist['is_exist'] == True:
                                    is_water_supply_code_exist = True
                        
                        if is_water_supply_code_exist == False:

                            province_id=''
                            if pd.isnull(dbframe[2]) == False:
                                province_filter_url = MAIN_URL + 'provincefilterbyname/?search=' + dbframe[2]                
                                provinces = requests.get(province_filter_url).json()
                                if len(provinces) > 0 :
                                    province_id = provinces[0]['id']
                            
                            district_id = ''
                            if pd.isnull(dbframe[3]) == False:
                                district_filter_url = MAIN_URL + 'districtfilterbyname/?search=' + dbframe[3]
                                districts = requests.get(district_filter_url).json()
                                for district in districts:
                                    if district['province_id'] == province_id:
                                        district_id = district['id']
                                # if len(districts) > 0:
                                #     district_id = districts[0]['id']
                            
                            commune_id = ''
                            if pd.isnull(dbframe[4]) == False:
                                commune_filter_url = MAIN_URL + 'communefilterbyname/?search=' + dbframe[4]
                                communes = requests.get(commune_filter_url).json()
                                for commune in communes:
                                    if commune['district_id'] == district_id:
                                        commune_id = commune['id']
                                # if len(communes) > 0:
                                #     commune_id = communes[0]['id']
                            
                            village_id = ''
                            if pd.isnull(dbframe[5]) == False:
                                village_filter_url = MAIN_URL + 'villagefilterbyname/?search=' + dbframe[5]
                                villages = requests.get(village_filter_url).json()
                                if len(villages) == 0:
                                    #dbframe[34] = "Village not available in the system."
                                    ErrorImported.append(dbframe)
                                else:
                                    for village in villages:
                                        if village['commune_id'] == commune_id:
                                            village_id = village['id']                            
                            

                            if dbframe[6] == '' or pd.isnull(dbframe[6]):
                                total_family =0 
                            elif dbframe[6] == '–' :
                                total_family = 0
                            else:
                                total_family = float(dbframe[6])

                            map_unit_id = 1
                            utm_x = 0
                            utm_y = 0
                            coor_x = 0
                            coor_y = 0
                            if pd.isnull(dbframe[8]) == False:
                                split_coor_x = str(dbframe[8]).split(' ')
                                if len(split_coor_x) == 1: #UTM
                                    utm_x =dbframe[8]
                                elif len(split_coor_x) == 2: # decimal degree
                                    map_unit_id = 2
                                    coor_x = split_coor_x[0][:-1] + '.'+split_coor_x[1]
                            
                            if pd.isnull(dbframe[9]) == False:
                                split_coor_y = str(dbframe[9]).split(' ')
                                if len(split_coor_y) == 1:
                                    utm_y = dbframe[9]
                                elif len(split_coor_y) == 2:
                                    coor_y = split_coor_y[0][:-1] + '.' + split_coor_y[1]

                            if pd.isnull(dbframe[28]) == False:
                                if dbframe[28] == '–':
                                    beneficiary_total_people= 0
                                else:                           
                                    beneficiary_total_people = float(dbframe[28])
                            if pd.isnull(dbframe[29]) == False:
                                if dbframe[29] == '–':
                                    beneficiary_total_women = 0
                                else:
                                    beneficiary_total_women = float(dbframe[29])
                            if pd.isnull(dbframe[30]) == False :
                                if dbframe[30] == '–':
                                    beneficiary_total_family = 0
                                else:
                                    beneficiary_total_family = float(dbframe[30])
                            if pd.isnull(dbframe[31]) == False:
                                if dbframe[31] == '–':
                                    beneficiary_total_family_poor_1 = 0
                                else:
                                    beneficiary_total_family_poor_1 = float(dbframe[31])
                            if pd.isnull(dbframe[32]) == False:
                                if dbframe[32] == '–':
                                    beneficiary_total_family_poor_2 = 0
                                else:
                                    beneficiary_total_family_poor_2 = float(dbframe[32])
                            if pd.isnull(dbframe[33]) == False:
                                if isNum(dbframe[33]) == False:
                                    beneficiary_total_family_vulnerable = 0
                                else:
                                    beneficiary_total_family_vulnerable = float(dbframe[33])
                            if pd.isnull(dbframe[34]) == False:
                                if dbframe[34] == '–':
                                    beneficiary_total_family_indigenous = 0
                                else:
                                    beneficiary_total_family_indigenous = float(dbframe[34])


                            if pd.isnull(dbframe[10]) == False:

                                construction_date =pd.to_datetime(dbframe[10]).strftime("%Y-%m-%d")
                            
                                print(construction_date)

                            source_budget = 0
                            if pd.isnull(dbframe[11]) == False: #Source Budget
                                split_source_budget = dbframe[11].split('.')
                                source_budget = int(split_source_budget[0])                       
                            
                            construction_by = ''
                            if pd.isnull(dbframe[13]) == False:
                                construction_by = dbframe[13]
                            management_type = 0
                            if pd.isnull(dbframe[14]) == False:
                                split_management_type = dbframe[14].split('.')
                                if isNum(split_management_type[0]):
                                    management_type = int(split_management_type[0])
                            managed_by = ''
                            if pd.isnull(dbframe[15]) == False:
                                managed_by = dbframe[15]

                            is_risk_enviroment = False
                            if pd.isnull(dbframe[25]) == False:
                                split_risk_enviroment = dbframe[25].split('.')
                                if len(split_risk_enviroment) > 0:
                                    if isNum(split_risk_enviroment[0]):
                                        num_risk_enviroment = int(split_risk_enviroment[0])
                                        if num_risk_enviroment == 0:
                                            is_risk_enviroment = True

                            #print(total_family)

                            #specific fields of Well 
                            well_type_id = 0
                            if pd.isnull(dbframe[16]) == False:
                                split_well_type = dbframe[16].split('.')
                                if len(split_well_type) > 0:
                                    if isNum(split_well_type[0]):
                                        well_type_id = int(split_well_type[0])
                                else:
                                    split_well_type = dbframe[16].split(':')
                                    if len(split_well_type) > 0:
                                        if isNum(split_well_type[0]):
                                            well_type_id = int(split_well_type[0])
                                well_type_id = well_type_id + 1
                            
                            well_height = 0
                            if pd.isnull(dbframe[17]) == False:
                                if isNum(dbframe[17]):
                                    well_height = float(dbframe[17])
                            well_filter_height = 0 
                            if pd.isnull(dbframe[18]) == False:
                                if isNum(dbframe[17]):
                                    well_filter_height = float(dbframe[18])
                            well_water_supply = 0
                            if pd.isnull(dbframe[19]) == False:
                                if isNum(dbframe[19]):
                                    well_water_supply = float(dbframe[19])
                            well_nirostatic = 0
                            if pd.isnull(dbframe[20]) == False:
                                if isNum(dbframe[20]):
                                    well_nirostatic = float(dbframe[20])
                            well_nirodynamic = 0
                            if pd.isnull(dbframe[21]) == False:
                                if isNum(dbframe[21]):
                                    well_nirodynamic = float(dbframe[21])
                            well_watar_quality = 9
                            if pd.isnull(dbframe[24]) == False:
                                split_well_water_quality = dbframe[24].split(':')
                                if len(split_well_water_quality) > 0:
                                    if isNum(split_well_water_quality[0]):
                                        well_water_quality_value = int(split_well_water_quality[0])
                                        if well_water_quality_value == 0:
                                            well_watar_quality = 8
                                        else:
                                            well_watar_quality = 9

                            
                            #print(well_watar_quality)
                            well_water_quality_check = 0
                            if pd.isnull(dbframe[22]) == False:
                                split_water_quality_check = dbframe[22].split(':')
                                if len(split_water_quality_check) > 0:
                                    if isNum(split_water_quality_check[0]):
                                        well_water_quality_check_value = int(split_water_quality_check[0])
                                        if well_water_quality_check_value == 0:
                                            well_water_quality_check= 10
                                        else:
                                            well_water_quality_check = 11

                            well_status = 0
                            if pd.isnull(dbframe[26]) == False:
                                split_well_status = dbframe[26].split(':')
                                if len(split_well_status) > 0:
                                    if isNum(split_well_status[0]):
                                        well_status_value = int(split_well_status[0])
                                        if well_status_value == 0:
                                            well_status = 12
                                        else:
                                            well_status = 13
                            well_status_reason = 0
                            if pd.isnull(dbframe[27]) == False:
                                well_status_reason = dbframe[27]


                            payload = {
                                "water_supply_type_id": 1,
                                "province_id": province_id,
                                "district_id": district_id,
                                "created_by":  request.session['user']['id'],
                                "updated_by":  request.session['user']['id'],#
                                "is_active": True,
                                "is_risk_enviroment_area": is_risk_enviroment,
                                "commune_id": commune_id,
                                "village_id": village_id,
                                "construction_date": construction_date,
                                "water_supply_code" : water_supply_code,
                                "total_family" : total_family,
                                "utm_x": utm_x,
                                "utm_y": utm_y,
                                "source_budget": source_budget,
                                "constructed_by":construction_by,
                                "management_type":management_type,
                                "managed_by":managed_by,
                                "beneficiary_total_people": beneficiary_total_people,
                                "beneficiary_total_women": beneficiary_total_women,
                                "beneficiary_total_family": beneficiary_total_family,
                                "beneficiary_total_family_poor_1": beneficiary_total_family_poor_1,
                                "beneficiary_total_family_poor_2": beneficiary_total_family_poor_2,
                                "beneficiary_total_family_vulnerable": beneficiary_total_family_vulnerable,
                                "beneficiary_total_family_indigenous": beneficiary_total_family_indigenous,
                                "main_status":9,
                                "is_water_quality_check": False,
                                "map_unit" : map_unit_id,
                                "decimal_degress_lat" :coor_x,
                                "decimal_degress_lng" : coor_y,
                                "mds_x_degress" : 0,
                                "mds_x_minute" : 0,
                                "mds_x_second" : 0,
                                "mds_y_degress" : 0,
                                "mds_y_minute" : 0,
                                "mds_y_second" : 0
                            }

                            #print(payload)
                            if village_id == '':
                                VillageErrorImported.append(dbframe)
                                #ErrorImported.append(dbframe)
                            else :
                            
                                headers = {'Content-Type': 'application/json'}
                                #response = requests.post(url1, json=payload, headers=headers)

                                response = requests.post(url1, json=payload, headers=headers)
                                res_json  = response.json()
                                print(res_json)
                                
                                if 'status' in res_json:
                                    SucessImported.append(dbframe)
                                    #water supply workflow
                                    #ws_workflow = "http://13.212.250.28/en/api/v2/watersupplyworkflow"
                                    ws_workflow = settings.API_ENDPOINT + "v2/watersupplyworkflow"
                                    payload_wsworkflow = {
                                        "watersupply_id": res_json['data']['id'],
                                        "status_id": 9,
                                        "user_id": request.session['user']['id'],
                                        "remark": ""
                                    }
                                    response_ws_workflow = requests.post(ws_workflow, json=payload_wsworkflow, headers=headers).json()
                                    #WELL Specific Fields 
                                    #ws_well_url = "http://13.212.250.28/en/api/watersupplywell/"
                                    ws_well_url = settings.API_ENDPOINT + "watersupplywell/"
                                    payload_well = {
                                        "watersupply_id" : res_json['data']['id'],
                                        "well_type" : well_type_id,
                                        "well_height": well_height,
                                        "well_filter_height" : well_filter_height,
                                        "well_water_supply" : well_water_supply,
                                        "well_nirostatic": well_nirostatic,
                                        "well_watar_quality": well_watar_quality,
                                        "well_water_quality_check" : well_water_quality_check,
                                        "well_status": well_status,
                                        "well_status_reason":well_status_reason,
                                        "well_nirodynamic": well_nirodynamic,
                                        "is_active": True,
                                    }
                                    response_well = requests.post(ws_well_url, json=payload_well, headers=headers)
                                    well_res_json = response_well.json()                
                                    # print(well_res_json)
                                    if 'id' in well_res_json:
                                        #ws_option_value_url = "http://13.212.250.28/en/api/watersupplywelloptionvalue/"
                                        ws_option_value_url = settings.API_ENDPOINT + "watersupplywelloptionvalue/"

                                        payload_well_option_value ={
                                            "water_supply_well_id": well_res_json['id'],
                                            "option_id": 1,
                                            "value_id":int(well_type_id),
                                            "is_active": True
                                        }
                                        response_well_option_value = requests.post(ws_option_value_url,json=payload_well_option_value, headers=headers).json()
                                #         #print(payload_well_option_value)
                                    
                counter = counter + 1   
                    

            #Small PIPE 
            # small_pipe_excel_data = pd.read_excel(settings.MEDIA_ROOT + '/' + filename,sheet_name=1)
            # dbframe = small_pipe_excel_data
            # counter_small_pipe = 0
            # for dbframe in dbframe.itertuples():
            #     PriceList.append(dbframe)
            #     if counter_small_pipe > 6:
            #         if pd.isnull(dbframe[1]) == False:
                        
            #             total_family = 0 #6
            #             beneficiary_total_people = 0 #28
            #             beneficiary_total_women = 0 #29
            #             beneficiary_total_family = 0 #30
            #             beneficiary_total_family_poor_1 = 0 #31
            #             beneficiary_total_family_poor_2 = 0 #32
            #             beneficiary_total_family_vulnerable = 0 #33
            #             beneficiary_total_family_indigenous = 0 #34

            #             water_supply_code = ''
            #             construction_date = '2023-01-01'
            #             is_water_supply_code_exist= False

            #             if pd.isnull(dbframe[7]) == False:
            #                 if dbframe[7] == '–':
            #                     water_supply_code = ''
            #                 else:
            #                     water_supply_code = dbframe[7]
                            
            #                     check_exist_watersupply_url = MAIN_URL + 'watersupplycheckisexist/' + str(water_supply_code) + '/'
            #                     result_exist = requests.get(check_exist_watersupply_url).json()
            #                     if 'is_exist' in result_exist:
            #                         if result_exist['is_exist'] == True:
            #                             is_water_supply_code_exist = True
                        
            #             if is_water_supply_code_exist == False:

            #                 province_id=''
            #                 if pd.isnull(dbframe[2]) == False:
            #                     province_filter_url = MAIN_URL + 'provincefilterbyname/?search=' + dbframe[2]                
            #                     provinces = requests.get(province_filter_url).json()
            #                     if len(provinces) > 0 :
            #                         province_id = provinces[0]['id']
                            
            #                 district_id = ''
            #                 if pd.isnull(dbframe[3]) == False:
            #                     district_filter_url = MAIN_URL + 'districtfilterbyname/?search=' + dbframe[3]
            #                     districts = requests.get(district_filter_url).json()
            #                     for district in districts:
            #                         if district['province_id'] == province_id:
            #                             district_id = district['id']
            #                     # if len(districts) > 0:
            #                     #     district_id = districts[0]['id']
                            
            #                 commune_id = ''
            #                 if pd.isnull(dbframe[4]) == False:
            #                     commune_filter_url = MAIN_URL + 'communefilterbyname/?search=' + dbframe[4]
            #                     communes = requests.get(commune_filter_url).json()
            #                     for commune in communes:
            #                         if commune['district_id'] == district_id:
            #                             commune_id = commune['id']
            #                     # if len(communes) > 0:
            #                     #     commune_id = communes[0]['id']
                            
            #                 village_id = ''
            #                 if pd.isnull(dbframe[5]) == False:
            #                     village_filter_url = MAIN_URL + 'villagefilterbyname/?search=' + dbframe[4]
            #                     villages = requests.get(village_filter_url).json()

            #                     for village in villages:
            #                         if village['commune_id'] == commune_id:
            #                             village_id = village['id']

            #                     # if len(villages) > 0:
            #                     #     village_id = villages[0]['id']

                            
                            

            #                 if pd.isnull(dbframe[6]) == False :
            #                     if dbframe[6] == '–':
            #                         total_family = 0
            #                     else:
            #                         total_family = float(dbframe[6])                           
                                
            #                 map_unit_id = 1
            #                 utm_x = 0
            #                 utm_y = 0
            #                 coor_x = 0
            #                 coor_y = 0
            #                 if pd.isnull(dbframe[8]) == False:
            #                     if dbframe[8] == '–':
            #                         utm_x = 0
            #                         coor_x = 0
            #                     else:
            #                         split_coor_x =str(dbframe[8]).split(' ')
            #                         if len(split_coor_x) == 1: #UTM
            #                             utm_x = dbframe[8]
            #                         elif len(split_coor_x) == 2: # decimal degree
            #                             map_unit_id = 2
            #                             coor_x = split_coor_x[0][:-1] + '.'+split_coor_x[1]
                            
            #                 if pd.isnull(dbframe[9]) == False:
            #                     if dbframe[9] == '–':
            #                         utm_y = 0
            #                         coor_y = 0
            #                     else:
            #                         split_coor_y = str(dbframe[9]).split(' ')
            #                         if len(split_coor_y) == 1:
            #                             utm_y = dbframe[9]
            #                         elif len(split_coor_y) == 2:
            #                             coor_y = split_coor_y[0][:-1] + '.' + split_coor_y[1]

            #                 if pd.isnull(dbframe[30]) == False:
            #                     if dbframe[30] == '–':
            #                         beneficiary_total_people= 0
            #                     else:                           
            #                         beneficiary_total_people = float(dbframe[30])
            #                 if pd.isnull(dbframe[31]) == False:
            #                     if dbframe[31] == '–':
            #                         beneficiary_total_women = 0
            #                     else:
            #                         beneficiary_total_women = float(dbframe[31])
            #                 if pd.isnull(dbframe[32]) == False :
            #                     if dbframe[32] == '–':
            #                         beneficiary_total_family = 0
            #                     else:
            #                         beneficiary_total_family = float(dbframe[32])
            #                 if pd.isnull(dbframe[33]) == False:
            #                     if dbframe[33] == '–':
            #                         beneficiary_total_family_poor_1 = 0
            #                     else:
            #                         beneficiary_total_family_poor_1 = float(dbframe[33])
            #                 if pd.isnull(dbframe[34]) == False:
            #                     if dbframe[34] == '–':
            #                         beneficiary_total_family_poor_2 = 0
            #                     else:
            #                         beneficiary_total_family_poor_2 = float(dbframe[34])
            #                 if pd.isnull(dbframe[35]) == False:
            #                     if isNum(dbframe[35]) == False:
            #                         beneficiary_total_family_vulnerable = 0
            #                     else:
            #                         beneficiary_total_family_vulnerable = float(dbframe[35])
            #                 if pd.isnull(dbframe[36]) == False:
            #                     if dbframe[36] == '–':
            #                         beneficiary_total_family_indigenous = 0
            #                     else:
            #                         beneficiary_total_family_indigenous = float(dbframe[36])


            #                 # if pd.isnull(dbframe[10]) == False:
            #                 #     construction_date = dbframe[10].strftime("%Y-%m-%d")
                            
            #                     #print(construction_date)

            #                 source_budget = 0
            #                 if pd.isnull(dbframe[11]) == False: #Source Budget
            #                     split_source_budget = dbframe[11].split('.')
            #                     source_budget = int(split_source_budget[0])                       
                            
            #                 construction_by = ''
            #                 if pd.isnull(dbframe[13]) == False:
            #                     construction_by = dbframe[13]
            #                 management_type = 0
            #                 if pd.isnull(dbframe[14]) == False:
            #                     split_management_type = dbframe[14].split('.')
            #                     if isNum(split_management_type[0]):
            #                         management_type = int(split_management_type[0])
            #                 managed_by = ''
            #                 if pd.isnull(dbframe[15]) == False:
            #                     managed_by = dbframe[15]

            #                 is_risk_enviroment = False
            #                 if pd.isnull(dbframe[27]) == False:
            #                     split_risk_enviroment = dbframe[27].split('.')
            #                     if len(split_risk_enviroment) > 0:
            #                         if isNum(split_risk_enviroment[0]):
            #                             num_risk_enviroment = int(split_risk_enviroment[0])
            #                             if num_risk_enviroment == 0:
            #                                 is_risk_enviroment = True

            #                 payload = {
            #                     "water_supply_type_id": 2,
            #                     "province_id": province_id,
            #                     "district_id": district_id,
            #                     "created_by":  request.session['user']['id'],
            #                     "updated_by":  request.session['user']['id'],#
            #                     "is_active": True,
            #                     "is_risk_enviroment_area": is_risk_enviroment,
            #                     "commune_id": commune_id,
            #                     "village_id": village_id,
            #                     "construction_date": construction_date,
            #                     "water_supply_code" : water_supply_code,
            #                     "total_family" : total_family,
            #                     "utm_x": utm_x,
            #                     "utm_y": utm_y,
            #                     "source_budget": source_budget,
            #                     "constructed_by":construction_by,
            #                     "management_type":management_type,
            #                     "managed_by":managed_by,
            #                     "beneficiary_total_people": beneficiary_total_people,
            #                     "beneficiary_total_women": beneficiary_total_women,
            #                     "beneficiary_total_family": beneficiary_total_family,
            #                     "beneficiary_total_family_poor_1": beneficiary_total_family_poor_1,
            #                     "beneficiary_total_family_poor_2": beneficiary_total_family_poor_2,
            #                     "beneficiary_total_family_vulnerable": beneficiary_total_family_vulnerable,
            #                     "beneficiary_total_family_indigenous": beneficiary_total_family_indigenous,
            #                     "main_status":9,
            #                     "is_water_quality_check": False,
            #                     "map_unit" : map_unit_id,
            #                     "decimal_degress_lat" :coor_x,
            #                     "decimal_degress_lng" : coor_y,
            #                     "mds_x_degress" : 0,
            #                     "mds_x_minute" : 0,
            #                     "mds_x_second" : 0,
            #                     "mds_y_degress" : 0,
            #                     "mds_y_minute" : 0,
            #                     "mds_y_second" : 0
            #                 }

            #                 #print(payload)
            #                 headers = {'Content-Type': 'application/json'}
            #                 #response = requests.post(url1, json=payload, headers=headers)

            #                 response = requests.post(url1, json=payload, headers=headers)
            #                 res_json  = response.json()
            #                 print(res_json)
                            
            #                 if 'status' in res_json:
            #                     SucessImported.append(dbframe)
            #                     #water supply workflow
            #                     ws_workflow = "http://13.212.250.28/en/api/v2/watersupplyworkflow"
            #                     payload_wsworkflow = {
            #                         "watersupply_id": res_json['data']['id'],
            #                         "status_id": 9,
            #                         "user_id": request.session['user']['id'],
            #                         "remark": "Excel Imported"
            #                     }
            #                     response_ws_workflow = requests.post(ws_workflow, json=payload_wsworkflow, headers=headers).json()

            #     counter_small_pipe = counter_small_pipe + 1

        except Exception as e:
            #dbframe[35] =
            #ErrorImported.append(dbframe)
            raise e


        return render(request, 'import/import_rural_water_supply.html', {
            'empexceldata': PriceList,
            'successimported' : SucessImported,
            'errorimported' : ErrorImported,
            'villageerrorimported' : VillageErrorImported
        })   

    return render(request,'import/import_rural_water_supply.html')

def isNum(data):
    try:
        int(data)
        return True
    except ValueError:
        return False