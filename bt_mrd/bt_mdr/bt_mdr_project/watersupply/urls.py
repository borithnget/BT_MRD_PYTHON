from django.urls import path
from . import views
#from mdrapp import views
#app_name = 'mdrapp'

urlpatterns = [
    path('index/<int:id>', views.index, name='index'),
    path('create/<int:id>', views.create_watersupply, name= 'watersupply_create'),
    path('detail/<int:id>', views.detail, name= 'watersupply_detail'),
    path('edit/<int:id>', views.edit, name="watersupply_edit"),
    path('myreqeust/', views.watersupply_myreqeust, name='watersupply_myrequest'),
    path('myapproval/', views.watersupply_myapproval, name="watersupply_myapproval"),
    path('myapprovalhistory/', views.watersupply_myapprovalhistory, name="watersupply_myapprovalhistory"),
    path('userlist/', views.user_index, name='user_index'),
    path('register/', views.user_register, name='user_register'),
    path('mainaccount/', views.user_main_account, name="user_main_account"),
    path('qrcode/', views.qr_gen, name='qr_gen'),

    path('reportwatersupplymap/', views.report_water_supply_map, name='report_watersupply_map'),
    path('reportwellbyprovince/', views.report_well_by_province, name="reportwellbyprovince"),
    path('reportwatersupplycoverage/', views.report_water_supply_coverage, name="reportwatersupplycoverage"),

    path('importruralwatersupply/', views.import_rural_water_supply, name="import_rural_water_supply"),

    path('reportwellbyprovince/<str:token>/', views.report_well_by_province_token, name="reportwellbyprovincetoken"),
    path('reportwatersupplycoverage/<str:token>/', views.report_water_supply_coverage_token, name="reportwatersupplycoveragetoken"),

    path('syncwatersupplymap/', views.sync_water_supply_map, name='syncwatersupplymap')
]
