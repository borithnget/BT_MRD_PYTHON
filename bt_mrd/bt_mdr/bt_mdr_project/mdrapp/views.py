from django.shortcuts import render, redirect
import googlemaps
import json
from django.conf import settings
from django.http import HttpResponse
import requests
import json
from rest_framework.parsers import JSONParser
import datetime, time
from qrcode import *
from django.conf import settings
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
# Create your views here.

# MAIN_URL = 'http://3.0.166.20/api/' 
# MAIN_URL_1 = 'http://3.0.166.20/en/'

def geocode(request):
    gmaps = googlemaps.Client(key= settings.GOOGLE_API_KEY)
    result = gmaps.geocode(str('Stadionstraat 5, 4815 NC Breda'))

    context = {
        'result':result,
    }
    return render(request, 'google/geocode.html', context)

def map(request):
    key = settings.GOOGLE_API_KEY
    context = {
        'key':key
    }
    return render(request, 'google/map.html', context)

# def home(request):
#     #authentication_classes=[SessionAuthentication]
#     count_pending = 0
#     count_well = 0 #1
#     count_small_pipe = 0 #2
#     count_water_kiosk = 0 #3
#     count_community_pond = 0 #4
#     count_rain_water_harvesting = 0 #5
#     count_pipe = 0 #6
#     count_air_to_water = 0 #7
#     if 'token' in request.session:
#         watersupply_type_url = settings.API_ENDPOINT + 'watersupplytype/'
#         watersupplytypelist = requests.get(watersupply_type_url).json()
#         count_well_response = requests.get(settings.API_ENDPOINT + 'watersupplygetcountbytype/1/').json()
#         if 'count' in count_well_response:
#             count_well = int(count_well_response['count'])
#         count_small_pipe_response = requests.get(settings.API_ENDPOINT + 'watersupplygetcountbytype/2/').json()
#         if 'count' in count_small_pipe_response:
#             count_small_pipe = int(count_small_pipe_response['count'])    
#         count_water_kiosk_response = requests.get(settings.API_ENDPOINT + 'watersupplygetcountbytype/3/').json()
#         if 'count' in count_water_kiosk_response:
#             count_water_kiosk = int(count_water_kiosk_response['count'])
#         count_community_pond_response = requests.get(settings.API_ENDPOINT + 'watersupplygetcountbytype/4/').json()
#         if 'count' in count_community_pond_response:
#             count_community_pond = int(count_community_pond_response['count'])   
#         count_rain_water_harvesting_response = requests.get(settings.API_ENDPOINT + 'watersupplygetcountbytype/5/').json()
#         if 'count' in count_rain_water_harvesting_response:
#             count_rain_water_harvesting = int(count_rain_water_harvesting_response['count'])   
#         count_pipe_response = requests.get(settings.API_ENDPOINT + 'watersupplygetcountbytype/6/').json()
#         if 'count' in count_pipe_response:
#             count_pipe = int(count_pipe_response['count'])    
#         count_air_to_water_response = requests.get(settings.API_ENDPOINT + 'watersupplygetcountbytype/7/').json()
#         if 'count' in count_air_to_water_response:
#             count_air_to_water = int(count_air_to_water_response['count'])
#         # if request.session['user']['is_data_entry']:
#         #     url = settings.API_ENDPOINT + "watersupplysubmittedbyuser/"+str(request.session['user']['id'])+"/"
#         #     json_response = requests.get(url).json()
#         #     if 'count' in json_response:
#         #         count_pending= count_pending + int(json_response['count'])
#         # #print(json_response)
#         # if request.session['user']['is_provincial_department_head']:          
#         #     province = request.session['user']['provincial_department_head_province_id']            
#         #     url = settings.API_ENDPOINT + "watersupplypendingprovincial/" + str(province) +"/"
#         #     json_response = requests.get(url).json()
#         #     if 'count' in json_response:
#         #         count_pending= count_pending + int(json_response['count'])
#         # if request.session['user']['is_data_verifier_1']:
#         #     url = settings.API_ENDPOINT + "watersupplycountpendingapproval/2/"
#         #     json_response = requests.get(url).json()
#         #     if 'count' in json_response:
#         #         count_pending= count_pending + int(json_response['count'])
#         # if request.session['user']['is_data_verifier_2']:
#         #     url = settings.API_ENDPOINT + "watersupplycountpendingapproval/5/"
#         #     json_response = requests.get(url).json()
#         #     if 'count' in json_response:
#         #         count_pending= count_pending + int(json_response['count'])
#         # if request.session['user']['is_head_department']:
#         #     url = settings.API_ENDPOINT + "watersupplycountpendingapproval/7/"
#         #     json_response = requests.get(url).json()
#         #     if 'count' in json_response:
#         #         count_pending= count_pending + int(json_response['count'])
#     else:
#         return redirect('user_login')
#     context = {
#         'count_pending' : count_pending,
#         'key' : settings.GOOGLE_API_KEY,
#         'watersupplytypelist' : watersupplytypelist,
#         'count_well' : count_well,
#         'count_small_pipe' : count_small_pipe,
#         'count_water_kiosk': count_water_kiosk,
#         'count_community_pond':count_community_pond,
#         'count_rain_water_harvesting': count_rain_water_harvesting,
#         'count_pipe': count_pipe,
#         'count_air_to_water' : count_air_to_water
#     }
#     return render(request, 'home.html', context)

def home(request):

    #authentication_classes=[SessionAuthentication]

    count_pending = 0
    count_well = 0 #1
    count_small_pipe = 0 #2
    count_water_kiosk = 0 #3
    count_community_pond = 0 #4
    count_rain_water_harvesting = 0 #5
    count_pipe = 0 #6
    count_air_to_water = 0 #7
    
    watersupply_type_url = settings.API_ENDPOINT + 'watersupplytype/'
    watersupplytypelist = requests.get(watersupply_type_url).json()

    count_well_response = requests.get(settings.API_ENDPOINT + 'watersupplygetcountbytype/1/').json()
    if 'count' in count_well_response:
        count_well = int(count_well_response['count'])

    count_small_pipe_response = requests.get(settings.API_ENDPOINT + 'watersupplygetcountbytype/2/').json()
    if 'count' in count_small_pipe_response:
        count_small_pipe = int(count_small_pipe_response['count'])
        
    count_water_kiosk_response = requests.get(settings.API_ENDPOINT + 'watersupplygetcountbytype/3/').json()
    if 'count' in count_water_kiosk_response:
        count_water_kiosk = int(count_water_kiosk_response['count'])

    count_community_pond_response = requests.get(settings.API_ENDPOINT + 'watersupplygetcountbytype/4/').json()
    if 'count' in count_community_pond_response:
        count_community_pond = int(count_community_pond_response['count'])
        
    count_rain_water_harvesting_response = requests.get(settings.API_ENDPOINT + 'watersupplygetcountbytype/5/').json()
    if 'count' in count_rain_water_harvesting_response:
        count_rain_water_harvesting = int(count_rain_water_harvesting_response['count'])
        
    count_pipe_response = requests.get(settings.API_ENDPOINT + 'watersupplygetcountbytype/6/').json()
    if 'count' in count_pipe_response:
        count_pipe = int(count_pipe_response['count'])
        
    count_air_to_water_response = requests.get(settings.API_ENDPOINT + 'watersupplygetcountbytype/7/').json()
    if 'count' in count_air_to_water_response:
        count_air_to_water = int(count_air_to_water_response['count'])

    context = {
        'count_pending' : count_pending,
        'key' : settings.GOOGLE_API_KEY,
        'watersupplytypelist' : watersupplytypelist,
        'count_well' : count_well,
        'count_small_pipe' : count_small_pipe,
        'count_water_kiosk': count_water_kiosk,
        'count_community_pond':count_community_pond,
        'count_rain_water_harvesting': count_rain_water_harvesting,
        'count_pipe': count_pipe,
        'count_air_to_water' : count_air_to_water
    }
    return render(request, 'home.html', context)

def user_login(request):

    error_msgs = []

    if request.method == "POST":
        #login_url = "http://3.0.166.20/en/api/login/"
        #login_url = "http://3.0.166.20/en/api/login/"
        login_url = settings.API_ENDPOINT + "login/"
        payload = {
            "username": request.POST["username"],
            "password": request.POST["password"]
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(login_url, json=payload, headers=headers).json()
        print(response)
        if 'data' in response:
            print(response['user'])
            request.session['token'] = response['data']['token']
            request.session['user'] = response['user']
            return redirect('home')
        elif 'non_field_errors' in response:
            error_msgs.append(response['non_field_errors'])
            #error_msgs.append("ធ្វើអីខុសដឹងខ្លួនឯងហើយ!")
            return render(request, 'users/login.html', { 'error_msgs': error_msgs })
        else: 
            return redirect('user_login')
        
        return render(request, 'users/login.html', { 'error_msgs': error_msgs })

    return render(request, 'users/login.html')