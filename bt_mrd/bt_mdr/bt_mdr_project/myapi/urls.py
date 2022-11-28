# myapi/urls.py
from django.urls import include, path
from rest_framework import routers
from . import views
from knox import views as knox_views
# from django.conf.urls import url 


router = routers.DefaultRouter()
router.register(r'heroes', views.HeroViewSet)
router.register(r'province', views.ProvinceViewSet)
router.register(r'district', views.DistrictViewSet)
router.register(r'commune', views.CommnueViewSet)
router.register(r'village', views.VillageViewSet)
router.register(r'watersupplytype', views.WaterSupplyTypeViewSet)
router.register(r'watersupplyoption', views.WaterSupplyOptionViewSet)
router.register(r'watersupplyoptionValue', views.WaterSupplyOptionValueViewSet)
router.register(r'watersupplytypeoption', views.WaterSupplyTypeOptionViewSet)
router.register(r'watersupply', views.WaterSupplyViewSet, basename='watersupply'),
#router.register(r'v2/watersupply', views.WaterSupplyViewSet_2)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('register/',views.RegisterAPI.as_view(), name='register'),
    path('login/', views.LoginAPI.as_view(), name='apilogin'),
    path('logout/', knox_views.LogoutView.as_view(), name='apilogout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    # path('v2/watersupply', views.WaterSupplyAPIView.as_view()),
    path('v2/watersupply', views.WaterSupplyCreateAPIView.as_view()),
    path('userlist/', views.UserListViewSet.as_view(), name='userlist')
]