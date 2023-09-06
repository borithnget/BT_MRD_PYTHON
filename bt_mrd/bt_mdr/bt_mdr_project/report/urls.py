from django.urls import include, path
from . import views

urlpatterns = [
    path('coverage_by_map', views.report_rural_water_supply_coverage_map, name='report_coverage_by_map'),
    path('wellsumbyprovince', views.report_well_sum_by_province, name='report_well_sum_by_province'),
    path('wellsumbyprovince/<str:token>/', views.report_well_sum_by_province_token, name='report_well_sum_by_province_token'),
    path('coverage_by_map/<str:token>/', views.report_rural_water_supply_coverage_map_token, name='report_coverage_by_map_token'),
]