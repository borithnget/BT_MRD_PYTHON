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
    
    def __str__(self):
        return self.name_kh
    
class WaterSupplyOptionValue(models.Model):
    code = models.CharField(max_length=255, default='', null=True, blank=True)
    name_en = models.TextField(default='', null=True, blank=True)
    name_kh = models.TextField(default='', null=True, blank=True)
    description = models.CharField(max_length=1000, default='', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    water_supply_option_id = models.ForeignKey(WaterSupplyOption, on_delete=models.CASCADE)
    
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
    