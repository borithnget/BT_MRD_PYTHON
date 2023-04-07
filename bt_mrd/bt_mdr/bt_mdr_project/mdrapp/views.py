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

MAIN_URL = 'http://52.14.59.145/api/' 
MAIN_URL_1 = 'http://52.14.59.145/en/'

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

def home(request):

    authentication_classes=[SessionAuthentication]

    count_pending = 0
    if 'token' in request.session:
        if request.session['user']['is_data_entry']:
            url = settings.API_ENDPOINT + "watersupplysubmittedbyuser/"+str(request.session['user']['id'])+"/"
            json_response = requests.get(url).json()
            if 'count' in json_response:
                count_pending= count_pending + int(json_response['count'])
        #print(json_response)
        if request.session['user']['is_provincial_department_head']:          
            province = request.session['user']['provincial_department_head_province_id']            
            url = settings.API_ENDPOINT + "watersupplypendingprovincial/" + str(province) +"/"
            json_response = requests.get(url).json()
            if 'count' in json_response:
                count_pending= count_pending + int(json_response['count'])
        if request.session['user']['is_data_verifier_1']:
            url = settings.API_ENDPOINT + "watersupplycountpendingapproval/2/"
            json_response = requests.get(url).json()
            if 'count' in json_response:
                count_pending= count_pending + int(json_response['count'])
        if request.session['user']['is_data_verifier_2']:
            url = settings.API_ENDPOINT + "watersupplycountpendingapproval/5/"
            json_response = requests.get(url).json()
            if 'count' in json_response:
                count_pending= count_pending + int(json_response['count'])
        if request.session['user']['is_head_department']:
            url = settings.API_ENDPOINT + "watersupplycountpendingapproval/7/"
            json_response = requests.get(url).json()
            if 'count' in json_response:
                count_pending= count_pending + int(json_response['count'])
    else:
        return redirect('user_login')
    context = {
        'count_pending' : count_pending,
        'key' : settings.GOOGLE_API_KEY
    }
    return render(request, 'home.html', context)

def user_login(request):

    error_msgs = []

    if request.method == "POST":
        #login_url = "http://52.14.59.145/en/api/login/"
        #login_url = "http://127.0.0.1:8000/en/api/login/"
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