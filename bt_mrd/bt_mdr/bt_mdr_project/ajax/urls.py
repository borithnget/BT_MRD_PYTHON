from django.urls import path
from . import views

urlpatterns = [
    path('get/country', views.get_country_km, name="ajax_get_country_km"),
    path('get/district', views.district, name = "ajax_get_district"),
    path('get/commune_list', views.get_commnue_list, name="ajax_get_commune_list"),
    path('get/village_list', views.get_village_list, name="ajax_get_village_list"),
    path('get/province_list', views.get_province_list, name="ajax_get_province_list"),
    path('get/approval_by_provicial_head_department', views.post_approval_watersupply_by_provicial_head_department, name="ajax_post_approval_watersupply_by_provincialheaddepartment"),
    path('get/watersupplypublishlist', views.get_watersupply_list, name="ajax_get_watersupply_publish"),
    path('get/myrequest_draft', views.get_myrequest_draft_list, name='ajax_get_myrequest_draft_list'),
    path('get/myrequest_history', views.get_myrequest_history_list, name= 'ajax_get_myrequest_history_list'),
    path('get/water_supply_delete', views.put_water_supply_delete, name= 'ajax_put_water_supply_delete'),
    path('get/watersupplyreportmap', views.get_water_supply_report_map, name='ajax_get_water_supply_report_map'),
    path('get/reportwatersupplywellbydaterange', views.report_supply_well_by_province, name="ajax_get_report_water_supply_well_daterange"),
    path('get/beneficiarytotalpeople', views.get_beneficiary_total_people, name='ajax_get_beneficiarytotalpeople'),
    path('get/reqeusthistory_by_phd', views.get_phd_requested_history, name="ajax_get_phd_requested_history"),
]