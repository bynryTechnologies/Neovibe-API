__author__ = "aki"

from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from v1.commonapp.common_functions import ChoiceField
from v1.commonapp.serializers.area import AreaShortViewSerializer
from v1.commonapp.serializers.city import CityShortViewSerializer
from v1.commonapp.serializers.premises import PremisesShortViewSerializer
from v1.commonapp.serializers.state import StateShortViewSerializer
from v1.commonapp.serializers.sub_area import SubAreaShortViewSerializer
from v1.meter_data_management.models.meter import Meter as MeterTbl
from v1.commonapp.serializers.global_lookup import GlobalLookupShortViewSerializer
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.meter_data_management.serializers.meter_make import MeterMakeShortViewSerializer
from v1.meter_data_management.serializers.route import RouteShortViewSerializer
from v1.meter_data_management.views.common_function import set_meter_validated_data
from v1.utility.serializers.utility_product import UtilityProductShortViewSerializer


class MeterListSerializer(serializers.ModelSerializer):

    class Meta:
        model = MeterTbl
        fields = ('id_string', 'meter_make')


class MeterViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer()
    utility = UtilityMasterViewSerializer()
    state_id = StateShortViewSerializer(many=False, source='get_state_name')
    city_id = CityShortViewSerializer(many=False, source='get_city_name')
    area_id = AreaShortViewSerializer(many=False, source='get_area_name')
    sub_area_id = SubAreaShortViewSerializer(many=False, source='get_sub_area_name')
    route_id = RouteShortViewSerializer(many=False, source='get_route_name')
    premise_id = PremisesShortViewSerializer(many=False, source='get_premise_type')
    category_id = GlobalLookupShortViewSerializer(many=False, source='get_category_name')
    meter_type_id = GlobalLookupShortViewSerializer(many=False, source='get_meter_type_name')
    meter_make_id = MeterMakeShortViewSerializer(many=False, source='get_meter_make')
    utility_product_id = UtilityProductShortViewSerializer(many=False, source='get_utility_product_type_name')
    meter_status = ChoiceField(choices=MeterTbl.METER_STATUS)
    reader_status = ChoiceField(choices=MeterTbl.READER_STATUS)

    class Meta:
        model = MeterTbl
        fields = ('id_string', 'meter_no', 'meter_digit', 'current_reading', 'latitude', 'longitude', 'meter_status',
                  'reader_status', 'install_date', 'created_by', 'updated_by', 'created_date', 'updated_date',
                  'state_id', 'city_id', 'area_id', 'sub_area_id', 'route_id', 'premise_id', 'meter_type_id',
                  'meter_make_id', 'utility_product_id', 'category_id', 'tenant', 'utility',)


class MeterSerializer(serializers.ModelSerializer):
    utility_id = serializers.UUIDField(required=True)
    route_id = serializers.UUIDField(required=True)
    premise_id = serializers.UUIDField(required=True)
    meter_type_id = serializers.UUIDField(required=False)
    utility_product_id = serializers.UUIDField(required=False)
    meter_detail = serializers.JSONField(required=False)

    class Meta:
        model = MeterTbl
        fields = ('__all__')

    def update(self, instance, validated_data, user):
        validated_data = set_meter_validated_data(validated_data)
        with transaction.atomic():
            meter_obj = super(MeterSerializer, self).update(instance, validated_data)
            meter_obj.tenant = user.tenant
            meter_obj.updated_by = user.id
            meter_obj.updated_date = timezone.now()
            meter_obj.save()
            return meter_obj
