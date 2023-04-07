#from .views import *
from django.urls import path, include
from . import views 

urlpatterns = [
   #path('', views.home, name="home"),
   path('geocode/', views.geocode, name="geocode"),
   path('map', views.map, name="map"),
   path('', views.home, name='home'),
   path('login', views.user_login, name='user_login'),
]