from django.contrib import admin
from mdrapp import models
from mdrapp.models import User
# Register your models here.

admin.site.register(User)
admin.site.register(models.Province)
admin.site.register(models.District)
admin.site.register(models.Commune)
admin.site.register(models.Village)
admin.site.register(models.WaterSupplyType)
admin.site.register(models.WaterSupplyOption)
admin.site.register(models.WaterSupplyOptionValue)
admin.site.register(models.WaterSupplyTypeOption)
admin.site.register(models.WaterSupply)
admin.site.register(models.WaterSupplyValue)
admin.site.register(models.WaterSupplyWell)
admin.site.register(models.WaterSupplyPipe)
admin.site.register(models.WaterSupplyKiosk)
admin.site.register(models.WaterSupplyCommunityPond)
admin.site.register(models.WaterSupplyRainWaterHarvesting)