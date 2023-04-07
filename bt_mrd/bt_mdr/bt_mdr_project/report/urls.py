from django.urls import include, path
from . import views

urlpatterns = [
    path('coverage_by_map', views.report_rural_water_supply_coverage_map, name='report_coverage_by_map'),
    path('wellsumbyprovince', views.report_well_sum_by_province, name='report_well_sum_by_province'),
]