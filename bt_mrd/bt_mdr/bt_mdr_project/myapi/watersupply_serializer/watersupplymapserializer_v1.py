from drf_eager_fields.serializers import EagerFieldsSerializer
from rest_framework import serializer
from django.db.models import Prefetch, Subquery
from django.db.models.expressions import OuterRef
from django.utils.functional import classproperty
from mdrapp import models
import serializers

class WaterSupplyMapSerializer_V1(serializer.ModelSerializer, EagerFieldsSerializer):
    class Meta:
        model = models.WaterSupply
        fields = ('id', 'decimal_degress_lat', 'decimal_degress_lng')

    @classproperty
    def extra(self):
        return{
            "watersupplytype" : {
                "field": serializers.WaterSupplyTypeSerializer_V2(),
                "prefetch": True,
            }
        }

