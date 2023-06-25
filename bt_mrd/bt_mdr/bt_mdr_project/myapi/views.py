import imp
import json
import io
from pickle import NONE
import time
from urllib import response
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, generics, permissions, filters, status
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework.views import APIView

from mdrapp.models import Commune, Province, District, Village, WaterSupplyType, WaterSupplyOption, WaterSupplyOptionValue, WaterSupplyTypeOption, WaterSupply, WaterSupplyWell, WaterSupplyPipe, WaterSupplyKiosk, WaterSupplyCommunityPond, WaterSupplyRainWaterHarvesting, Status, WaterSupplyWorkFlow, UserDetail, WaterSupplyQRCode, WaterSupplyHistory, WaterSupplyPipeOptionValue, WaterQualityCheckedParamater, WaterSupplyQuanlityCheckParamater, WaterSupplyKioskOptionValue, WaterSupplyPipePrivate, WaterSupplyPipePrivateOptionValue, WaterSupplyAirWater, WaterSupplyAirWaterOptionValue, User, Country
from mdrapp.views import MAIN_URL_1
from .serializers import CommuneSerializer, HeroSerializer, UserSerializer, RegisterSerializer, ProvinceSerializer, DistrictSerializer, VillageSerializer, WaterSupplyOptionSerializer, WaterSupplyOptionValueSerializer, WaterSupplyTypeSerializer, WaterSupplySerializer, UserDetailSerializer, StatusSerializer, WaterSupplyWorkflowSerializer,  WaterSupplyWellOptionValue, UserRoleDetailSerializer, WaterSupplyQRCodeSerializer, WaterSupplyUpdateMainStatusSerializer
from .models import Hero
from django.contrib.auth import login, authenticate
from knox.views import LoginView as KnoxLoginView
from knox.models import AuthToken
import django_filters.rest_framework
from . import serializers
import datetime
from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from django_filters import DateRangeFilter,DateFilter
from django.db.models import Sum
from django_filters.fields import CSVWidget
from .filters import WaterSupplyMultipleFilterBackend
import csv
from django.conf import settings
from qrcode import *

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
        #return super(LoginAPI, self).post(request, format=None)
        temp_list = super(LoginAPI, self).post(request, format=None)
        #user_detail = User.objects.filter(id=user.id)
        #temp_list.data['user'] = user_detail
        return Response({
            "data" : temp_list.data,
            "user" : UserSerializer(user).data,
            })

class SignInAPI(generics.GenericAPIView):
    serializer_class =  serializers.LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })

class MainUser(generics.RetrieveAPIView):
  permission_classes = [
      permissions.IsAuthenticated
  ]
  serializer_class = UserSerializer

  def get_object(self):
    return self.request.user

@ensure_csrf_cookie
def set_csrf_token(request):
    """
    This will be `/api/set-csrf-cookie/` on `urls.py`
    """
    return JsonResponse({"details": "CSRF cookie set"})

@api_view(['POST',])
@permission_classes((AllowAny,))
def login_view(request):
    """
    POST API for login
    """
    #data = json.loads(request.data)
    #print(data)
    authentication_classes = (SessionAuthentication, )
    username = request.data.get('username')
    password = request.data.get('password')
    if username is None:
        return JsonResponse({
            "errors": {
                "detail": "Please enter username"
            }
        }, status=400)
    elif password is None:
        return JsonResponse({
            "errors": {
                "detail": "Please enter password"
            }
        }, status=400)

    # authentication user
    user = authenticate(username=username, password=password)
    #print(user)
    if user is not None:
        login(request, user)
        return JsonResponse({"success": "User has been logged in"})
    return JsonResponse(
        {"errors": "Invalid credentials"},
        status=400,
    )

# class ChangePasswordView(generics.UpdateAPIView):
#     """
#     An endpoint for changing password.
#     """
#     serializer_class = serializers.ChangePasswordSerializer
#     model = get_user_model()
#     #permission_classes = (IsAuthenticated,)

#     def get_object(self, queryset=None):
#         obj = self.request.session['user']
#         return obj

#     def update(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         serializer = self.get_serializer(data=request.data)

#         if serializer.is_valid():
#             # Check old password
#             if not self.object.check_password(serializer.data.get("old_password")):
#                 return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
#             # set_password also hashes the password that the user will get
#             self.object.set_password(serializer.data.get("new_password"))
#             self.object.save()
#             response = {
#                 'status': 'success',
#                 'code': status.HTTP_200_OK,
#                 'message': 'Password updated successfully',
#                 'data': []
#             }

#             return Response(response)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(generics.UpdateAPIView):

    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ChangePasswordSerializer

class ProvinceViewSet(viewsets.ModelViewSet):
    model = Province
    queryset = Province.objects.all().order_by('code_en').filter(is_active=True)
    serializer_class = ProvinceSerializer
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['id']
    filter_backends = [DjangoFilterBackend]
    filterset_fields  = ['id']

class DistrictViewSet(viewsets.ModelViewSet):
    model = District
    queryset = District.objects.all().order_by('code_en').filter(is_active=True)
    serializer_class = DistrictSerializer
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['province_id__id']
    filter_backends = [DjangoFilterBackend]
    filterset_fields  = ['province_id__id']

class CommnueViewSet(viewsets.ModelViewSet):
    model = Commune
    queryset = Commune.objects.all().order_by('code_en').filter(is_active=True)
    serializer_class = CommuneSerializer
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['district_id__id']
    filter_backends = [DjangoFilterBackend]
    filterset_fields  = ['district_id__id']

class VillageViewSet(viewsets.ModelViewSet):
    model = Village
    queryset = Village.objects.all().order_by('code_en').filter(is_active=True)
    serializer_class = VillageSerializer
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['commune_id__id']
    filter_backends = [DjangoFilterBackend]
    filterset_fields  = ['commune_id__id']

class CountryViewSet(viewsets.ModelViewSet):
    model = Country
    queryset = Country.objects.all().order_by('code_en').filter(is_active=True)
    serializer_class = serializers.CountrySerializer

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
    # filter_backends = [filters.SearchFilter]
    # filter_fields = ['water_supply_type_id__id']
    # search_fields = ['water_supply_type_id__id']
    filter_backends = [DjangoFilterBackend]
    filterset_fields  = ['water_supply_type_id', 'main_status']

class WaterSupplyReportMap(viewsets.ModelViewSet):
    model = WaterSupply
    queryset = WaterSupply.objects.all().order_by('-created_at').filter(is_active=True).filter(main_status=9)
    serializer_class = serializers.WaterSupplySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields  = ['water_supply_type_id']

class WaterSupplyByUserAndStatusViewSet(viewsets.ModelViewSet):
    model = WaterSupply
    queryset = WaterSupply.objects.all().order_by('-created_at').filter(is_active=True)
    serializer_class = serializers.WaterSupplySerializer
    # filter_backends = [filters.SearchFilter]
    # filter_fields = ['water_supply_type_id__id']
    # search_fields = ['water_supply_type_id__id']
    filter_backends = [DjangoFilterBackend]
    filterset_fields  = ['created_by', 'main_status']



class WaterSupplyByUserViewSet(viewsets.ModelViewSet):
    model = WaterSupply
    queryset = WaterSupply.objects.all().order_by('-created_at').filter(is_active=True).exclude(main_status=3)
    serializer_class = serializers.WaterSupplySerializer
    filter_backends = [filters.SearchFilter]
    filter_fields = ['created_by__id']
    search_fields = ['created_by__id']

    # def get_queryset(self):                                            # added string
    #     return super().get_queryset().filter(created_by=self.request.user.id)

class WaterSupplyByProvinceViewSet(viewsets.ModelViewSet):
    model = WaterSupply
    queryset = WaterSupply.objects.all().order_by('-created_at').filter(is_active=True)
    serializer_class = serializers.WaterSupplySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields  = ['province_id', 'main_status']

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

class WaterSupplyUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.WaterSupplyUpdateSerializer
    lookup_field = "id"

    def get_object(self):
        id = self.kwargs["id"]
        return get_object_or_404(WaterSupply, id=id)

    def put(self, request, *args, **kwargs):
        response = self.update(request, *args, **kwargs)
        return Response({
            'status': 200,
            'message': 'Testimonials fetched',
            'data': response.data
        })

class WaterSupplyDeleteAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.WaterSupplyDeleteSerializer
    lookup_field = "id"

    def get_object(self):
        id = self.kwargs["id"]
        return get_object_or_404(WaterSupply, id=id)

    def put(self, request, *args, **kwargs):
        response = self.update(request, *args, **kwargs)
        return Response({
            'status': 200,
            'message': 'Testimonials fetched',
            'data': response.data
        })

class UserDeactivateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.UserDeactivateSerializer
    lookup_field = 'id'

    def get_object(self):
        id = self.kwargs["id"]
        return get_object_or_404(User, id=id)

    def put(self, request, *args, **kwargs):
        response = self.update(request, *args, **kwargs)
        return Response({
            'status': 200,
            'message': 'Testimonials fetched',
            'data': response.data
        })

class WaterSupplyWorkFlowCreateAPIVIew(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.WaterSupplyWorkflowSerializer_v2

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            'status': 200,
            'message': 'Testimonials fetched',
            'data': response.data
        })

class WaterSupplyCountSubmittedRequestbyUserGenericAPIView(generics.ListAPIView):
    serializer_class = serializers.WaterSupplyWorkflowSerializer
    permission_classes = (AllowAny, )

    def get_queryset(self):
        user = self.kwargs['user']
        return WaterSupply.objects.filter(created_by=user).filter(is_active=True).filter(main_status=1)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        count = queryset.count()
        # return Response({"count":count, "data":serializer.data})
        return Response({"count":count})

class WaterSupplyCountProvincialHeadDepartmentGenericAPIView(generics.ListAPIView):
    serializer_class = serializers.WaterSupplySerializer
    permission_classes = (AllowAny, )

    def get_queryset(self):
        province = self.kwargs['province']
        return WaterSupply.objects.filter(province_id=province).filter(is_active=True).filter(main_status=1)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        count = queryset.count()
        # return Response({"count":count, "data":serializer.data})
        return Response({"count":count})

class WaterSupplyCountPendingApprovalGenericAPIVIew(generics.ListAPIView):
    serializer_class = serializers.WaterSupplySerializer
    permission_classes = (AllowAny, )

    def get_queryset(self):
        status = self.kwargs['status']
        return WaterSupply.objects.filter(is_active=True).filter(main_status=status)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        count = queryset.count()
        # return Response({"count":count, "data":serializer.data})
        return Response({"count":count})

class WaterSupplyHistoryViewSet(viewsets.ModelViewSet):
    model = WaterSupplyHistory
    queryset = WaterSupplyHistory.objects.all().order_by('-id')
    serializer_class = serializers.WaterSupplyHistortSerializer

class WaterSupplyWellViewSet(viewsets.ModelViewSet):
    model= WaterSupplyWell
    queryset = WaterSupplyWell.objects.all().order_by('-id').filter(is_active=True)
    serializer_class = serializers.WaterSupplyWellSerializer

class WaterSupplyWellOptionValueViewSet(viewsets.ModelViewSet):
    model = WaterSupplyWellOptionValue
    queryset = WaterSupplyWellOptionValue.objects.all().order_by('-id').filter(is_active=True)
    serializer_class = serializers.WaterSupplyWellOptionValueSerializer

class WaterSupplyPipeViewSet(viewsets.ModelViewSet):
    model = WaterSupplyPipe
    queryset = WaterSupplyPipe.objects.all().filter(is_active=True)
    serializer_class = serializers.WaterSupplyPipeSerializer

class WaterSupplyPipeOptionValueViewSet(viewsets.ModelViewSet):
    model = WaterSupplyPipeOptionValue
    queryset = WaterSupplyPipeOptionValue.objects.all().order_by('-id').filter(is_active=True)
    serializer_class = serializers.WaterSupplyPipeOptionValueSerializer

class WaterSupplyKioskViewSet(viewsets.ModelViewSet):
    model = WaterSupplyKiosk
    queryset = WaterSupplyKiosk.objects.all().filter(is_active=True)
    serializer_class = serializers.WaterSupplyKioskSerializer

class WaterSupplyKioskOptionValueViewSet(viewsets.ModelViewSet):
    model = WaterSupplyKioskOptionValue
    queryset = WaterSupplyKioskOptionValue.objects.all().order_by('-id').filter(is_active=True)
    serializer_class = serializers.WaterSupplyKioskOptionValueSerializer

class WaterSupplyCommunityPondViewSet(viewsets.ModelViewSet):
    model = WaterSupplyCommunityPond
    queryset = WaterSupplyCommunityPond.objects.all().filter(is_active=True)
    serializer_class = serializers.WaterSupplyCommuniryPondSerializer

class WaterSupplyRainWaterHarvestingViewSet(viewsets.ModelViewSet):
    model = WaterSupplyRainWaterHarvesting
    queryset = WaterSupplyRainWaterHarvesting.objects.all().filter(is_active=True)
    serializer_class = serializers.WaterSupplyRainWaterHarvestingSerializer

class StatusViewSet(viewsets.ModelViewSet):
    model = Status
    queryset = Status.objects.all().filter(is_active=True)
    serializer_class = StatusSerializer

class WaterSupplyWorkFlowViewSet(viewsets.ModelViewSet):
    model = WaterSupplyWorkFlow
    queryset = WaterSupplyWorkFlow.objects.all().order_by('-id')
    serializer_class = WaterSupplyWorkflowSerializer
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['watersupply_id__id']
    filter_backends = [DjangoFilterBackend]
    filterset_fields  = ['watersupply_id', 'user_id', 'status_id']

class WaterSupplyQRCodeViewSet(viewsets.ModelViewSet):
    model = WaterSupplyQRCode
    queryset = WaterSupplyQRCode.objects.all()
    serializer_class = WaterSupplyQRCodeSerializer

class WaterSupplyUpdateMainStatusAPIVIew(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = WaterSupplyUpdateMainStatusSerializer
    lookup_field = "id"

    def get_object(self):
        id = self.kwargs["id"]
        return get_object_or_404(WaterSupply, id=id)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

class WSByDateRange(generics.RetrieveAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = WaterSupplySerializer

    lookup_field = ["sd", "ed"]

    def get_object(self):
        sd = self.kwargs['sd']
        ed = self.kwargs['ed']
        return WaterSupply.objects.all().order_by('-id').filter(is_active=True)

class UserListViewSet(generics.ListAPIView):
    User = get_user_model()
    queryset = User.objects.all().filter(is_active =True)
    serializer_class = UserDetailSerializer
    #permission_classes = [IsAuthenticated]

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = UserDetailSerializer(queryset, many=True)
        return Response(serializer.data)

class UserRoleDetailViewSet(viewsets.ModelViewSet):
    model = UserDetail
    queryset = UserDetail.objects.all()
    serializer_class = UserRoleDetailSerializer

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

class WaterQuanlityCheckParameterViewSet(viewsets.ModelViewSet):
    model = WaterQualityCheckedParamater
    queryset = WaterQualityCheckedParamater.objects.all().order_by('id').filter(is_active=True)
    serializer_class = serializers.WaterQuanlityCheckParameterSerializer

class WaterSupplyQualityCheckParameterViewSet(viewsets.ModelViewSet):
    model = WaterSupplyQuanlityCheckParamater
    queryset = WaterSupplyQuanlityCheckParamater.objects.all().order_by('-id').filter(is_active=True)
    serializer_class = serializers.WaterSupplyQuanlityCheckParamaterSerializer

class WaterSupplyPipePrivateViewSet(viewsets.ModelViewSet):
    model = WaterSupplyPipePrivate
    queryset = WaterSupplyPipePrivate.objects.all().order_by('-id').filter(is_active=True)
    serializer_class = serializers.WaterSupplyPipePrivateSerializer

class WaterSupplyPipePrivateOptionValueViewSet(viewsets.ModelViewSet):
    model = WaterSupplyPipePrivateOptionValue
    queryset = WaterSupplyPipePrivateOptionValue.objects.all().order_by('-id').filter(is_active=True)
    serializer_class = serializers.WaterSupplyPipePrivateOptionValueSerializer

class WaterSupplyAirWaterViewSet(viewsets.ModelViewSet):
    model = WaterSupplyAirWater
    queryset = WaterSupplyAirWater.objects.all().order_by('-id').filter(is_active=True)
    serializer_class = serializers.WaterSupplyAirWaterSerializer

class WatersupplyAirWaterOptionValueViewSet(viewsets.ModelViewSet):
    model = WaterSupplyAirWaterOptionValue
    queryset = WaterSupplyAirWaterOptionValue.objects.all().order_by('-id').filter(is_active=True)
    serializer_class = serializers.WaterSupplyAirWaterOptionValueSerializer

class WaterSupplyFilterDateRange(django_filters.FilterSet):
    created_at = DateFilter(lookup_expr="gte")
    crated_at_1 = DateFilter(lookup_expr="lte")
    #created_at = DateRangeFilter(label='Date_Range')
    #created_at = filters.DateFromToRangeFilter()
    # start_date = DateFilter(name='created_at',lookup_type=('gt'),)
    # end_date = DateFilter(name='created_at',lookup_type=('lt'))

    class Meta:
        model = WaterSupply
        fields = ['created_at', 'crated_at_1', 'province_id']

# class WaterSupplyFilterDateRange(django_filters.FilterSet):
#     created_at = django_filters.DateRangeFilter()
#     #created_at = DateFilter(lookup_expr="gte")

#     class Meta:
#         model = WaterSupply
#         fields = ['created_at']


import django_filters
from psycopg2.extras import DateRange

class DateExactRangeWidget(django_filters.widgets.DateRangeWidget):
    """Date widget to help filter by *_start and *_end."""
    suffixes = ['start', 'end']

class DateExactRangeField(django_filters.fields.DateRangeField):
    widget = DateExactRangeWidget

    def compress(self, data_list):
        if data_list:
            start_date, stop_date = data_list
            return DateRange(start_date, stop_date)


class DateExactRangeFilter(django_filters.Filter):
    """
    Filter to be used for Postgres specific Django field - DateRangeField.
    https://docs.djangoproject.com/en/2.1/ref/contrib/postgres/fields/#daterangefield
    """
    field_class = DateExactRangeField

import django_filters
class WaterSupplyFilterDateRange1(django_filters.rest_framework.FilterSet):
    created_at = DateExactRangeFilter()

    class Meta:
        model = WaterSupply
        fields = [
            'created_at',
        ]

class WaterSupplyFilterDateRangeListView(generics.ListAPIView):
    serializer_class = serializers.WaterSupplySerializer
    queryset = WaterSupply.objects.all().order_by('-id').filter(is_active=True).filter(main_status=9).filter(water_supply_type_id=1)
    filter_backends = [DjangoFilterBackend]
    filterset_class = WaterSupplyFilterDateRange

class WaterSupplyByStatusMutipleViewSet(viewsets.ModelViewSet):
    model = WaterSupply
    queryset = WaterSupply.objects.all().order_by('-created_at').filter(is_active=True)
    serializer_class = serializers.WaterSupplySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class =  WaterSupplyMultipleFilterBackend

class WaterSupplyGetBeneficiaryTotalPeople(generics.ListAPIView):
    serializer_class = serializers.WaterSupplySerializer

    def get_queryset(self):
        wstype = self.kwargs['type']
        province_id = self.kwargs['province']
        if wstype == 0:
            return WaterSupply.objects.all().order_by('-id').filter(is_active=True).filter(main_status=9).filter(province_id=province_id)
        else:
            return WaterSupply.objects.all().order_by('-id').filter(is_active=True).filter(main_status=9).filter(province_id=province_id).filter(water_supply_type_id=wstype)

    # def get(self, request):
    #     """List Transactions"""
    #     transaction = WaterSupply.objects.all().order_by('-id').filter(is_active=True).filter(main_status=9)
    #     serializer = WaterSupplySerializer(transaction, many=True)
    #     ssum = transaction.aggregate(sum=Sum('beneficiary_total_people'))['sum']
    #     #return_data = {"sum": str(sum([lambda items: items['beneficiary_total_people']])), "objects": serializer.data}
    #     #return_data = {"sum": ssum, "objects": serializer.data}
    #     return_data = {"sum": ssum}
    #     return Response(return_data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        count = queryset.count()
        beneficiary_total_people = queryset.aggregate(sum=Sum('beneficiary_total_people'))['sum']

        return Response({"count":count, "data":serializer.data, "beneficiary_total_people" : beneficiary_total_people})
        #return Response({"count":count})

class WaterSupplyBeneficiaryTotalPeopleByCountry(generics.ListAPIView):
    serializer_class = serializers.WaterSupplySerializer

    def get_queryset(self):
        wstype = self.kwargs['type']
        if wstype == 0:
            return WaterSupply.objects.all().order_by('-id').filter(is_active=True).filter(main_status=9)
        else:
            return WaterSupply.objects.all().order_by('-id').filter(is_active=True).filter(main_status=9).filter(water_supply_type_id=wstype)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        count = queryset.count()
        beneficiary_total_people = queryset.aggregate(sum=Sum('beneficiary_total_people'))['sum']

        return Response({"count":count, "beneficiary_total_people" : beneficiary_total_people})

class WaterSupplyFilterDateRangeProvinceCoverageListView(generics.ListAPIView):
    serializer_class = serializers.WaterSupplySerializer

    def get_queryset(self):
        date_from = self.kwargs['date_from']
        province_id = self.kwargs['province']
        if province_id == 0:
            return WaterSupply.objects.all().order_by('-id').filter(is_active=True).filter(main_status=9).filter(water_supply_type_id=1)
        else:
            return WaterSupply.objects.all().order_by('-id').filter(is_active=True).filter(main_status=9).filter(province_id=province_id).filter(water_supply_type_id=1)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        count = queryset.count()
        beneficiary_total_people = queryset.aggregate(sum=Sum('beneficiary_total_people'))['sum']

        return Response({"count":count, "data":serializer.data, "beneficiary_total_people" : beneficiary_total_people})


class ProvinceListAPIView(generics.ListAPIView):
    serializer_class = serializers.ProvinceSerializer_v2

class ExportCSVWaterSupply(APIView):

    def get(self,request, *args, **kwargs):
        # response = HttpResponse(content_type='text/csv')
        # response['Content-Disposition'] = 'attachment; filename="export.csv"'
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=export_test.xls'
        response.write(u'\ufeff'.encode('utf8'))

        writer = csv.writer(response)
        writer.writerow(['Name KH','Name KH'])

        for ws in Province.objects.all():
            # row = ','.join([
            #     #ws.id,
            #     ws.name_kh,
            #     ws.name_en
            # ])

            writer.writerow([ws.name_kh,ws.name_en])
            # Uint8List imageBytes;
            # File('image.jpg').writeAsBytes(imageBytes);
        #new_bytes_obj = io.BytesIO(response)

        return response

class GenerateQRCodeView(APIView):

    def get(self, request, *args, **kwags):
        id = self.kwargs['id']
        detail_url = MAIN_URL_1 + "watersupply/detail/" + str(id)
        img = make(detail_url)
        img_name = 'qr' + str(time.time()) + '.png'
        img.save(settings.MEDIA_ROOT + '/' + img_name)

        return Response({"qr_name": img_name})
