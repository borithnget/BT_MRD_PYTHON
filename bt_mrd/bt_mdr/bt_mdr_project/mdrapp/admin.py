from django.contrib import admin
from mdrapp import models
from mdrapp.models import User
# from django.contrib.gis.db import models
# from mapwidgets.widgets import GooglePointFieldWidget
# Register your models here.

admin.site.register(User)
admin.site.register(models.Country)
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
admin.site.register(models.Status)
admin.site.register(models.WaterSupplyWorkFlow)
admin.site.register(models.WaterSupplyWellOptionValue)
admin.site.register(models.WaterSupplyQRCode)
admin.site.register(models.Menu)
admin.site.register(models.MenuPermission)
admin.site.register(models.WaterQualityCheckedParamater)
admin.site.register(models.WaterSupplyQuanlityCheckParamater)
admin.site.register(models.WaterSupplyAirWater)
admin.site.register(models.WaterSupplyAirWaterOptionValue)

# class CityAdmin(admin.ModelAdmin):
#     formfield_overrides = {
#         models.PointField: {"widget": GooglePointFieldWidget}
#     }