# myapi/urls.py
from django.urls import include, path
from rest_framework import routers
from . import views
from knox import views as knox_views
# from django.conf.urls import url 


router = routers.DefaultRouter()
# router.register(r'heroes', views.HeroViewSet)
router.register(r'country', views.CountryViewSet)
router.register(r'province', views.ProvinceViewSet)
router.register(r'district', views.DistrictViewSet)
router.register(r'commune', views.CommnueViewSet)
router.register(r'village', views.VillageViewSet)
router.register(r'watersupplytype', views.WaterSupplyTypeViewSet)
router.register(r'watersupplyoption', views.WaterSupplyOptionViewSet)
router.register(r'watersupplyoptionValue', views.WaterSupplyOptionValueViewSet)
router.register(r'watersupplytypeoption', views.WaterSupplyTypeOptionViewSet)
router.register(r'watersupply', views.WaterSupplyViewSet, basename='watersupply'),
router.register(r'watersupplywell', views.WaterSupplyWellViewSet)
router.register(r'watersupplypipe', views.WaterSupplyPipeViewSet)
router.register(r'watersupplykiosk', views.WaterSupplyKioskViewSet)
router.register(r'watersupplycommunitypond', views.WaterSupplyCommunityPondViewSet)
router.register(r'watersupplyrainwaterharvesting', views.WaterSupplyRainWaterHarvestingViewSet)
router.register(r'status', views.StatusViewSet)
router.register(r'watersupplyworkflow', views.WaterSupplyWorkFlowViewSet)
router.register(r'watersupplywelloptionvalue', views.WaterSupplyWellOptionValueViewSet)
router.register(r'watersupplybyuser', views.WaterSupplyByUserViewSet)
router.register(r'watersupplybyprovince', views.WaterSupplyByProvinceViewSet)
router.register(r'watersupplybyprovinceandmultiplestatus', views.WaterSupplyByStatusMutipleViewSet)
router.register(r'watersupplyqrcode', views.WaterSupplyQRCodeViewSet)
router.register(r'watersupplyhistory', views.WaterSupplyHistoryViewSet)
router.register(r'watersupplypipoptionvalue', views.WaterSupplyPipeOptionValueViewSet)
router.register(r'watersupplykioskoptionvalue', views.WaterSupplyKioskOptionValueViewSet)
router.register(r'waterquanlitycheck', views.WaterQuanlityCheckParameterViewSet)
router.register(r'watersupplyqualitycheckparameter', views.WaterSupplyQualityCheckParameterViewSet)
router.register(r'watersupplybyuserandstatus', views.WaterSupplyByUserAndStatusViewSet)
router.register(r'watersupplypipeprivate', views.WaterSupplyPipePrivateViewSet)
router.register(r'watersupplypipeprivateoptionvalue', views.WaterSupplyPipePrivateOptionValueViewSet)
router.register(r'watersupplyairwater', views.WaterSupplyAirWaterViewSet)
router.register(r'watersupplyairwateroptionvalue', views.WatersupplyAirWaterOptionValueViewSet)
router.register(r'watersupplyreportmap', views.WaterSupplyReportMap)
#router.register(r'v2/watersupply', views.WaterSupplyViewSet_2)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    #path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('register/',views.RegisterAPI.as_view(), name='register'),
    path('login/', views.LoginAPI.as_view(), name='apilogin'),
    path('logout/', knox_views.LogoutView.as_view(), name='apilogout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('changepassword/', views.ChangePasswordView.as_view(), name='change-password'),
    path('change_password/<int:pk>/', views.ChangePasswordView.as_view(), name='auth_change_password'),
    path('api-auth/login/', views.login_view, name="api-auth-login"),
    path('set-csrf/', views.set_csrf_token, name='Set-CSRF'),
    path('auth/login', views.SignInAPI.as_view()),
    path('auth/user', views.MainUser.as_view()),
    # path('v2/watersupply', views.WaterSupplyAPIView.as_view()),
    path('v2/watersupply', views.WaterSupplyCreateAPIView.as_view()),
    path('v2/watersupply/<int:id>/update/', views.WaterSupplyUpdateAPIView.as_view()),
    path('v2/watersupply/<int:id>/delete/', views.WaterSupplyDeleteAPIView.as_view()),
    path('v2/watersupplyworkflow', views.WaterSupplyWorkFlowCreateAPIVIew.as_view()),
    path('userlist/', views.UserListViewSet.as_view(), name='userlist'),
    path('watersupply/<int:id>/update/', views.WaterSupplyUpdateMainStatusAPIVIew.as_view(), name='WaterSupplyUpdateMainStatusAPI'),
    path('watersupplysubmittedbyuser/<int:user>/', views.WaterSupplyCountSubmittedRequestbyUserGenericAPIView.as_view()),
    path('watersupplypendingprovincial/<int:province>/', views.WaterSupplyCountProvincialHeadDepartmentGenericAPIView.as_view()),
    path('watersupplycountpendingapproval/<int:status>/', views.WaterSupplyCountPendingApprovalGenericAPIVIew.as_view()),
    path('watersupplyfilterdaterange', views.WaterSupplyFilterDateRangeListView.as_view()),
    path('v2/watersupplyfilterdaterange/<str:sd>/<str:ed>/', views.WSByDateRange.as_view()),
    path('watersupplybeneficiarytotalpeople/<int:type>/<int:province>/', views.WaterSupplyGetBeneficiaryTotalPeople.as_view()),
    path('watersupplybeneficiarytotalpeoplebycountry/<int:type>/', views.WaterSupplyBeneficiaryTotalPeopleByCountry.as_view()),
]