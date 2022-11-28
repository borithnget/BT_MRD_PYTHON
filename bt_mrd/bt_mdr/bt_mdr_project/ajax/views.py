from pickle import NONE
from urllib import request
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests
# Create your views here.

MAIN_URL = 'http://127.0.0.1:8000/api/' 

def district(request):
    if request.method == "GET":
        province_id = request.GET.get('province_id', NONE)
        district_url = MAIN_URL + 'district/?search=' + str(province_id)
        districts = requests.get(district_url).json()
        return JsonResponse({"district" : districts}, status=200)
    return JsonResponse({}, status = 400)

def get_commnue_list(request):
    if request.method == "GET":
        district_id = request.GET.get('district_id', NONE)
        commune_url = MAIN_URL + 'commune/?search=' + str(district_id)
        commnues = requests.get(commune_url).json()
        return JsonResponse({'communes': commnues}, status = 200)
    return JsonResponse({}, status = 400)

def get_village_list(request):
    if request.method == "GET":
        commune_id = request.GET.get('commune_id', NONE)
        village_url = MAIN_URL + 'village/?search=' + str(commune_id)
        villages = requests.get(village_url).json()
        return JsonResponse({'villages':villages}, status=200)
    return JsonResponse({}, status=400)