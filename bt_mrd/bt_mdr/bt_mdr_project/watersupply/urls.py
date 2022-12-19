from django.urls import path
from . import views

#app_name = 'mdrapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/<int:id>', views.create_watersupply, name= 'watersupply_create'),
    path('detail/<int:id>', views.detail, name= 'watersupply_detail'),
    path('userlist/', views.user_index, name='user_index'),
]
