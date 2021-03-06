from rest_framework import serializers, status
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.store.models.store_type import StoreType as StoreTypeTbl
from django.db import transaction
from datetime import datetime
from v1.commonapp.views.custom_exception import CustomAPIException
from api.messages import NAME_ALREADY_EXIST
from v1.store.views.common_functions import set_store_type_vaidated_data

class StoreTypeListSerializer(serializers.ModelSerializer):

    class Meta:
        model = StoreTypeTbl
        fields = ('id_string', 'name','is_active','created_by','created_date')


class StoreTypeViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = StoreTypeTbl
        fields = ('id_string', 'name', 'tenant','tenant_id_string','utility','utility_id_string')

class StoreTypeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200)
    utility_id = serializers.CharField(required=True, max_length=200)
    tenant_id = serializers.CharField(required=True, max_length=200)

    class Meta:
        model = StoreTypeTbl
        fields = ('__all__')

    def create(self, validated_data,  user):
        with transaction.atomic():
            validated_data = set_store_type_vaidated_data(validated_data)
            if StoreTypeTbl.objects.filter(name=validated_data['name'],tenant_id=validated_data['tenant_id'],
                                            utility_id=validated_data['utility_id']).exists():
                    raise CustomAPIException(NAME_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:
                store_type_obj = super(StoreTypeSerializer, self).create(validated_data)
                store_type_obj.created_by = user.id
                store_type_obj.updated_by = user.id
                store_type_obj.save()
                return store_type_obj

    def update(self, instance, validated_data, user):
        validated_data = set_store_type_vaidated_data(validated_data)
        if StoreTypeTbl.objects.filter(name=validated_data['name'],tenant_id=validated_data['tenant_id'],
                                            utility_id=validated_data['utility_id']).exists():
                    raise CustomAPIException(NAME_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
        else:
            with transaction.atomic():
                store_type_obj = super(StoreTypeSerializer, self).update(instance, validated_data)
                store_type_obj.updated_by = user.id
                store_type_obj.updated_date = datetime.utcnow()
                store_type_obj.save()
                return store_type_obj