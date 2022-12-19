from dataclasses import field, fields
from datetime import datetime
from email.policy import default
from pyexpat import model
from time import timezone
from rest_framework import serializers

from mdrapp import models
import myapi
from .models import Hero
from mdrapp.models import Commune, User, Province, District, Village, WaterSupplyType, WaterSupplyOption, WaterSupplyOptionValue, WaterSupply

class HeroSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Hero
        fields = ('id', 'name', 'alias')
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')
    
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined', 'is_head_department', 'is_data_entry')
        
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ('id', 'username', 'email', 'password', 'is_data_entry')
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'], validated_data['is_data_entry'])
        return user
    
class VillageSerializer(serializers.HyperlinkedModelSerializer):
    #commune_id = CommuneSerializer(many=False, read_only=True)
    class Meta:
        model = Village
        fields = ('id' ,'code_en', 'code_kh', 'name_en', 'name_kh', 'description' , "commune_id")

class CommuneSerializer(serializers.HyperlinkedModelSerializer):
    commnuevillage = VillageSerializer(many=True, read_only=True)
    class Meta:
        model = Commune
        fields = ('id' ,'code_en', 'code_kh', 'name_en', 'name_kh', 'description' ,'commnuevillage', "district_id")

class DistrictSerializer(serializers.HyperlinkedModelSerializer):
    districtcommnue = CommuneSerializer(many=True, read_only=True)
    class Meta:
        model = District
        fields = ('id' ,'code_en', 'code_kh', 'name_en', 'name_kh', 'description' ,'districtcommnue', "province_id")
  
class ProvinceSerializer(serializers.HyperlinkedModelSerializer):
    provincedistrict = DistrictSerializer(many= True, read_only=True)
    class Meta:
        model = Province
        # fields = '__all__'
        fields = ('id' ,'code_en', 'code_kh', 'name_en', 'name_kh', 'description' ,'provincedistrict')

class ProvinceSerializer_v2(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = '__all__'

class DistrictSerializer_v2(serializers.ModelSerializer):
    
    class Meta:
        model = District
        fields = '__all__'

class CommuneSerializer_v2(serializers.ModelSerializer):
    class Meta:
        model = Commune
        fields = '__all__'

class VillageSerializer_v2(serializers.ModelSerializer):
    #commune_id = CommuneSerializer(many=False, read_only=True)
    class Meta:
        model = Village
        fields = '__all__'
        
        
class WaterSupplyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterSupplyType
        fields = '__all__'
        
class WaterSupplyOptionValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterSupplyOptionValue
        fields = ('id', 'code', 'name_en', 'name_kh', 'description', 'is_active', 'water_supply_option_id')
        
class WaterSupplyOptionSerializer(serializers.ModelSerializer):
    
    watersupplyoption_value = WaterSupplyOptionValueSerializer(read_only=True, many=True)
    
    class Meta:
        model = WaterSupplyOption
        #fields = '__all__'
        fields=('id', 'name_en', 'name_kh', 'data_type', 'is_active', 'watersupplyoption_value', 'field_name')
        

        
class WaterSupplyTypeOptionSerializer(serializers.ModelSerializer):
    
    #watersupplytypeoption_option = WaterSupplyOptionSerializer(many=True)
    water_supply_type_id = WaterSupplyTypeSerializer(many=False)
    water_supply_option_id = WaterSupplyOptionSerializer(read_only=True, many=False)
    
    class Meta:
        model = models.WaterSupplyTypeOption
        # fields = '__all__'
        fields = ('id', 'ordering', 'water_supply_type_id', 'water_supply_option_id')

class WaterSupplyWellSerializer(serializers.ModelSerializer):

    well_type_obj = serializers.SerializerMethodField()
    well_watar_quality_obj = serializers.SerializerMethodField()
    well_water_quality_check_obj = serializers.SerializerMethodField()
    well_status_obj = serializers.SerializerMethodField()

    class Meta:
        model = models.WaterSupplyWell
        fields = ['id', 'watersupply_id', 'well_type', 'well_height', 'well_filter_height', 'well_water_supply', 'well_nirostatic', 'well_watar_quality', 'well_water_quality_check', 
        'well_status', 'well_status_reason', 'is_active', 'well_nirodynamic', 'well_type_obj', 'well_watar_quality_obj', 'well_water_quality_check_obj', 'well_status_obj']

    def get_well_type_obj(self, obj):
            customer_account_query = models.WaterSupplyOptionValue.objects.filter(id=int(obj.well_type))
            serializer = WaterSupplyOptionValueSerializer(customer_account_query, many=True)
            return serializer.data    
    
    def get_well_watar_quality_obj(self, obj):
            customer_account_query = models.WaterSupplyOptionValue.objects.filter(id=int(obj.well_watar_quality))
            serializer = WaterSupplyOptionValueSerializer(customer_account_query, many=True)
            return serializer.data   
    def get_well_water_quality_check_obj(self, obj):
            customer_account_query = models.WaterSupplyOptionValue.objects.filter(id=int(obj.well_water_quality_check))
            serializer = WaterSupplyOptionValueSerializer(customer_account_query, many=True)
            return serializer.data   
    def get_well_status_obj(self, obj):
            customer_account_query = models.WaterSupplyOptionValue.objects.filter(id=int(obj.well_status))
            serializer = WaterSupplyOptionValueSerializer(customer_account_query, many=True)
            return serializer.data   
        
class WaterSupplyPipeSerializer(serializers.ModelSerializer):

    source_type_of_water_obj = serializers.SerializerMethodField()
    pool_filter_obj = serializers.SerializerMethodField()
    water_quality_check_obj = serializers.SerializerMethodField()
    status_obj = serializers.SerializerMethodField()
    
    class Meta:
        model = models.WaterSupplyPipe
        fields = ['id', 'watersupply_id', 'is_active', 'source_type_of_water', 'abilty_of_produce_water', 'underground_pool_storage', 'pool_air', 'pool_filter', 'number_of_link', 
        'water_quality_check', 'status', 'status_no_reason', 'source_type_of_water_obj', 'pool_filter_obj', 'water_quality_check_obj', 'status_obj']
    
    def get_source_type_of_water_obj(self, obj):
        customer_account_query = models.WaterSupplyOptionValue.objects.filter(id=int(obj.source_type_of_water))
        serializer = WaterSupplyOptionValueSerializer(customer_account_query, many=True)
        return serializer.data  

    def get_pool_filter_obj(self, obj):
        customer_account_query = models.WaterSupplyOptionValue.objects.filter(id=int(obj.pool_filter))
        serializer = WaterSupplyOptionValueSerializer(customer_account_query, many=True)
        return serializer.data  

    def get_water_quality_check_obj(self, obj):
        customer_account_query = models.WaterSupplyOptionValue.objects.filter(id=int(obj.water_quality_check))
        serializer = WaterSupplyOptionValueSerializer(customer_account_query, many=True)
        return serializer.data  

    def get_status_obj(self, obj):
        customer_account_query = models.WaterSupplyOptionValue.objects.filter(id=int(obj.status))
        serializer = WaterSupplyOptionValueSerializer(customer_account_query, many=True)
        return serializer.data   
    
class WaterSupplyKioskSerializer(serializers.ModelSerializer):

    source_type_of_water_obj = serializers.SerializerMethodField()
    filter_system_obj = serializers.SerializerMethodField()
    status_obj = serializers.SerializerMethodField()
    water_quality_checking_obj = serializers.SerializerMethodField()

    class Meta:
        model = models.WaterSupplyKiosk
        fields = ['watersupply_id', 'is_active', 'source_type_of_water', 'abilty_of_produce_water', 'filter_system', 'water_quality_checking', 'status', 'status_no_reason', 'source_type_of_water_obj', 'filter_system_obj', 'status_obj', 'water_quality_checking_obj']

    def get_source_type_of_water_obj(self, obj):
        customer_account_query = models.WaterSupplyOptionValue.objects.filter(id=int(obj.source_type_of_water))
        serializer = WaterSupplyOptionValueSerializer(customer_account_query, many=True)
        return serializer.data 
    def get_filter_system_obj(self, obj):
        customer_account_query = models.WaterSupplyOptionValue.objects.filter(id=int(obj.filter_system))
        serializer = WaterSupplyOptionValueSerializer(customer_account_query, many=True)
        return serializer.data 
    def get_water_quality_checking_obj(self, obj):
        customer_account_query = models.WaterSupplyOptionValue.objects.filter(id=int(obj.water_quality_checking))
        serializer = WaterSupplyOptionValueSerializer(customer_account_query, many=True)
        return serializer.data 
    def get_status_obj(self, obj):
        customer_account_query = models.WaterSupplyOptionValue.objects.filter(id=int(obj.status))
        serializer = WaterSupplyOptionValueSerializer(customer_account_query, many=True)
        return serializer.data 

class WaterSupplyCommuniryPondSerializer(serializers.ModelSerializer):

    pool_filter_obj = serializers.SerializerMethodField()
    type_of_pond_obj = serializers.SerializerMethodField()
    is_summer_has_water_obj = serializers.SerializerMethodField()
    status_obj = serializers.SerializerMethodField()

    class Meta:
        model = models.WaterSupplyCommunityPond
        fields = ['watersupply_id', 'is_active', 'width', 'length', 'height', 'pool_filter', 
        'type_of_pond', 'is_summer_has_water', 'status', 'status_no_reason', 'pool_filter_obj', 'type_of_pond_obj', 'is_summer_has_water_obj', 'status_obj']
    
    def get_type_of_pond_obj(self, obj):
        customer_account_query = models.WaterSupplyOptionValue.objects.filter(id=int(obj.type_of_pond))
        serializer = WaterSupplyOptionValueSerializer(customer_account_query, many=True)
        return serializer.data  
    def get_pool_filter_obj(self, obj):
        customer_account_query = models.WaterSupplyOptionValue.objects.filter(id=int(obj.pool_filter))
        serializer = WaterSupplyOptionValueSerializer(customer_account_query, many=True)
        return serializer.data  
    def get_is_summer_has_water_obj(self, obj):
        customer_account_query = models.WaterSupplyOptionValue.objects.filter(id=int(obj.is_summer_has_water))
        serializer = WaterSupplyOptionValueSerializer(customer_account_query, many=True)
        return serializer.data  
    def get_status_obj(self, obj):
        customer_account_query = models.WaterSupplyOptionValue.objects.filter(id=int(obj.status))
        serializer = WaterSupplyOptionValueSerializer(customer_account_query, many=True)
        return serializer.data  

class WaterSupplyRainWaterHarvestingSerializer(serializers.ModelSerializer):

    type_of_using_obj = serializers.SerializerMethodField()
    status_obj = serializers.SerializerMethodField()

    class Meta:
        model = models.WaterSupplyRainWaterHarvesting
        fields = ['watersupply_id', 'is_active', 'type_of_using', 'capacity_35m3', 'capacity_4m3', 'capacity_of_rain_water_harvesting', 'status', 'status_no_reason', 
        'type_of_using_obj', 'status_obj']

    def get_type_of_using_obj(self, obj):
        customer_account_query = models.WaterSupplyOptionValue.objects.filter(id=int(obj.type_of_using))
        serializer = WaterSupplyOptionValueSerializer(customer_account_query, many=True)
        return serializer.data  
    def get_status_obj(self, obj):
        customer_account_query = models.WaterSupplyOptionValue.objects.filter(id=int(obj.status))
        serializer = WaterSupplyOptionValueSerializer(customer_account_query, many=True)
        return serializer.data  

class WaterSupplySerializer(serializers.HyperlinkedModelSerializer):
    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)
    water_supply_type_id = WaterSupplyTypeSerializer(many=False, read_only=True)
    province_id = ProvinceSerializer_v2(many=False, read_only=True)
    district_id = DistrictSerializer_v2(many=False, read_only=True)
    commune_id = CommuneSerializer_v2(many=False, read_only=True)
    village_id = VillageSerializer_v2(many=False, read_only=True)
    watersupplywell_watersupply = WaterSupplyWellSerializer(many=True, read_only = True)
    watersupplypipe_watersupply = WaterSupplyPipeSerializer(many=True, read_only=True)
    watersupplyKiosk_watersupply = WaterSupplyKioskSerializer(many=True, read_only=True)
    watersupplyCommunityPond_watersupply = WaterSupplyCommuniryPondSerializer(many=True, read_only=True)
    watersupplyRainWaterHarvesting_watersupply = WaterSupplyRainWaterHarvestingSerializer(many=True, read_only=True)

    class Meta:
        model = models.WaterSupply
        fields = ('id', 'water_supply_type_id', 'province_id', 'district_id', 'created_by', 'updated_by', 'created_at', 'updated_at', 'commune_id', 'village_id', 'water_supply_code', 'total_family', 'utm_x', 'utm_y', 'is_risk_enviroment_area', 'construction_date', 'source_budget', 'constructed_by', 
        'management_type', 'managed_by', 'beneficiary_total_people', 'beneficiary_total_women', 'beneficiary_total_family', 'beneficiary_total_family_poor_1', 'beneficiary_total_family_poor_2', 'beneficiary_total_family_vulnerable', 'beneficiary_total_family_indigenous', 
        'watersupplywell_watersupply', 'watersupplypipe_watersupply', 'watersupplyKiosk_watersupply', 'watersupplyCommunityPond_watersupply', 'watersupplyRainWaterHarvesting_watersupply')
        
class WaterSupplySerializer_v2(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(default=datetime.now())
    class Meta:
        model = models.WaterSupply
        fields = ['id','water_supply_type_id', 'province_id', 'district_id', 'created_by', 'updated_by', 'created_at', 'updated_at', 'is_active', 'commune_id', 'village_id', 'water_supply_code', 'total_family', 'utm_x', 'utm_y', 'is_risk_enviroment_area', 'construction_date', 'source_budget', 'constructed_by', 
        'management_type', 'managed_by', 'beneficiary_total_people', 'beneficiary_total_women', 'beneficiary_total_family', 'beneficiary_total_family_poor_1', 'beneficiary_total_family_poor_2', 'beneficiary_total_family_vulnerable', 'beneficiary_total_family_indigenous']

