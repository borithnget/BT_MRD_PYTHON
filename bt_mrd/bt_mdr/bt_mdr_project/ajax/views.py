from pickle import NONE
from urllib import request
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests
from django.conf import settings
# Create your views here.
from datetime import datetime

MAIN_URL = 'http://3.0.166.20/api/' 
#MAIN_URL = 'http://127.0.0.1:8000/en/api/'

def get_country_km(request):
    if request.method == "GET":
        country_url = settings.API_ENDPOINT + "country/1/"     # settings.API_ENDPOINT +  
        country = requests.get(country_url).json()
        return JsonResponse({"country":country}, status=200)
    return JsonResponse({}, status = 400)

def get_province_list(request):
    if request.method == "GET":
        province_api_url = settings.API_ENDPOINT + "province/"
        provinces = requests.get(province_api_url).json()
        return JsonResponse({"provinces":provinces}, status=200)
    return JsonResponse({}, status = 400)

def district(request):
    if request.method == "GET":
        province_id = request.GET.get('province_id', NONE)
        district_url = settings.API_ENDPOINT + 'district/?province_id__id=' + str(province_id)
        districts = requests.get(district_url).json()
        return JsonResponse({"district" : districts}, status=200)
    return JsonResponse({}, status = 400)

def get_commnue_list(request):
    if request.method == "GET":
        district_id = request.GET.get('district_id', NONE)
        commune_url = settings.API_ENDPOINT + 'commune/?district_id__id=' + str(district_id)
        commnues = requests.get(commune_url).json()
        return JsonResponse({'communes': commnues}, status = 200)
    return JsonResponse({}, status = 400)

def get_village_list(request):
    if request.method == "GET":
        commune_id = request.GET.get('commune_id', NONE)
        village_url = settings.API_ENDPOINT + 'village/?commune_id__id=' + str(commune_id)
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
        print(url)
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
        province_id = request.GET.get('province_id', NONE)
        #url = settings.API_ENDPOINT + "watersupplyreportmap/?water_supply_type_id="+ str(water_supply_id)
        #url = settings.API_ENDPOINT + "watersupplymap/?province_id="+str(province_id)
        #url = settings.API_ENDPOINT + "watersupplymap/?province_id="
        url = settings.API_ENDPOINT + "watersupplymap_v2/"
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

def report_supply_well_coverage_by_province(request):
    
    if request.method == "GET":
        date_start = request.GET.get('date_start', NONE)
        date_end = request.GET.get('date_end', NONE)
        province = request.GET.get('province', '')
        url = settings.API_ENDPOINT + "watersupplyfilterdaterange?created_at="+str(date_start)+"&crated_at_1="+str(date_end)+"&province_id="+province
        # print(url)
        list = requests.get(url).json()
        
        province_url = settings.API_ENDPOINT + "province/" + str(province)
        province = requests.get(province_url).json()
        
        return JsonResponse({'data': list, 'province': province}, status=200)
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

def get_watersupply_list_by_province(request):
    if request.method == "GET":
        #starttime = datetime.now()
        province_id = request.GET.get('province_id', '')
        ws_type = request.GET.get('ws_type', '')
        if ws_type == 0:
            ws_type = ''
        url = settings.API_ENDPOINT + 'watersupplylistbytype/?water_supply_type_id='+ str(ws_type) + '&province_id=' + str(province_id)
        print(url)
        response = requests.get(url).json()
        # endtime = datetime.now()
        # duration = endtime - starttime
        # f = open( 'filename_ajax.txt', 'w+' )
        # f.write('Start Time: '+ str(starttime) + '\n')
        # f.write('End time : ' + str(endtime) + '\n')
        # f.write( 'Duration : ' + str(duration) + '\n')
        # f.close()

        return JsonResponse({'data':response}, status=200)
    return JsonResponse({}, status=400)

def get_beneficiary_people_by_country(request):
    if request.method == "GET":
        ws_type = request.GET.get('ws_type', 0)
        url = settings.API_ENDPOINT + "watersupplybeneficiarytotalpeoplebycountry/"+str(ws_type)+"/"
        #print(url)
        list = requests.get(url).json()
        
        country_url = settings.API_ENDPOINT + "country/1/"
        country = requests.get(country_url).json()

        return JsonResponse({'data': list, 'country':country}, status=200)

    return JsonResponse({}, status=400) 

#START POST SECTION
def post_approval_watersupply_by_provicial_head_department(request):
    if request.method == "GET":
        try:
            headers = {'Content-Type': 'application/json'}
            water_supply_id = request.GET.get('water_supply_id', 0)
            status_id = request.GET.get('status_id',NONE)
            remark = request.GET.get('remark',NONE)

            #print(water_supply_id + " " + status_id)
            ws_workflow = "http://3.0.166.20/en/api/v2/watersupplyworkflow"
            payload_wsworkflow = {
                "watersupply_id":int(water_supply_id),
                "status_id":int(status_id),#1
                "user_id": int(request.session['user']['id']),
                "remark": remark
            }
            print(payload_wsworkflow)
            response_ws_workflow = requests.post(ws_workflow, json=payload_wsworkflow, headers=headers).json()
            print(response_ws_workflow)

            #Update Water Supply MainStatus
            ws_update_url = "http://3.0.166.20/en/api/watersupply/"+ str (water_supply_id) +"/update/"
            ws_update_payload = {
                "id": water_supply_id,
                "main_status": status_id #1
            }
            response_ws_upate_mainstatus = requests.put(ws_update_url, json=ws_update_payload, headers=headers).json()
            #print(response_ws_upate_mainstatus)
        except Exception as e:

            raise e

        return JsonResponse({'is_success':True},status=200)
    return JsonResponse({}, status=400)

def put_water_supply_delete(request):
    if request.method == "GET":
        headers = {'Content-Type': 'application/json'}
        water_supply_id = request.GET.get('water_supply_id', 0)

        ws_delete_url = "http://3.0.166.20/en/api/v2/watersupply/" + str(water_supply_id) + "/delete/"
        ws_delete_payload = {
            "id":int(water_supply_id),
            "updated_by": int(request.session['user']['id']),
            "is_active": False
        }
        response_delete_ws = requests.put(ws_delete_url, json=ws_delete_payload, headers=headers).json()
        return JsonResponse({'is_success':True},status=200)
    return JsonResponse({}, status=400)

#END POST SECTION

