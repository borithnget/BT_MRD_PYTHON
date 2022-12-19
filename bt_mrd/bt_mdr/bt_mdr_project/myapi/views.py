import imp
from pickle import NONE
from urllib import response
from django.shortcuts import render
from rest_framework import viewsets, generics, permissions, filters, status
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework.views import APIView

from mdrapp.models import Commune, Province, District, Village, WaterSupplyType, WaterSupplyOption, WaterSupplyOptionValue, WaterSupplyTypeOption, WaterSupply, WaterSupplyWell, WaterSupplyPipe, WaterSupplyKiosk, WaterSupplyCommunityPond, WaterSupplyRainWaterHarvesting
from .serializers import CommuneSerializer, HeroSerializer, UserSerializer, RegisterSerializer, ProvinceSerializer, DistrictSerializer, VillageSerializer, WaterSupplyOptionSerializer, WaterSupplyOptionValueSerializer, WaterSupplyTypeSerializer, WaterSupplySerializer, UserDetailSerializer
from .models import Hero
from django.contrib.auth import login
from knox.views import LoginView as KnoxLoginView
from knox.models import AuthToken
import django_filters.rest_framework
from . import serializers
import datetime
from django.http import JsonResponse
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAdminUser
# Create your views here.

class HeroViewSet(viewsets.ModelViewSet):
    queryset = Hero.objects.all().order_by('name')
    serializer_class = HeroSerializer
    
# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })
        
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)
    
class ProvinceViewSet(viewsets.ModelViewSet):
    model = Province
    queryset = Province.objects.all().order_by('name_en').filter(is_active=True)
    serializer_class = ProvinceSerializer
    
class DistrictViewSet(viewsets.ModelViewSet):
    model = District
    queryset = District.objects.all().order_by('name_en').filter(is_active=True)
    serializer_class = DistrictSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['province_id__id']

class CommnueViewSet(viewsets.ModelViewSet):
    model = Commune
    queryset = Commune.objects.all().order_by('name_en').filter(is_active=True)
    serializer_class = CommuneSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['district_id__id']
    
class VillageViewSet(viewsets.ModelViewSet):
    model = Village
    queryset = Village.objects.all().order_by('name_en').filter(is_active=True)
    serializer_class = VillageSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['commune_id__id']
    
class WaterSupplyTypeViewSet(viewsets.ModelViewSet):
    model = WaterSupplyType
    queryset = WaterSupplyType.objects.all().order_by('code').filter(is_active=True)
    serializer_class = WaterSupplyTypeSerializer
    
class WaterSupplyOptionViewSet(viewsets.ModelViewSet):
    model = WaterSupplyOption
    queryset = WaterSupplyOption.objects.all().order_by('code').filter(is_active=True)
    serializer_class = WaterSupplyOptionSerializer
    
class WaterSupplyOptionValueViewSet(viewsets.ModelViewSet):
    model = WaterSupplyOptionValue
    queryset = WaterSupplyOptionValue.objects.all().order_by('code').filter(is_active=True)
    serializer_class = WaterSupplyOptionValueSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['water_supply_option_id__id']
    
class WaterSupplyTypeOptionViewSet(viewsets.ModelViewSet):
    model = WaterSupplyTypeOption
    queryset = WaterSupplyTypeOption.objects.select_related('water_supply_option_id').all().order_by('ordering').filter(is_active=True)
    serializer_class = serializers.WaterSupplyTypeOptionSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['water_supply_type_id__id']
    
class WaterSupplyViewSet(viewsets.ModelViewSet):
    model = WaterSupply
    queryset = WaterSupply.objects.all().order_by('-created_at').filter(is_active=True)
    serializer_class = serializers.WaterSupplySerializer
    
class WaterSupplyViewSet_2(viewsets.ModelViewSet):
    model = WaterSupply
    queryset = WaterSupply.objects.all().order_by('-created_at').filter(is_active=True)
    serializer_class = serializers.WaterSupplySerializer_v2
    
class WaterSupplyCreateAPIView(generics.CreateAPIView):
  permission_classes = (AllowAny,)
  serializer_class = serializers.WaterSupplySerializer_v2
  
  def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            'status': 200,
            'message': 'Testimonials fetched',
            'data': response.data
        })

class WaterSupplyWellViewSet(viewsets.ModelViewSet):
    model= WaterSupplyWell
    queryset = WaterSupplyWell.objects.all().filter(is_active=True)
    serializer_class = serializers.WaterSupplyWellSerializer

class WaterSupplyPipeViewSet(viewsets.ModelViewSet):
    model = WaterSupplyPipe
    queryset = WaterSupplyPipe.objects.all().filter(is_active=True)
    serializer_class = serializers.WaterSupplyPipeSerializer

class WaterSupplyKioskViewSet(viewsets.ModelViewSet):
    model = WaterSupplyKiosk
    queryset = WaterSupplyKiosk.objects.all().filter(is_active=True)
    serializer_class = serializers.WaterSupplyKioskSerializer

class WaterSupplyCommunityPondViewSet(viewsets.ModelViewSet):
    model = WaterSupplyCommunityPond
    queryset = WaterSupplyCommunityPond.objects.all().filter(is_active=True)
    serializer_class = serializers.WaterSupplyCommuniryPondSerializer

class WaterSupplyRainWaterHarvestingViewSet(viewsets.ModelViewSet):
    model = WaterSupplyRainWaterHarvesting
    queryset = WaterSupplyRainWaterHarvesting.objects.all().filter(is_active=True)
    serializer_class = serializers.WaterSupplyRainWaterHarvestingSerializer

class UserListViewSet(generics.ListAPIView):
    User = get_user_model()
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    #permission_classes = [IsAuthenticated]

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = UserDetailSerializer(queryset, many=True)
        return Response(serializer.data)
  

# class WaterSupplyAPIView(APIView):
#     http_method_names = ['get', 'head', 'post']
#     def get(self, request, *args, **kwargs):
#         queryset = WaterSupply.objects.all().order_by('created_at').filter(is_active=True)
#         serializer = serializers.WaterSupplySerializer_v2(queryset, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     def post(self, request, *args, **kwargs):
#         data = {
#             'water_supply_type_id': request.data.get('water_supply_type_id'),
#             'province_id': request.data.get('province_id'),
#             'district_id': request.data.get('district_id'),
#             'is_active': request.data.get('is_active'),
#             'created_by': request.data.get('created_by'),
#             'created_at' : datetime.datetime.now()
#         }
#         print(data)
#         watersupply_serializer =serializers.WaterSupplySerializer_v2(data=data)
#         if watersupply_serializer.is_valid():
#             watersupply_serializer.save()
#             # response = {
#             #     'data':watersupply_serializer.data,
#             #     'status':status.HTTP_201_CREATED
#             # }
#             # return JsonResponse(response)
#             return Response(watersupply_serializer.data, status=status.HTTP_201_CREATED) 
#         return Response(watersupply_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         #return JsonResponse({'status':status.HTTP_400_BAD_REQUEST, "message": watersupply_serializer.errors })
    