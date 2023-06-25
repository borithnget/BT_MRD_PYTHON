from dataclasses import field, fields
from datetime import datetime
from email.policy import default
from pyexpat import model
from time import timezone
from rest_framework import serializers
from django.contrib.auth import authenticate

from mdrapp import models
import myapi
from .models import Hero
from mdrapp.models import Commune, User, Province, District, Village, WaterSupplyType, WaterSupplyOption, WaterSupplyOptionValue, WaterSupply, Status, WaterSupplyWorkFlow, WaterSupplyWellOptionValue, UserDetail, WaterSupplyQRCode, WaterSupplyHistory, WaterQualityCheckedParamater, WaterSupplyQuanlityCheckParamater, WaterSupplyPipePrivate, WaterSupplyPipePrivateOptionValue, WaterSupplyAirWater, WaterSupplyAirWaterOptionValue, Country
from rest_framework import exceptions

class HeroSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Hero
        fields = ('id', 'name', 'alias')
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_data_entry', 'is_head_department', 'is_provincial_department_head', 'is_data_verifier_1', 'is_data_verifier_2', 'is_partner', 'data_entry_province_id', 'provincial_department_head_province_id', 'first_name', 'last_name', 'is_staff')
    

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ('username', 'email', 'password', 'is_data_entry', 'is_head_department', 'is_provincial_department_head', 'is_data_verifier_1', 'is_data_verifier_2', 'is_partner', 'data_entry_province_id', 'provincial_department_head_province_id', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'], 
            validated_data['email'], 
            validated_data['password'], 
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            is_data_entry=validated_data['is_data_entry'],
            is_head_department=validated_data['is_head_department'],
            is_provincial_department_head=validated_data['is_provincial_department_head'],
            is_data_verifier_1=validated_data['is_data_verifier_1'],
            is_data_verifier_2=validated_data['is_data_verifier_2'],
            is_partner=validated_data['is_partner'],
            data_entry_province_id = validated_data['data_entry_province_id'],
            provincial_department_head_province_id= validated_data['provincial_department_head_province_id']
            )
        # user = User.objects.create_user(
        #     self.cleaned_data['username'], 
        #     email=self.cleaned_data['email'], 
        #     password=self.cleaned_data['password'], 
        #     is_data_entry=self.cleaned_data['is_data_entry']
        #     )
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Incorrect Credentials Passed.')

class UserRoleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetail
        fields = ('id', 'data_entry_province_id', 'provincial_department_head_province_id')

# class ChangePasswordSerializer(serializers.Serializer):
#     old_password = serializers.CharField(required=True)
#     new_password = serializers.CharField(required=True)

class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True) #, validators=[validate_password]
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

class UserDeactivateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id', 'is_active')
    
class VillageSerializer(serializers.HyperlinkedModelSerializer):
    #commune_id = CommuneSerializer(many=False, read_only=True)
    class Meta:
        model = Village
        fields = ('id' ,'code_en', 'code_kh', 'name_en', 'name_kh', 'description' , "commune_id")

class CommuneSerializer(serializers.HyperlinkedModelSerializer):
    #commnuevillage = VillageSerializer(many=True, read_only=True)
    class Meta:
        model = Commune
        fields = ('id' ,'code_en', 'code_kh', 'name_en', 'name_kh', 'description' , "district_id") #'commnuevillage',

class DistrictSerializer(serializers.HyperlinkedModelSerializer):
    #districtcommnue = CommuneSerializer(many=True, read_only=True)
    class Meta:
        model = District
        fields = ('id' ,'code_en', 'code_kh', 'name_en', 'name_kh', 'description' , "province_id") #'districtcommnue',
  
class ProvinceSerializer(serializers.HyperlinkedModelSerializer):
    #provincedistrict = DistrictSerializer(many= True, read_only=True)
    total_district = serializers.SerializerMethodField(read_only=True)
    
    def get_total_district(self, language):
        return language.provincedistrict.count()

    
    class Meta:
        model = Province
        # fields = '__all__'
        fields = ('id' ,'code_en', 'code_kh', 'name_en', 'name_kh', 'total_population', 'description', 'coordinate_border', 'coordinate_center',  'total_district' ) #,'provincedistrict'

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

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'
        
class UserDetailSerializer(serializers.ModelSerializer):
    data_entry_province_id = ProvinceSerializer_v2(many=False)
    provincial_department_head_province_id = ProvinceSerializer_v2(many=False)
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined', 'is_head_department', 'is_data_entry', 'is_provincial_department_head', 'is_data_verifier_1', 'is_data_verifier_2', 'is_partner', 'data_entry_province_id', 'provincial_department_head_province_id')
        
        
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
        fields=('id', 'name_en', 'name_kh', 'data_type', 'is_active', 'watersupplyoption_value', 'field_name', 'is_required')
        
class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ('id', 'status_name', 'status_name_kh', 'is_active')
        
class WaterSupplyTypeOptionSerializer(serializers.ModelSerializer):
    
    #watersupplytypeoption_option = WaterSupplyOptionSerializer(many=True)
    water_supply_type_id = WaterSupplyTypeSerializer(many=False)
    water_supply_option_id = WaterSupplyOptionSerializer(read_only=True, many=False)
    
    class Meta:
        model = models.WaterSupplyTypeOption
        # fields = '__all__'
        fields = ('id', 'ordering', 'water_supply_type_id', 'water_supply_option_id')

class WaterSupplyWellOptionValueSerializer(serializers.ModelSerializer):
    # option_id = WaterSupplyOptionSerializer(many=False)
    #value_id = WaterSupplyOptionValueSerializer(many=False)
    watersupplywelloptionvalue_value = WaterSupplyOptionValueSerializer(many=True, read_only=True)
    value_obj = serializers.SerializerMethodField()
    class Meta:
        model = models.WaterSupplyWellOptionValue
        fields = ('id', 'water_supply_well_id', 'option_id', 'value_id', 'is_active', 'watersupplywelloptionvalue_value', 'value_obj')

    def get_value_obj(self, obj):
        customer_account_query = models.WaterSupplyOptionValue.objects.filter(id=obj.value_id.id)
        serializer = WaterSupplyOptionValueSerializer(customer_account_query, many=True)
        return serializer.data   

class WaterSupplyWellSerializer(serializers.ModelSerializer):

    well_type_obj = serializers.SerializerMethodField()
    well_watar_quality_obj = serializers.SerializerMethodField()
    well_water_quality_check_obj = serializers.SerializerMethodField()
    well_status_obj = serializers.SerializerMethodField()
    watersupplywelloptionvalue_watersupplywell = WaterSupplyWellOptionValueSerializer(many=True, read_only=True)

    class Meta:
        model = models.WaterSupplyWell
        fields = ['id', 'watersupply_id', 'well_type', 'well_height', 'well_filter_height', 'well_water_supply', 'well_nirostatic', 'well_watar_quality', 'well_water_quality_check', 
        'well_status', 'well_status_reason', 'is_active', 'well_nirodynamic', 'well_watar_quality_obj', 'well_water_quality_check_obj', 'well_status_obj', 'watersupplywelloptionvalue_watersupplywell', 'well_type_obj']

    def get_well_type_obj(self, obj):
            customer_account_query = models.WaterSupplyWellOptionValue.objects.filter(water_supply_well_id=int(obj.id))
            serializer = WaterSupplyWellOptionValueSerializer(customer_account_query, many=True)
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
        
class WaterSupplyPipeOptionValueSerializer(serializers.ModelSerializer):

    value_obj = serializers.SerializerMethodField()

    class Meta:
        model = models.WaterSupplyPipeOptionValue
        fields = ('id', 'water_supply_pipe_id', 'option_id', 'value_id', 'is_active', 'value_obj')

    def get_value_obj(self, obj):
        customer_account_query = models.WaterSupplyOptionValue.objects.filter(id=obj.value_id.id)
        serializer = WaterSupplyOptionValueSerializer(customer_account_query, many=True)
        return serializer.data  

class WaterSupplyPipeSerializer(serializers.ModelSerializer):

    # source_type_of_water_obj = serializers.SerializerMethodField()
    pool_filter_obj = serializers.SerializerMethodField()
    water_quality_check_obj = serializers.SerializerMethodField()
    status_obj = serializers.SerializerMethodField()
    watersupplypipeoptionvalue_watersupplypipe = WaterSupplyPipeOptionValueSerializer(many=True, read_only=True)
    
    class Meta:
        model = models.WaterSupplyPipe
        fields = ['id', 'watersupply_id', 'is_active', 'source_type_of_water', 'abilty_of_produce_water', 'underground_pool_storage', 'pool_air', 'pool_filter', 'number_of_link', 
        'water_quality_check', 'status', 'status_no_reason', 'pool_filter_obj', 'water_quality_check_obj', 'status_obj' , 'watersupplypipeoptionvalue_watersupplypipe', 'pipe_length', 'area_covering']
    
    # def get_source_type_of_water_obj(self, obj):
    #     customer_account_query = models.WaterSupplyOptionValue.objects.filter(id=int(obj.source_type_of_water))
    #     serializer = WaterSupplyOptionValueSerializer(customer_account_query, many=True)
    #     return serializer.data  

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
    
class WaterSupplyKioskOptionValueSerializer(serializers.ModelSerializer):
    value_obj = serializers.SerializerMethodField()

    class Meta:
        model = models.WaterSupplyKioskOptionValue
        fields = ('id', 'water_supply_kiosk_id', 'option_id', 'value_id', 'is_active', 'value_obj')

    def get_value_obj(self, obj):
        customer_account_query = models.WaterSupplyOptionValue.objects.filter(id=obj.value_id.id)
        serializer = WaterSupplyOptionValueSerializer(customer_account_query, many=True)
        return serializer.data  

class WaterSupplyKioskSerializer(serializers.ModelSerializer):

    # source_type_of_water_obj = serializers.SerializerMethodField()
    filter_system_obj = serializers.SerializerMethodField()
    status_obj = serializers.SerializerMethodField()
    water_quality_checking_obj = serializers.SerializerMethodField()
    watersupplykioskoptionvalue_watersupplykiosk = WaterSupplyKioskOptionValueSerializer(many=True, read_only=True)

    class Meta:
        model = models.WaterSupplyKiosk
        fields = ['id', 'watersupply_id', 'is_active', 'source_type_of_water', 'abilty_of_produce_water', 'filter_system', 'water_quality_checking', 'status', 'status_no_reason', 'filter_system_obj', 'status_obj', 'water_quality_checking_obj', 'watersupplykioskoptionvalue_watersupplykiosk']

    # def get_source_type_of_water_obj(self, obj):
    #     customer_account_query = models.WaterSupplyOptionValue.objects.filter(id=int(obj.source_type_of_water))
    #     serializer = WaterSupplyOptionValueSerializer(customer_account_query, many=True)
    #     return serializer.data 
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
    capacity_of_rain_water_harvesting_obj = serializers.SerializerMethodField()
    water_quality_checking_obj = serializers.SerializerMethodField()

    class Meta:
        model = models.WaterSupplyRainWaterHarvesting
        fields = ['watersupply_id', 'is_active', 'type_of_using', 'capacity_35m3', 'capacity_4m3', 'capacity_of_rain_water_harvesting', 'status', 'status_no_reason', 
        'type_of_using_obj', 'status_obj', 'capacity_of_rain_water_harvesting_obj', 'water_quality_checking', 'water_quality_checking_obj']

    def get_type_of_using_obj(self, obj):
        customer_account_query = models.WaterSupplyOptionValue.objects.filter(id=int(obj.type_of_using))
        serializer = WaterSupplyOptionValueSerializer(customer_account_query, many=True)
        return serializer.data  
    def get_status_obj(self, obj):
        customer_account_query = models.WaterSupplyOptionValue.objects.filter(id=int(obj.status))
        serializer = WaterSupplyOptionValueSerializer(customer_account_query, many=True)
        return serializer.data

    def get_capacity_of_rain_water_harvesting_obj(self, obj):
        customer_account_query = models.WaterSupplyOptionValue.objects.filter(id=int(obj.capacity_of_rain_water_harvesting))
        serializer = WaterSupplyOptionValueSerializer(customer_account_query, many=True)
        return serializer.data  
    
    def get_water_quality_checking_obj(self, obj):
        customer_account_query = models.WaterSupplyOptionValue.objects.filter(id=int(obj.water_quality_checking))
        serializer = WaterSupplyOptionValueSerializer(customer_account_query, many=True)
        return serializer.data  

class WaterSupplyPipePrivateOptionValueSerializer(serializers.ModelSerializer):

    value_obj = serializers.SerializerMethodField()

    class Meta:
        model = WaterSupplyPipePrivateOptionValue
        fields = ['id', 'water_supply_pipe_id', 'option_id', 'value_id', 'is_active', 'value_obj']

    def get_value_obj(self, obj):
        customer_account_query = models.WaterSupplyOptionValue.objects.filter(id=obj.value_id.id)
        serializer = WaterSupplyOptionValueSerializer(customer_account_query, many=True)
        return serializer.data

class WaterSupplyPipePrivateSerializer(serializers.ModelSerializer):

    pool_filter_obj = serializers.SerializerMethodField()
    water_quality_check_obj = serializers.SerializerMethodField()
    status_obj = serializers.SerializerMethodField()
    watersupplypipeprivateoptionvalue_watersupplypipewater = WaterSupplyPipePrivateOptionValueSerializer(many=True, read_only=True)
    is_has_license_obj = serializers.SerializerMethodField()

    class Meta:
        model = WaterSupplyPipePrivate
        fields = ['id', 'watersupply_id', 'is_active', 'source_type_of_water', 'abilty_of_produce_water', 'underground_pool_storage', 'pool_air', 'pool_filter', 'number_of_link', 'water_quality_check', 'status', 'status_no_reason', 'pipe_length', 'area_covering', 'is_has_license', 'license_registered_date', 'license_expired_date', 
                  'pool_filter_obj', 'water_quality_check_obj', 'status_obj', 'is_has_license_obj', 'watersupplypipeprivateoptionvalue_watersupplypipewater']
        
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
    
    def get_is_has_license_obj(self, obj):
        customer_account_query = models.WaterSupplyOptionValue.objects.filter(id=int(obj.is_has_license))
        serializer = WaterSupplyOptionValueSerializer(customer_account_query, many=True)
        return serializer.data 

class WaterSupplyAirWaterOptionValueSerializer(serializers.ModelSerializer):

    value_obj = serializers.SerializerMethodField()

    class Meta:
        model = WaterSupplyAirWaterOptionValue
        fields = ['id', 'water_supply_airwater_id', 'option_id', 'value_id', 'is_active', 'value_obj']

    def get_value_obj(self, obj):
        customer_account_query = models.WaterSupplyOptionValue.objects.filter(id=obj.value_id.id)
        serializer = WaterSupplyOptionValueSerializer(customer_account_query, many=True)
        return serializer.data

class WaterSupplyAirWaterSerializer(serializers.ModelSerializer):

    filter_system_obj = serializers.SerializerMethodField()
    status_obj = serializers.SerializerMethodField()
    water_quality_checking_obj = serializers.SerializerMethodField()
    watersupplyairwateroptionvalue_watersupplykioskwater = WaterSupplyAirWaterOptionValueSerializer(many=True, read_only=True)
    
    class Meta:
        model = WaterSupplyAirWater
        fields = ['id', 'watersupply_id', 'is_active', 'source_type_of_water', 'abilty_of_produce_water', 'filter_system', 'water_quality_checking', 'status', 'status_no_reason', 'filter_system_obj', 'status_obj', 'water_quality_checking_obj', 'watersupplyairwateroptionvalue_watersupplykioskwater']

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

class WaterSupplyWorkflowSerializer_v1(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(default=datetime.now(), format="%Y-%m-%d %H:%M:%S")
    status_id = StatusSerializer(many=False, read_only=True)
    user_id = UserSerializer(many=False, read_only=True)
    # watersupply_id = WaterSupplySerializer(many=False, read_only=True)

    class Meta:
        model = WaterSupplyWorkFlow
        fields = ('id', 'watersupply_id', 'status_id', 'user_id', 'created_at', 'remark')

class WaterSupplyQRCodeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = WaterSupplyQRCode
        fields = ('id', 'watersupply_id', 'qr_code_image_name')

class WaterQuanlityCheckParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterQualityCheckedParamater
        fields = '__all__'

class WaterSupplyQuanlityCheckParamaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterSupplyQuanlityCheckParamater
        fields = ('id', 'water_supply_id', 'water_quanlity_check_parameter_id', 'value', 'is_active')

class WaterSupplyQuanlityCheckParamaterSerializer_v2(serializers.ModelSerializer):
    water_quanlity_check_parameter_id = WaterQuanlityCheckParameterSerializer(many=False, read_only=True)
    class Meta:
        model = WaterSupplyQuanlityCheckParamater
        fields = ('id', 'water_supply_id', 'water_quanlity_check_parameter_id', 'value')

class WaterSupplySerializer(serializers.HyperlinkedModelSerializer):
    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)
    water_supply_type_id = WaterSupplyTypeSerializer(many=False, read_only=True)
    province_id = ProvinceSerializer_v2(many=False, read_only=True)
    district_id = DistrictSerializer_v2(many=False, read_only=True)
    commune_id = CommuneSerializer_v2(many=False, read_only=True)
    village_id = VillageSerializer_v2(many=False, read_only=True)
    #watersupplywell_watersupply = WaterSupplyWellSerializer(many=True, read_only = True)
    #watersupplypipe_watersupply = WaterSupplyPipeSerializer(many=True, read_only=True)
    # watersupplyKiosk_watersupply = WaterSupplyKioskSerializer(many=True, read_only=True)
    #watersupplyCommunityPond_watersupply = WaterSupplyCommuniryPondSerializer(many=True, read_only=True)
    # watersupplyRainWaterHarvesting_watersupply = WaterSupplyRainWaterHarvestingSerializer(many=True, read_only=True)
    # watersupplypipeprivate_watersupply = WaterSupplyPipePrivateSerializer(many=True, read_only=True)
    # watersupplyairwater_watersupply = WaterSupplyAirWaterSerializer(many=True, read_only=True)
    watersupplyworkflow_watersupply = WaterSupplyWorkflowSerializer_v1(many=True, read_only=True)
    main_status = StatusSerializer(many=False, read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    crated_at_1 = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    watersupplyqrcode_watersupply = WaterSupplyQRCodeSerializer(many=True,read_only=True)
    watersupplywell_watersupply = serializers.SerializerMethodField()
    watersupplyairwater_watersupply = serializers.SerializerMethodField()
    watersupplypipe_watersupply = serializers.SerializerMethodField()
    watersupplyKiosk_watersupply = serializers.SerializerMethodField()
    watersupplyCommunityPond_watersupply = serializers.SerializerMethodField()
    watersupplyRainWaterHarvesting_watersupply = serializers.SerializerMethodField()
    watersupplypipeprivate_watersupply = serializers.SerializerMethodField()

    wqc_param1_obj = serializers.SerializerMethodField()
    wqc_param2_obj = serializers.SerializerMethodField()
    wqc_param3_obj = serializers.SerializerMethodField()
    wqc_param4_obj = serializers.SerializerMethodField()
    wqc_param5_obj = serializers.SerializerMethodField()
    wqc_param6_obj = serializers.SerializerMethodField()
    wqc_param7_obj = serializers.SerializerMethodField()
    wqc_param8_obj = serializers.SerializerMethodField()
    wqc_param9_obj = serializers.SerializerMethodField()
    wqc_param10_obj = serializers.SerializerMethodField()
    wqc_param11_obj = serializers.SerializerMethodField()
    wqc_param12_obj = serializers.SerializerMethodField()
    wqc_param13_obj = serializers.SerializerMethodField()
    wqc_param14_obj = serializers.SerializerMethodField()
    wqc_param15_obj = serializers.SerializerMethodField()
    wqc_param16_obj = serializers.SerializerMethodField()

    class Meta:
        model = models.WaterSupply
        fields = ('id', 'water_supply_type_id', 'province_id', 'district_id', 'created_by', 'updated_by', 'created_at', 'crated_at_1', 'updated_at', 'commune_id', 'village_id', 'water_supply_code', 'total_family', 'utm_x', 'utm_y', 'is_risk_enviroment_area', 'construction_date', 'source_budget', 'constructed_by', 
        'management_type', 'managed_by', 'beneficiary_total_people', 'beneficiary_total_women', 'beneficiary_total_family', 'beneficiary_total_family_poor_1', 'beneficiary_total_family_poor_2', 'beneficiary_total_family_vulnerable', 'beneficiary_total_family_indigenous', 
        'watersupplywell_watersupply', 'watersupplypipe_watersupply', 'watersupplyKiosk_watersupply', 'watersupplyCommunityPond_watersupply', 'watersupplyRainWaterHarvesting_watersupply', 'watersupplypipeprivate_watersupply', 'watersupplyairwater_watersupply', 'watersupplyworkflow_watersupply', 'main_status', 'watersupplyqrcode_watersupply', 
        'wqc_param1_obj', 'wqc_param2_obj', 'wqc_param3_obj', 'wqc_param4_obj', 'wqc_param5_obj', 'wqc_param6_obj', 'wqc_param7_obj', 'wqc_param8_obj', 'wqc_param9_obj', 'wqc_param10_obj', 'wqc_param11_obj', 'wqc_param12_obj', 'wqc_param13_obj', 'wqc_param14_obj', 'wqc_param1_obj', 'wqc_param15_obj', 'wqc_param16_obj',
        'is_water_quality_check', 'map_unit', 'decimal_degress_lat', 'decimal_degress_lng', 'mds_x_degress', 'mds_x_minute', 'mds_x_second', 'mds_y_degress', 'mds_y_minute', 'mds_y_second')
    
    def get_watersupplywell_watersupply(self, instance):
        watersupplywell_watersupplys = instance.watersupplywell_watersupply.all().order_by('-id')
        return WaterSupplyWellSerializer(watersupplywell_watersupplys, many=True).data
    
    def get_watersupplyairwater_watersupply(self, instance):
        watersupplywell_watersupplys = instance.watersupplyairwater_watersupply.all().order_by('-id')
        return WaterSupplyAirWaterSerializer(watersupplywell_watersupplys, many=True).data
    
    def get_watersupplypipe_watersupply(self, instance):
        watersupplywell_watersupplys = instance.watersupplypipe_watersupply.all().order_by('-id')
        return WaterSupplyPipeSerializer(watersupplywell_watersupplys, many=True).data
    
    def get_watersupplyKiosk_watersupply(self, instance):
        watersupplywell_watersupplys = instance.watersupplyKiosk_watersupply.all().order_by('-id')
        return WaterSupplyKioskSerializer(watersupplywell_watersupplys, many=True).data
    
    def get_watersupplyCommunityPond_watersupply(self, instance):
        watersupplywell_watersupplys = instance.watersupplyCommunityPond_watersupply.all().order_by('-id')
        return WaterSupplyCommuniryPondSerializer(watersupplywell_watersupplys, many=True).data
    
    def get_watersupplyRainWaterHarvesting_watersupply(self, instance):
        watersupplywell_watersupplys = instance.watersupplyRainWaterHarvesting_watersupply.all().order_by('-id')
        return WaterSupplyRainWaterHarvestingSerializer(watersupplywell_watersupplys, many=True).data
    
    def get_watersupplypipeprivate_watersupply(self, instance):
        watersupplywell_watersupplys = instance.watersupplypipeprivate_watersupply.all().order_by('-id')
        return WaterSupplyPipePrivateSerializer(watersupplywell_watersupplys, many=True).data

    
    def get_wqc_param1_obj(self, instance):
        objs = models.WaterSupplyQuanlityCheckParamater.objects.order_by('-id').filter(water_supply_id=instance.id).filter(water_quanlity_check_parameter_id=1)
        return WaterSupplyQuanlityCheckParamaterSerializer_v2(objs, many=True).data
    def get_wqc_param2_obj(self, instance):
        objs = models.WaterSupplyQuanlityCheckParamater.objects.order_by('-id').filter(water_supply_id=instance.id).filter(water_quanlity_check_parameter_id=2)
        return WaterSupplyQuanlityCheckParamaterSerializer_v2(objs, many=True).data
    def get_wqc_param3_obj(self, instance):
        objs = models.WaterSupplyQuanlityCheckParamater.objects.order_by('-id').filter(water_supply_id=instance.id).filter(water_quanlity_check_parameter_id=3)
        return WaterSupplyQuanlityCheckParamaterSerializer_v2(objs, many=True).data
    def get_wqc_param4_obj(self, instance):
        objs = models.WaterSupplyQuanlityCheckParamater.objects.order_by('-id').filter(water_supply_id=instance.id).filter(water_quanlity_check_parameter_id=4)
        return WaterSupplyQuanlityCheckParamaterSerializer_v2(objs, many=True).data
    def get_wqc_param5_obj(self, instance):
        objs = models.WaterSupplyQuanlityCheckParamater.objects.order_by('-id').filter(water_supply_id=instance.id).filter(water_quanlity_check_parameter_id=5)
        return WaterSupplyQuanlityCheckParamaterSerializer_v2(objs, many=True).data
    def get_wqc_param6_obj(self, instance):
        objs = models.WaterSupplyQuanlityCheckParamater.objects.order_by('-id').filter(water_supply_id=instance.id).filter(water_quanlity_check_parameter_id=6)
        return WaterSupplyQuanlityCheckParamaterSerializer_v2(objs, many=True).data
    def get_wqc_param7_obj(self, instance):
        objs = models.WaterSupplyQuanlityCheckParamater.objects.order_by('-id').filter(water_supply_id=instance.id).filter(water_quanlity_check_parameter_id=7)
        return WaterSupplyQuanlityCheckParamaterSerializer_v2(objs, many=True).data
    def get_wqc_param8_obj(self, instance):
        objs = models.WaterSupplyQuanlityCheckParamater.objects.order_by('-id').filter(water_supply_id=instance.id).filter(water_quanlity_check_parameter_id=8)
        return WaterSupplyQuanlityCheckParamaterSerializer_v2(objs, many=True).data
    def get_wqc_param9_obj(self, instance):
        objs = models.WaterSupplyQuanlityCheckParamater.objects.order_by('-id').filter(water_supply_id=instance.id).filter(water_quanlity_check_parameter_id=9)
        return WaterSupplyQuanlityCheckParamaterSerializer_v2(objs, many=True).data
    def get_wqc_param10_obj(self, instance):
        objs = models.WaterSupplyQuanlityCheckParamater.objects.order_by('-id').filter(water_supply_id=instance.id).filter(water_quanlity_check_parameter_id=10)
        return WaterSupplyQuanlityCheckParamaterSerializer_v2(objs, many=True).data
    def get_wqc_param11_obj(self, instance):
        objs = models.WaterSupplyQuanlityCheckParamater.objects.order_by('-id').filter(water_supply_id=instance.id).filter(water_quanlity_check_parameter_id=11)
        return WaterSupplyQuanlityCheckParamaterSerializer_v2(objs, many=True).data
    def get_wqc_param12_obj(self, instance):
        objs = models.WaterSupplyQuanlityCheckParamater.objects.order_by('-id').filter(water_supply_id=instance.id).filter(water_quanlity_check_parameter_id=12)
        return WaterSupplyQuanlityCheckParamaterSerializer_v2(objs, many=True).data
    def get_wqc_param13_obj(self, instance):
        objs = models.WaterSupplyQuanlityCheckParamater.objects.order_by('-id').filter(water_supply_id=instance.id).filter(water_quanlity_check_parameter_id=13)
        return WaterSupplyQuanlityCheckParamaterSerializer_v2(objs, many=True).data
    def get_wqc_param14_obj(self, instance):
        objs = models.WaterSupplyQuanlityCheckParamater.objects.order_by('-id').filter(water_supply_id=instance.id).filter(water_quanlity_check_parameter_id=14)
        return WaterSupplyQuanlityCheckParamaterSerializer_v2(objs, many=True).data
    def get_wqc_param15_obj(self, instance):
        objs = models.WaterSupplyQuanlityCheckParamater.objects.order_by('-id').filter(water_supply_id=instance.id).filter(water_quanlity_check_parameter_id=15)
        return WaterSupplyQuanlityCheckParamaterSerializer_v2(objs, many=True).data
    def get_wqc_param16_obj(self, instance):
        objs = models.WaterSupplyQuanlityCheckParamater.objects.order_by('-id').filter(water_supply_id=instance.id).filter(water_quanlity_check_parameter_id=16)
        return WaterSupplyQuanlityCheckParamaterSerializer_v2(objs, many=True).data

class WaterSupplySerializer_v2(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(default=datetime.now())
    crated_at_1 = serializers.DateTimeField(default=datetime.now())
    class Meta:
        model = models.WaterSupply
        fields = ['id','water_supply_type_id', 'province_id', 'district_id', 'created_by', 'updated_by', 'created_at', 'crated_at_1', 'updated_at', 'is_active', 'commune_id', 'village_id', 'water_supply_code', 'total_family', 'utm_x', 'utm_y', 'is_risk_enviroment_area', 'construction_date', 'source_budget', 'constructed_by', 
        'management_type', 'managed_by', 'beneficiary_total_people', 'beneficiary_total_women', 'beneficiary_total_family', 'beneficiary_total_family_poor_1', 'beneficiary_total_family_poor_2', 'beneficiary_total_family_vulnerable', 'beneficiary_total_family_indigenous', 'main_status', 'is_water_quality_check',
        'map_unit', 'decimal_degress_lat', 'decimal_degress_lng', 'mds_x_degress', 'mds_x_minute', 'mds_x_second', 'mds_y_degress', 'mds_y_minute', 'mds_y_second', 'crated_at_1']

class WaterSupplyHistortSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(default=datetime.now())
    class Meta:
        model = models.WaterSupplyHistory
        fields = ['id','water_supply_id', 'province_id', 'district_id', 'created_by', 'created_at', 'commune_id', 'village_id', 'water_supply_code', 'total_family', 'utm_x', 'utm_y', 'is_risk_enviroment_area', 'construction_date', 'source_budget', 'constructed_by', 
        'management_type', 'managed_by', 'beneficiary_total_people', 'beneficiary_total_women', 'beneficiary_total_family', 'beneficiary_total_family_poor_1', 'beneficiary_total_family_poor_2', 'beneficiary_total_family_vulnerable', 'beneficiary_total_family_indigenous', 'main_status']

class WaterSupplyUpdateSerializer(serializers.ModelSerializer):
    updated_at = serializers.DateTimeField(default=datetime.now())
    class Meta:
        model = models.WaterSupply
        fields = ['id','province_id', 'district_id', 'updated_by', 'updated_at', 'is_active', 'commune_id', 'village_id', 'water_supply_code', 'total_family', 'utm_x', 'utm_y', 'is_risk_enviroment_area', 'construction_date', 'source_budget', 'constructed_by', 
        'management_type', 'managed_by', 'beneficiary_total_people', 'beneficiary_total_women', 'beneficiary_total_family', 'beneficiary_total_family_poor_1', 'beneficiary_total_family_poor_2', 'beneficiary_total_family_vulnerable', 'beneficiary_total_family_indigenous', 'main_status', 'is_water_quality_check',
        'map_unit', 'decimal_degress_lat', 'decimal_degress_lng', 'mds_x_degress', 'mds_x_minute', 'mds_x_second', 'mds_y_degress', 'mds_y_minute', 'mds_y_second']

class WaterSupplyDeleteSerializer(serializers.ModelSerializer):
    updated_at = serializers.DateTimeField(default=datetime.now())
    class Meta:
        model = models.WaterSupply
        fields = ['id', 'updated_by', 'updated_at', 'is_active',]

class WaterSupplyWorkflowSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(default=datetime.now(), format="%Y-%m-%d")
    status_id = StatusSerializer(many=False, read_only=True)
    user_id = UserSerializer(many=False, read_only=True)
    watersupply_id = WaterSupplySerializer(many=False, read_only=True)

    class Meta:
        model = WaterSupplyWorkFlow
        fields = ('id', 'watersupply_id', 'status_id', 'user_id', 'created_at', 'remark')

class WaterSupplyWorkflowSerializer_v2(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(default=datetime.now())
    class Meta:
        model = WaterSupplyWorkFlow
        fields = ('id', 'watersupply_id', 'status_id', 'user_id', 'created_at', 'remark')

class WaterSupplyUpdateMainStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterSupply
        fields = ('id', 'main_status')

    def update(self, instance, validated_data):
        instance.main_status = validated_data.get('main_status', instance.main_status)
        instance.save()
        return instance

class WaterQuanlityCheckParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterQualityCheckedParamater
        fields = '__all__'


#START REPORT
class WaterSupplyReportMapSerializer(serializers.ModelSerializer):

    class Meta:
        model = WaterSupply
        fields = ('id', 'water_supply_type_id', 'map_unit', 'decimal_degress_lat', 'decimal_degress_lng', 'utm_x', 'utm_y', 'mds_x_degress', 'mds_x_minute', 'mds_x_second', 'mds_y_degress', 'mds_y_minute', 'mds_y_second')


#END REPORT