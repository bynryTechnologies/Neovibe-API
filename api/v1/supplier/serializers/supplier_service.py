__author__ = "aki"

from django.db import transaction
from rest_framework import serializers
from django.utils import timezone
from v1.commonapp.views.settings_reader import SettingReader
setting_reader = SettingReader()
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.supplier.models.supplier_service import SupplierService as SupplierServiceTbl
from v1.supplier.serializers.supplier import SupplierShortViewSerializer
from v1.supplier.views.common_functions import set_supplier_service_validated_data


class SupplierServiceViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer(read_only=True)
    utility = UtilityMasterViewSerializer(read_only=True)
    supplier = SupplierShortViewSerializer(many=False, required=False, source='get_supplier')
    created_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)
    updated_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)

    class Meta:
        model = SupplierServiceTbl
        fields = ('id_string', 'name', 'rate', 'quantity', 'unit', 'created_date', 'updated_date', 'tenant', 'utility',
                  'supplier', 'type', 'category', 'subcategory', 'status', 'source_type')


class SupplierServiceSerializer(serializers.ModelSerializer):
    category = serializers.UUIDField(required=False)
    subcategory = serializers.UUIDField(required=False)
    type = serializers.UUIDField(required=False)
    status = serializers.UUIDField(required=False)
    source_type = serializers.UUIDField(required=False)
    name = serializers.CharField(required=True, max_length=200)
    rate = serializers.FloatField(required=True)
    quantity = serializers.CharField(required=True, max_length=200)

    class Meta:
        model = SupplierServiceTbl
        fields = ('__all__')

    def create(self, validated_data, supplier_obj, user):
        validated_data = set_supplier_service_validated_data(validated_data)
        if SupplierServiceTbl.objects.filter(tenant=user.tenant, utility=user.utility,
                                             supplier=supplier_obj.id, name=validated_data["name"]).exists():
            return False
        with transaction.atomic():
            supplier_service_obj = super(SupplierServiceSerializer, self).create(validated_data)
            supplier_service_obj.tenant = user.tenant
            supplier_service_obj.utility = user.utility
            supplier_service_obj.supplier = supplier_obj.id
            supplier_service_obj.created_by = user.id
            supplier_service_obj.save()
            return supplier_service_obj

    def update(self, instance, validated_data, user):
        validated_data = set_supplier_service_validated_data(validated_data)
        with transaction.atomic():
            supplier_service_obj = super(SupplierServiceSerializer, self).update(instance, validated_data)
            supplier_service_obj.tenant = user.tenant
            supplier_service_obj.utility = user.utility
            supplier_service_obj.updated_by = user.id
            supplier_service_obj.updated_date = timezone.now()
            supplier_service_obj.save()
            return supplier_service_obj