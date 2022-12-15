from email.policy import default
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    is_head_department = models.BooleanField(default=False)
    is_data_entry = models.BooleanField(default=False)
    
class Province(models.Model):
    code_en = models.CharField(max_length=255, default='')
    code_kh = models.CharField(max_length=255, default='')
    name_en = models.CharField(max_length=500)
    name_kh = models.CharField(max_length=500)
    description = models.CharField(max_length=1000, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return '%s - %s' % (self.code_en, self.name_en)
    
class District(models.Model):
    code_en = models.CharField(max_length=255, default='')
    code_kh = models.CharField(max_length=255, default='')
    name_en = models.CharField(max_length=500)
    name_kh = models.CharField(max_length=500)
    description = models.CharField(max_length=1000, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    province_id = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='provincedistrict')
    
    def __str__(self):
        return self.name_en
    
class Commune(models.Model):
    code_en = models.CharField(max_length=255, default='')
    code_kh = models.CharField(max_length=255, default='')
    name_en = models.CharField(max_length=500)
    name_kh = models.CharField(max_length=500)
    description = models.CharField(max_length=1000, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    district_id = models.ForeignKey(District, on_delete=models.CASCADE, related_name="districtcommnue")
    
    def __str__(self):
        return self.name_en
    
class Village(models.Model):
    code_en = models.CharField(max_length=255, default='')
    code_kh = models.CharField(max_length=255, default='')
    name_en = models.CharField(max_length=500)
    name_kh = models.CharField(max_length=500)
    description = models.CharField(max_length=1000, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    commune_id = models.ForeignKey(Commune, on_delete=models.CASCADE, related_name="commnuevillage")
    
    def __str__(self):
        return self.name_en
    
class WaterSupplyType(models.Model):
    code = models.CharField(max_length=255, default='')
    name_en = models.CharField(max_length=500, default='')
    name_kh = models.CharField(max_length=500, default='')
    description = models.CharField(max_length=1000, default='', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name_en
    
class WaterSupplyOption(models.Model):
    code = models.CharField(max_length=255, default='', null=True, blank=True)
    name_en = models.TextField(default='', null=True, blank=True)
    name_kh = models.TextField(default='', null=True, blank=True)
    data_type = models.CharField(default='', null=True, blank=True, max_length=255)
    description = models.CharField(max_length=1000, default='', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    field_name = models.CharField(max_length=255 , default='', null=True, blank=True)
    
    def __str__(self):
        return self.name_kh
    
class WaterSupplyOptionValue(models.Model):
    code = models.CharField(max_length=255, default='', null=True, blank=True)
    name_en = models.TextField(default='', null=True, blank=True)
    name_kh = models.TextField(default='', null=True, blank=True)
    description = models.CharField(max_length=1000, default='', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    water_supply_option_id = models.ForeignKey(WaterSupplyOption, on_delete=models.CASCADE, related_name='watersupplyoption_value')
    
    def __str__(self):
        return self.name_kh
    
class WaterSupplyTypeOption(models.Model):
    ordering = models.IntegerField(default=0, null=True, blank=True)
    water_supply_type_id = models.ForeignKey(WaterSupplyType, on_delete=models.CASCADE, related_name='watersupplytypeoption_type')
    water_supply_option_id = models.ForeignKey(WaterSupplyOption, on_delete=models.CASCADE, related_name='watersupplytypeoption_option')
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return '%s. %s %s' % (self.ordering, self.water_supply_type_id, self.water_supply_option_id)
    
class WaterSupply(models.Model):
    water_supply_type_id = models.ForeignKey(WaterSupplyType, on_delete=models.CASCADE, related_name='watersupply_type')
    province_id = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='watersupply_province')
    district_id = models.ForeignKey(District, on_delete=models.CASCADE, related_name='watersupply_district')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watersupply_created_by', null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watersupply_updated_by', null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    commune_id = models.ForeignKey(Commune, on_delete=models.CASCADE, related_name='watersupply_commune', null=True, blank=True)
    village_id = models.ForeignKey(Village, on_delete=models.CASCADE, related_name='watersupply_village',  null=True, blank=True)
    water_supply_code = models.TextField(default='', null=True, blank=True)
    total_family = models.IntegerField(default=0, null=True, blank=True)
    utm_x = models.DecimalField(max_digits=12, decimal_places=6, default=0, null=True, blank=True)
    utm_y = models.DecimalField(max_digits=12, decimal_places=6, default=0, null=True, blank=True)
    is_risk_enviroment_area = models.BooleanField(default=True)
    construction_date = models.DateField(null=True, blank=True)
    source_budget = models.IntegerField(default=0, null=True, blank=True)
    constructed_by = models.TextField(default='', null=True, blank=True)
    management_type = models.IntegerField(default=0, null=True, blank=True)
    managed_by = models.TextField(default='', null=True, blank=True)
    beneficiary_total_people = models.IntegerField(default=0, null=True, blank=True)
    beneficiary_total_women = models.IntegerField(default=0, null=True, blank=True)
    beneficiary_total_family = models.IntegerField(default=0, null=True, blank=True)
    beneficiary_total_family_poor_1 = models.IntegerField(default=0, null=True, blank=True)
    beneficiary_total_family_poor_2 = models.IntegerField(default=0, null=True, blank=True)
    beneficiary_total_family_vulnerable = models.IntegerField(default=0, null=True, blank=True)
    beneficiary_total_family_indigenous = models.IntegerField(default=0, null=True, blank=True)

class WaterSupplyValue(models.Model):
    watersupply_id = models.ForeignKey(WaterSupply, on_delete=models.CASCADE, related_name= "watersupplyoptionvalue_watersupply")
    water_supply_option_id = models.ForeignKey(WaterSupplyOption, on_delete=models.CASCADE, related_name='watersupplyoptionvalue_option')
    water_supply_option_value = models.TextField(default='', null=True, blank=True)
    is_active = models.BooleanField(default=True)

class WaterSupplyWell(models.Model):
    watersupply_id = models.ForeignKey(WaterSupply, on_delete=models.CASCADE, related_name= "watersupplywell_watersupply")
    well_type = models.CharField(max_length=255, default='', null=True, blank=True)
    well_height = models.CharField(max_length=255, default='0', null=True, blank=True)
    well_filter_height = models.CharField(max_length=255, default='0', null=True, blank=True)
    well_water_supply = models.CharField(max_length=255, default='0', null=True, blank=True)
    well_nirostatic = models.CharField(max_length=255, default='0', null=True, blank=True)
    well_nirodynamic = models.CharField(max_length=255, default='0', null=True, blank=True)
    well_watar_quality = models.CharField(max_length=255, default='0', null=True, blank=True)
    well_water_quality_check = models.CharField(max_length=255, default='0', null=True, blank=True)
    well_status = models.CharField(max_length=255, default='0', null=True, blank=True)
    well_status_reason = models.TextField(default='', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
class WaterSupplyPipe(models.Model):
    watersupply_id = models.ForeignKey(WaterSupply, on_delete=models.CASCADE, related_name= "watersupplypipe_watersupply")
    is_active = models.BooleanField(default=True)
    source_type_of_water = models.CharField(max_length=255, default='', null=True, blank=True)
    abilty_of_produce_water = models.CharField(max_length=255, default='', null=True, blank=True)
    underground_pool_storage = models.CharField(max_length=255, default='', null=True, blank=True)
    pool_air = models.CharField(max_length=255, default='', null=True, blank=True)
    pool_filter = models.CharField(max_length=255, default='', null=True, blank=True)
    number_of_link = models.CharField(max_length=255, default='', null=True, blank=True)
    water_quality_check = models.CharField(max_length=255, default='0', null=True, blank=True)
    status = models.CharField(max_length=255, default='0', null=True, blank=True)
    status_no_reason = models.TextField(default='', null=True, blank=True)
    
class WaterSupplyKiosk(models.Model):
    watersupply_id = models.ForeignKey(WaterSupply, on_delete=models.CASCADE, related_name= "watersupplyKiosk_watersupply")
    is_active = models.BooleanField(default=True)
    source_type_of_water = models.CharField(max_length=255, default='', null=True, blank=True)
    abilty_of_produce_water = models.CharField(max_length=255, default='', null=True, blank=True)
    filter_system = models.CharField(max_length=255, default='', null=True, blank=True)
    status = models.CharField(max_length=255, default='0', null=True, blank=True)
    status_no_reason = models.TextField(default='', null=True, blank=True)
    
class WaterSupplyCommunityPond(models.Model):
    watersupply_id = models.ForeignKey(WaterSupply, on_delete=models.CASCADE, related_name= "watersupplyCommunityPond_watersupply")
    is_active = models.BooleanField(default=True)
    width = models.CharField(max_length=255, default='0', null=True, blank=True)
    length = models.CharField(max_length=255, default='0', null=True, blank=True)
    height = models.CharField(max_length=255, default='0', null=True, blank=True)
    pool_filter = models.CharField(max_length=255, default='0', null=True, blank=True)
    type_of_pond = models.CharField(max_length=255, default='0', null=True, blank=True)
    is_summer_has_water = models.CharField(max_length=255, default='0', null=True, blank=True)
    status = models.CharField(max_length=255, default='0', null=True, blank=True)
    status_no_reason = models.TextField(default='', null=True, blank=True)
    
class WaterSupplyRainWaterHarvesting(models.Model):
    watersupply_id = models.ForeignKey(WaterSupply, on_delete=models.CASCADE, related_name= "watersupplyRainWaterHarvesting_watersupply")
    is_active = models.BooleanField(default=True)
    type_of_using = models.CharField(max_length=255, default='0', null=True, blank=True)
    capacity_35m3 = models.CharField(max_length=255, default='0', null=True, blank=True)
    capacity_4m3 = models.CharField(max_length=255, default='0', null=True, blank=True)
    capacity_of_rain_water_harvesting = models.CharField(max_length=255, default='0', null=True, blank=True)
    status = models.CharField(max_length=255, default='0', null=True, blank=True)
    status_no_reason = models.TextField(default='', null=True, blank=True)
    