from django.shortcuts import render
from django.conf import settings
import requests

# Create your views here.
def report_rural_water_supply_coverage_map(request):
    url = settings.API_ENDPOINT + 'watersupplytype/'
    watersupplytypelist = requests.get(url).json()
    if 'token' in request.session:
        if request.session['user']['is_data_entry']:
            province_url = settings.API_ENDPOINT + 'province/?id=' + str(request.session['user']['data_entry_province_id'])
            #print(request.user.data_entry_province_id.id)
        else:
            province_url = settings.API_ENDPOINT + 'province'
    else:
        province_url = settings.API_ENDPOINT + 'province'
    provinces = requests.get(province_url).json()

    return render(request, 'report/report_water_supply_coverage_map.html', 
                  { 'key':settings.GOOGLE_API_KEY, 
                    "watersupplytypelist": watersupplytypelist ,
                    "provinces" : provinces
                })

def report_rural_water_supply_coverage_map_token(request, token):
    url = settings.API_ENDPOINT + 'watersupplytype/'
    watersupplytypelist = requests.get(url).json()
    province_url = settings.API_ENDPOINT + 'province'
    provinces = requests.get(province_url).json()

    return render(request, 'report/report_water_supply_coverage_map.html', 
                  { 'key':settings.GOOGLE_API_KEY, 
                    "watersupplytypelist": watersupplytypelist ,
                    "provinces" : provinces
                })

def report_well_sum_by_province(request):
    url = settings.API_ENDPOINT + 'watersupplytype/'
    watersupplytypelist = requests.get(url).json()

    if 'token' in request.session:
        if request.session['user']['is_data_entry']:
            province_url = settings.API_ENDPOINT + 'province/?id=' + str(request.session['user']['data_entry_province_id'])
            #print(request.user.data_entry_province_id.id)
        else:
            province_url = settings.API_ENDPOINT + 'province'
    else:
        province_url = settings.API_ENDPOINT + 'province'
    provinces = requests.get(province_url).json()
    return render(request, 'report/report_well_sum_by_province.html',
                  
                  { "provinces" : provinces,
                   "watersupplytypelist": watersupplytypelist
                   })

def report_well_sum_by_province_token(request, token):
    url = settings.API_ENDPOINT + 'watersupplytype/'
    watersupplytypelist = requests.get(url).json()
    province_url = settings.API_ENDPOINT + 'province'    
    provinces = requests.get(province_url).json()
    return render(request, 'report/report_well_sum_by_province.html',
                  { "provinces" : provinces,"watersupplytypelist":watersupplytypelist })