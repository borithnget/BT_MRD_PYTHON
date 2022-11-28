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
        
        
class WaterSupplyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterSupplyType
        fields = '__all__'
        
class WaterSupplyOptionValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterSupplyOptionValue
        fields = '__all__'
        
class WaterSupplyOptionSerializer(serializers.ModelSerializer):
    
    values = WaterSupplyOptionValueSerializer(read_only=True, many=True)
    
    class Meta:
        model = WaterSupplyOption
        fields = '__all__'
        #fields=('id', 'values')
        

        
class WaterSupplyTypeOptionSerializer(serializers.ModelSerializer):
    
    #watersupplytypeoption_option = WaterSupplyOptionSerializer(many=True)
    water_supply_type_id = WaterSupplyTypeSerializer(many=False)
    water_supply_option_id = WaterSupplyOptionSerializer(read_only=True, many=False)
    
    class Meta:
        model = models.WaterSupplyTypeOption
        # fields = '__all__'
        fields = ('id', 'ordering', 'water_supply_type_id', 'water_supply_option_id')
        
class WaterSupplySerializer(serializers.HyperlinkedModelSerializer):
    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)
    water_supply_type_id = WaterSupplyTypeSerializer(many=False, read_only=True)
    province_id = ProvinceSerializer(many=False, read_only=True)
    district_id = DistrictSerializer(many=False, read_only=True)
    commune_id = CommuneSerializer(many=False, read_only=True)
    village_id = VillageSerializer(many=False, read_only=True)
    
    
    class Meta:
        model = models.WaterSupply
        fields = ('id', 'water_supply_type_id', 'province_id', 'district_id', 'created_by', 'updated_by', 'created_at', 'updated_at', 'commune_id', 'village_id', 'water_supply_code', 'total_family', 'utm_x', 'utm_y', 'is_risk_enviroment_area', 'construction_date')
        
class WaterSupplySerializer_v2(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(default=datetime.now())
    class Meta:
        model = models.WaterSupply
        fields = ['id','water_supply_type_id', 'province_id', 'district_id', 'created_by', 'updated_by', 'created_at', 'updated_at', 'is_active', 'commune_id', 'village_id', 'water_supply_code', 'total_family', 'utm_x', 'utm_y', 'is_risk_enviroment_area', 'construction_date']