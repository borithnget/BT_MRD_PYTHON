from pickle import NONE
from urllib import request
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests
from django.conf import settings
# Create your views here.

MAIN_URL = 'http://52.14.59.145/api/' 
#MAIN_URL = 'http://127.0.0.1:8000/en/api/'

def get_province_list(request):
    if request.method == "GET":
        province_api_url = settings.API_ENDPOINT + "province/"
        provinces = requests.get(province_api_url).json()
        return JsonResponse({"provinces":provinces}, status=200)
    return JsonResponse({}, status = 400)

def district(request):
    if request.method == "GET":
        province_id = request.GET.get('province_id', NONE)
        district_url = settings.API_ENDPOINT + 'district/?search=' + str(province_id)
        districts = requests.get(district_url).json()
        return JsonResponse({"district" : districts}, status=200)
    return JsonResponse({}, status = 400)

def get_commnue_list(request):
    if request.method == "GET":
        district_id = request.GET.get('district_id', NONE)
        commune_url = settings.API_ENDPOINT + 'commune/?search=' + str(district_id)
        commnues = requests.get(commune_url).json()
        return JsonResponse({'communes': commnues}, status = 200)
    return JsonResponse({}, status = 400)

def get_village_list(request):
    if request.method == "GET":
        commune_id = request.GET.get('commune_id', NONE)
        village_url = settings.API_ENDPOINT + 'village/?search=' + str(commune_id)
        villages = requests.get(village_url).json()
        return JsonResponse({'villages':villages}, status=200)
    return JsonResponse({}, status=400)

def get_watersupply_list(request):
    if request.method == "GET":
        water_supply_url = settings.API_ENDPOINT + 'watersupply/?water_supply_type_id=&main_status=9'
        print(water_supply_url)
        watersupplylist = requests.get(water_supply_url).json()
        return JsonResponse({'data':watersupplylist}, status=200)
    return JsonResponse({}, status = 400)

def get_myrequest_draft_list(request):
    if request.method == "GET":
        user_id = request.session['user']['id']
        if request.session['user']['is_data_entry']:
            url = settings.API_ENDPOINT + 'watersupplybyuserandstatus/?created_by='+ str(user_id) +'&main_status=3'
        else: 
            url = settings.API_ENDPOINT + 'watersupplybyuserandstatus/?created_by='+ str(user_id) +'&main_status=12'
        list= requests.get(url).json()
        return JsonResponse({'data':list}, status=200)
    return JsonResponse({}, status = 400)

def get_myrequest_history_list(request):
    if request.method == "GET":     
        #user_id = request.session['user']['id']
        user_id = request.session['user']['id']
        url = settings.API_ENDPOINT + "watersupplybyuser/?search="+str(user_id)
        list= requests.get(url).json()
        return JsonResponse({'data':list}, status=200)
    return JsonResponse({}, status=400)

def get_phd_requested_history(request):
    if request.method == "GET":
        user_id = request.session['user']['id']
        url = settings.API_ENDPOINT + "watersupplyworkflow/?watersupply_id=&user_id="+str(user_id)+"&status_id=12"
        list= requests.get(url).json()
        
        return JsonResponse({'data':list}, status=200)
    return JsonResponse({}, status = 400)

def get_water_supply_report_map(request):
    if request.method == "GET":
        headers = {'Content-Type': 'application/json'}
        water_supply_id = request.GET.get('water_supply_id', NONE)
        url = settings.API_ENDPOINT + "watersupplyreportmap/?water_supply_type_id="+ str(water_supply_id)
        list = requests.get(url).json()
        return JsonResponse({'data': list}, status=200)
    return JsonResponse({}, status=400)

def report_supply_well_by_province(request):
    if request.method == "GET":
        date_start = request.GET.get('date_start', NONE)
        date_end = request.GET.get('date_end', NONE)
        province = request.GET.get('province', '')
        url = settings.API_ENDPOINT + "watersupplyfilterdaterange?created_at="+str(date_start)+"&crated_at_1="+str(date_end)+"&province_id="+province
        # print(url)
        list = requests.get(url).json()
        return JsonResponse({'data': list}, status=200)
    return JsonResponse({}, status=400) 

def get_beneficiary_total_people(request):
    if request.method == "GET":
        ws_type = request.GET.get('ws_type', 0)
        province_id = request.GET.get('province_id', 0)
        url = settings.API_ENDPOINT + "watersupplybeneficiarytotalpeople/"+str(ws_type)+"/"+str(province_id)+"/"
        #print(url)
        list = requests.get(url).json()
        
        province_url = settings.API_ENDPOINT + "province/" + str(province_id)
        province = requests.get(province_url).json()

        return JsonResponse({'data': list, 'province':province}, status=200)

    return JsonResponse({}, status=400) 

#START POST SECTION
def post_approval_watersupply_by_provicial_head_department(request):
    if request.method == "GET":
        headers = {'Content-Type': 'application/json'}
        water_supply_id = request.GET.get('water_supply_id', NONE)
        status_id = request.GET.get('status_id',NONE)
        remark = request.GET.get('remark',NONE)

        #print(water_supply_id + " " + status_id)
        ws_workflow = "http://52.14.59.145/en/api/v2/watersupplyworkflow"
        payload_wsworkflow = {
            "watersupply_id": water_supply_id,
            "status_id":int(status_id),
            "user_id": int(request.session['user']['id']),
            "remark": remark
        }
        #print(payload_wsworkflow)
        response_ws_workflow = requests.post(ws_workflow, json=payload_wsworkflow, headers=headers).json()

        #Update Water Supply MainStatus
        ws_update_url = "http://52.14.59.145/en/api/watersupply/"+ str (water_supply_id) +"/update/"
        ws_update_payload = {
            "id": water_supply_id,
            "main_status": status_id
        }
        response_ws_upate_mainstatus = requests.put(ws_update_url, json=ws_update_payload, headers=headers).json()
        #print(response_ws_upate_mainstatus)

        return JsonResponse({'is_success':True},status=200)
    return JsonResponse({}, status=400)

def put_water_supply_delete(request):
    if request.method == "GET":
        headers = {'Content-Type': 'application/json'}
        water_supply_id = request.GET.get('water_supply_id', NONE)

        ws_delete_url = "http://52.14.59.145/en/api/v2/watersupply/" + str(water_supply_id) + "/delete/"
        ws_delete_payload = {
            "id": water_supply_id,
            "updated_by": int(request.session['user']['id']),
            "is_active": False
        }
        response_delete_ws = requests.put(ws_delete_url, json=ws_delete_payload, headers=headers).json()
        return JsonResponse({'is_success':True},status=200)
    return JsonResponse({}, status=400)

#END POST SECTION

