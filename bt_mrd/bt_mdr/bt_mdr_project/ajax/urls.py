from django.urls import path
from . import views

urlpatterns = [
    path('get/district', views.district, name = "ajax_get_district"),
    path('get/commune_list', views.get_commnue_list, name="ajax_get_commune_list"),
    path('get/village_list', views.get_village_list, name="ajax_get_village_list"),
]