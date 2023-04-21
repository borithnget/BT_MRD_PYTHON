from email.policy import default
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import AbstractUser

#import jsonfield
# Create your models here.

class Country(models.Model):
    code_en = models.CharField(max_length=255, default='')
    code_kh = models.CharField(max_length=255, default='')
    name_en = models.CharField(max_length=500)
    name_kh = models.CharField(max_length=500)
    description = models.CharField(max_length=1000, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    total_population = models.DecimalField(max_digits=25, decimal_places=0, default=0, null=True, blank=True)
    coordinate_border = models.TextField(null=True, blank=True, default='')
    coordinate_center = models.CharField(max_length=255, default='', null=True, blank=True)
    #the_json = jsonfield.JSONField()
    form_data = models.JSONField(null=True, blank=True)
    
    def __str__(self):
        return '%s - %s' % (self.code_en, self.name_en)

class Province(models.Model):
    code_en = models.CharField(max_length=255, default='')
    code_kh = models.CharField(max_length=255, default='')
    name_en = models.CharField(max_length=500)
    name_kh = models.CharField(max_length=500)
    description = models.CharField(max_length=1000, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    total_population = models.DecimalField(max_digits=25, decimal_places=0, default=0, null=True, blank=True)
    coordinate_border = models.TextField(null=True, blank=True, default='')
    coordinate_center = models.CharField(max_length=255, default='', null=True, blank=True)
    
    def __str__(self):
        return '%s - %s' % (self.code_en, self.name_en)

class User(AbstractUser):
    is_head_department = models.BooleanField(default=False)
    is_data_entry = models.BooleanField(default=False)
    is_provincial_department_head = models.BooleanField(default=False)
    is_data_verifier_1 = models.BooleanField(default=False)
    is_data_verifier_2 = models.BooleanField(default=False)
    is_partner = models.BooleanField(default=False)
    data_entry_province_id = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='userdataentry_province', null=True, blank=True)
    provincial_department_head_province_id = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='provincialdepartmenthead_province', null=True, blank=True)

class UserDetail(models.Model):
    data_entry_province_id = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='userdetaildataentry_province', null=True, blank=True)
    provincial_department_head_province_id = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='userdetailprovincialdepartmenthead_province', null=True, blank=True)

class District(models.Model):
    code_en = models.CharField(max_length=255, default='')
    code_kh = models.CharField(max_length=255, default='')
    name_en = models.CharField(max_length=500)
    name_kh = models.CharField(max_length=500)
    description = models.CharField(max_length=1000, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    province_id = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='provincedistrict')
    total_population = models.DecimalField(max_digits=25, decimal_places=0, default=0, null=True, blank=True)
    coordinate_border = models.TextField(null=True, blank=True, default='')
    coordinate_center = models.CharField(max_length=255, default='', null=True, blank=True)
    
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
    total_population = models.DecimalField(max_digits=25, decimal_places=0, default=0, null=True, blank=True)
    coordinate_border = models.TextField(null=True, blank=True, default='')
    coordinate_center = models.CharField(max_length=255, default='', null=True, blank=True)
    
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
    total_population = models.DecimalField(max_digits=25, decimal_places=0, default=0, null=True, blank=True)
    coordinate_border = models.TextField(null=True, blank=True, default='')
    coordinate_center = models.CharField(max_length=255, default='', null=True, blank=True)
    
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
    is_required = models.BooleanField(default=False)
    
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
        return '%s. %s' % (self.water_supply_option_id, self.name_kh)
    
class WaterSupplyTypeOption(models.Model):
    ordering = models.IntegerField(default=0, null=True, blank=True)
    water_supply_type_id = models.ForeignKey(WaterSupplyType, on_delete=models.CASCADE, related_name='watersupplytypeoption_type')
    water_supply_option_id = models.ForeignKey(WaterSupplyOption, on_delete=models.CASCADE, related_name='watersupplytypeoption_option')
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return '%s. %s %s' % (self.ordering, self.water_supply_type_id, self.water_supply_option_id)

class Status(models.Model):
    status_code = models.CharField(max_length=50, default='', null=True, blank=True)
    status_name = models.CharField(max_length=500, default='', null=True, blank=True)
    status_name_kh = models.CharField(max_length=500, default='', null=True, blank=True)
    background_color = models.CharField(max_length=500, default='', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.status_name
    
class WaterSupply(models.Model):
    water_supply_type_id = models.ForeignKey(WaterSupplyType, on_delete=models.CASCADE, related_name='watersupply_type')
    province_id = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='watersupply_province')
    district_id = models.ForeignKey(District, on_delete=models.CASCADE, related_name='watersupply_district')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watersupply_created_by', null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watersupply_updated_by', null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    crated_at_1 = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    commune_id = models.ForeignKey(Commune, on_delete=models.CASCADE, related_name='watersupply_commune', null=True, blank=True)
    village_id = models.ForeignKey(Village, on_delete=models.CASCADE, related_name='watersupply_village',  null=True, blank=True)
    water_supply_code = models.TextField(default='', null=True, blank=True)
    total_family = models.IntegerField(default=0, null=True, blank=True)
    utm_x = models.DecimalField(max_digits=30, decimal_places=15, default=0, null=True, blank=True)
    utm_y = models.DecimalField(max_digits=30, decimal_places=15, default=0, null=True, blank=True)
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
    main_status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name="watersupply_status", null=True, blank=True)
    is_water_quality_check = models.BooleanField(default=False)
    map_unit = models.IntegerField(default=0, null=True, blank=True)
    decimal_degress_lat = models.DecimalField(max_digits=20, decimal_places=15, default=0, null=True, blank=True)
    decimal_degress_lng = models.DecimalField(max_digits=20, decimal_places=15, default=0, null=True, blank=True)
    mds_x_degress = models.DecimalField(max_digits=20, decimal_places=15, default=0, null=True, blank=True)
    mds_x_minute = models.DecimalField(max_digits=20, decimal_places=15, default=0, null=True, blank=True)
    mds_x_second = models.DecimalField(max_digits=20, decimal_places=15, default=0, null=True, blank=True)
    mds_y_degress = models.DecimalField(max_digits=20, decimal_places=15, default=0, null=True, blank=True)
    mds_y_minute = models.DecimalField(max_digits=20, decimal_places=15, default=0, null=True, blank=True)
    mds_y_second = models.DecimalField(max_digits=20, decimal_places=15, default=0, null=True, blank=True)

class WaterSupplyHistory(models.Model):
    water_supply_id = models.ForeignKey(WaterSupply, on_delete=models.CASCADE, related_name='watersupplyhistory_watersupply')
    province_id = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='watersupplyhistory_province')
    district_id = models.ForeignKey(District, on_delete=models.CASCADE, related_name='watersupplyhistory_district')    
    commune_id = models.ForeignKey(Commune, on_delete=models.CASCADE, related_name='watersupplyhistory_commune', null=True, blank=True)
    village_id = models.ForeignKey(Village, on_delete=models.CASCADE, related_name='watersupplyhistory_village',  null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watersupplyhistory_created_by', null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    water_supply_code = models.TextField(default='', null=True, blank=True)
    total_family = models.IntegerField(default=0, null=True, blank=True)
    utm_x = models.DecimalField(max_digits=20, decimal_places=15, default=0, null=True, blank=True)
    utm_y = models.DecimalField(max_digits=20, decimal_places=15, default=0, null=True, blank=True)
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
    main_status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name="watersupplyhistory_status", null=True, blank=True)

class WaterSupplyValue(models.Model):
    watersupply_id = models.ForeignKey(WaterSupply, on_delete=models.CASCADE, related_name= "watersupplyoptionvalue_watersupply")
    water_supply_option_id = models.ForeignKey(WaterSupplyOption, on_delete=models.CASCADE, related_name='watersupplyoptionvalue_option')
    water_supply_option_value = models.TextField(default='', null=True, blank=True)
    is_active = models.BooleanField(default=True)

class WaterSupplyQRCode(models.Model):
    watersupply_id = models.ForeignKey(WaterSupply, on_delete=models.CASCADE, related_name= "watersupplyqrcode_watersupply")
    qr_code_image_name = models.TextField(default='',null=True, blank=True)

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

class WaterSupplyWellOptionValue(models.Model):
    water_supply_well_id = models.ForeignKey(WaterSupplyWell, on_delete=models.CASCADE, related_name= "watersupplywelloptionvalue_watersupplywell")
    option_id = models.ForeignKey(WaterSupplyOption, on_delete=models.CASCADE, related_name='watersupplywelloptionvalue_option')
    value_id = models.ForeignKey(WaterSupplyOptionValue, on_delete=models.CASCADE, related_name='watersupplywelloptionvalue_value')
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
    pipe_length = models.CharField(max_length=50, default='', null=True, blank=True)
    area_covering = models.TextField(default='', null=True, blank=True)

class WaterSupplyPipeOptionValue(models.Model):
    water_supply_pipe_id = models.ForeignKey(WaterSupplyPipe, on_delete=models.CASCADE, related_name= "watersupplypipeoptionvalue_watersupplypipe")
    option_id = models.ForeignKey(WaterSupplyOption, on_delete=models.CASCADE, related_name='watersupplypipeoptionvalue_option')
    value_id = models.ForeignKey(WaterSupplyOptionValue, on_delete=models.CASCADE, related_name='watersupplypipeoptionvalue_value')
    is_active = models.BooleanField(default=True)
    
class WaterSupplyKiosk(models.Model):
    watersupply_id = models.ForeignKey(WaterSupply, on_delete=models.CASCADE, related_name= "watersupplyKiosk_watersupply")
    is_active = models.BooleanField(default=True)
    source_type_of_water = models.CharField(max_length=255, default='', null=True, blank=True)
    abilty_of_produce_water = models.CharField(max_length=255, default='', null=True, blank=True)
    filter_system = models.CharField(max_length=255, default='', null=True, blank=True)
    water_quality_checking  = models.CharField(max_length=255, default='', null=True, blank=True)
    status = models.CharField(max_length=255, default='0', null=True, blank=True)
    status_no_reason = models.TextField(default='', null=True, blank=True)

class WaterSupplyKioskOptionValue(models.Model):
    water_supply_kiosk_id = models.ForeignKey(WaterSupplyKiosk, on_delete=models.CASCADE, related_name= "watersupplykioskoptionvalue_watersupplykiosk")
    option_id = models.ForeignKey(WaterSupplyOption, on_delete=models.CASCADE, related_name='watersupplykioskoptionvalue_option')
    value_id = models.ForeignKey(WaterSupplyOptionValue, on_delete=models.CASCADE, related_name='watersupplykioskoptionvalue_value')
    is_active = models.BooleanField(default=True)
    
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
    water_quality_checking  = models.CharField(max_length=255, default='', null=True, blank=True)

class WaterSupplyPipePrivate(models.Model):
    watersupply_id = models.ForeignKey(WaterSupply, on_delete=models.CASCADE, related_name= "watersupplypipeprivate_watersupply")
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
    pipe_length = models.CharField(max_length=50, default='', null=True, blank=True)
    area_covering = models.TextField(default='', null=True, blank=True)
    is_has_license = models.CharField(max_length=255, default='0', null=True, blank=True)
    license_registered_date = models.DateField(null=True, blank=True)
    license_expired_date = models.DateField(null=True, blank=True)

class WaterSupplyPipePrivateOptionValue(models.Model):
    water_supply_pipe_id = models.ForeignKey(WaterSupplyPipePrivate, on_delete=models.CASCADE, related_name= "watersupplypipeprivateoptionvalue_watersupplypipewater")
    option_id = models.ForeignKey(WaterSupplyOption, on_delete=models.CASCADE, related_name='watersupplypipeprivateoptionvalue_option')
    value_id = models.ForeignKey(WaterSupplyOptionValue, on_delete=models.CASCADE, related_name='watersupplypipeprivateoptionvalue_value')
    is_active = models.BooleanField(default=True)

class WaterSupplyAirWater(models.Model):
    watersupply_id = models.ForeignKey(WaterSupply, on_delete=models.CASCADE, related_name= "watersupplyairwater_watersupply")
    is_active = models.BooleanField(default=True)
    source_type_of_water = models.CharField(max_length=255, default='', null=True, blank=True)
    abilty_of_produce_water = models.CharField(max_length=255, default='', null=True, blank=True)
    filter_system = models.CharField(max_length=255, default='', null=True, blank=True)
    water_quality_checking  = models.CharField(max_length=255, default='', null=True, blank=True)
    status = models.CharField(max_length=255, default='0', null=True, blank=True)
    status_no_reason = models.TextField(default='', null=True, blank=True)

class WaterSupplyAirWaterOptionValue(models.Model):
    water_supply_airwater_id = models.ForeignKey(WaterSupplyAirWater, on_delete=models.CASCADE, related_name= "watersupplyairwateroptionvalue_watersupplykioskwater")
    option_id = models.ForeignKey(WaterSupplyOption, on_delete=models.CASCADE, related_name='watersupplyairwateroptionvalue_option')
    value_id = models.ForeignKey(WaterSupplyOptionValue, on_delete=models.CASCADE, related_name='watersupplyairwateroptionvalue_value')
    is_active = models.BooleanField(default=True)
    
class WaterSupplyWorkFlow(models.Model):
    watersupply_id = models.ForeignKey(WaterSupply, on_delete=models.CASCADE, related_name= "watersupplyworkflow_watersupply")
    status_id = models.ForeignKey(Status, on_delete=models.CASCADE, related_name= "watersupplyworkflow_status")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "watersupplyworkflow_user_id")
    created_at = models.DateTimeField(null=True, blank=True)
    remark = models.TextField(null=True, blank=True, default='')

    def __str__(self):
        return '%s. %s by %s' % (self.watersupply_id.water_supply_type_id, self.status_id, self.user_id)

class WaterQualityCheckedParamater(models.Model):
    parameter_code = models.CharField(max_length=50, default='', null=True, blank=True)
    parameter = models.CharField(max_length=255, default='', null=True, blank=True)
    unit = models.CharField(max_length=50, default='', null=True, blank=True)
    standard_of_drinking_water = models.CharField(max_length=255, default='', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    field_name = models.CharField(max_length=50, default='', null=True, blank=True)

    def __str__(self):
        return '%s %s' % (self.parameter_code, self.parameter)

class WaterSupplyQuanlityCheckParamater(models.Model):
    water_supply_id = models.ForeignKey(WaterSupply, on_delete=models.CASCADE, related_name= "watersupplyquanlitycheckparamater_watersupply")
    water_quanlity_check_parameter_id = models.ForeignKey(WaterQualityCheckedParamater, on_delete=models.CASCADE, related_name= "watersupplyquanlitycheckparamater_water_quanlity_check_parameter")
    value = models.DecimalField(null=True, blank=True, default=0 , max_digits=5, decimal_places=2)
    is_active = models.BooleanField(default=True)

class Menu(models.Model):
    code = models.CharField(max_length=255, default='', null=True, blank=True)
    name_en = models.TextField(default='', null=True, blank=True)
    name_kh = models.TextField(default='', null=True, blank=True)
    description = models.CharField(max_length=1000, default='', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    ordering = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return '%s %s %s' % (self.id, self.name_en, self.name_kh)

class MenuPermission(models.Model):
    menu_id = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name= "menu_menupermission")
    is_create = models.BooleanField(default=False)
    is_edit = models.BooleanField(default=False)
    is_detail = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    is_data_entry = models.BooleanField(default=False)
    is_provincial_department_head = models.BooleanField(default=False)
    is_data_verifier_1 = models.BooleanField(default=False)
    is_data_verifier_2 = models.BooleanField(default=False)
    is_partner = models.BooleanField(default=False)
    is_head_department = models.BooleanField(default=False)

    def __str__(self):
        return self.menu_id.name_kh