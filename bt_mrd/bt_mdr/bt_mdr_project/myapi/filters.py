from django.forms import MultipleChoiceField
from rest_framework import filters as drf_filters
from django_filters import rest_framework as df_filters
from mdrapp.models import WaterSupply
from django_filters.fields import CSVWidget

class MultipleField(MultipleChoiceField):
    def valid_value(self, value):   
        return True

class MultipleFilter(df_filters.MultipleChoiceFilter):
    field_class = MultipleField

class WaterSupplyMultipleFilterBackend(df_filters.FilterSet):

    main_status = MultipleFilter(
                 lookup_expr="icontains", 
                 field_name = "main_status__id",
                 widget=CSVWidget
            )

    class Meta:
        model = WaterSupply
        fields = ["main_status", "province_id"]