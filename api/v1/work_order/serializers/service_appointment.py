__author__ = "Priyanka"

from django.db import transaction
from datetime import datetime
from rest_framework import serializers, status
import random
from rest_framework.validators import UniqueTogetherValidator
from v1.commonapp.views.settings_reader import SettingReader
setting_reader = SettingReader()
from v1.work_order.models.service_appointments import ServiceAppointment
from v1.work_order.views.common_functions import set_service_appointment_validated_data
from v1.tenant.serializers.tenant import TenantStatusViewSerializer
from v1.consumer.serializers.consumer_service_contract_details import ConsumerServiceContractDetailViewSerializer
from v1.asset.serializer.asset import AssetShortListSerializer
from v1.work_order.serializers.work_order_master import WorkOrderMasterShortListSerializer
from v1.work_order.serializers.service_appointment_status import ServiceAppointmentStatusListSerializer
from v1.work_order.views.common_functions import generate_service_appointment_no
from v1.commonapp.views.custom_exception import CustomAPIException
from api.messages import SERVICE_APPOINTMENT_ALREADY_EXIST
from v1.registration.serializers.registration import ChoiceField
from v1.commonapp.serializers.area import AreaShortViewSerializer
from v1.commonapp.serializers.global_lookup import GlobalLookupShortViewSerializer


class ServiceAppointmentListSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')
    consumer_service_contract_detail_id = ConsumerServiceContractDetailViewSerializer(many=False, required=True, source='get_consumer_service_contract_detail_id')
    asset_id = AssetShortListSerializer(many=False, required=False, source='get_asset')
    work_order_master_id = WorkOrderMasterShortListSerializer(many=False, required=True, source='get_service')
    created_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)
    updated_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)
    state = ChoiceField(choices=ServiceAppointment.CHOICES)

    class Meta:
        model = ServiceAppointment
        fields = ('id_string', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string', 'consumer_service_contract_detail_id', 'asset_id',
                  'work_order_master_id',
                  'sa_number', 'sa_name', 'sa_date', 'sa_description', 'sa_rule', 'created_date', 'updated_date',
                  'state', 'is_active', 'sa_user_remark')


class ServiceAppointmentSerializer(serializers.ModelSerializer):
    utility_id = serializers.CharField(required=False, max_length=200)
    asset_id = serializers.CharField(required=False, max_length=200)
    consumer_service_contract_detail_id = serializers.CharField(required=False, max_length=200)
    work_order_master_id = serializers.CharField(required=False, max_length=200)
    # sa_name = serializers.CharField(required=True, max_length=200)
    # sa_description = serializers.CharField(required=True, max_length=200)
    sa_date = serializers.CharField(required=False, max_length=200)
    # sa_time = serializers.CharField(required=False, max_length=200)
    # sa_estimated_effort = serializers.CharField(required=False, max_length=200)
    state_id = serializers.CharField(required=False, max_length=200)
    city_id = serializers.CharField(required=False, max_length=200)
    area_id = serializers.CharField(required=False, max_length=200)
    sub_area_id = serializers.CharField(required=False, max_length=200)
    ownership_id = serializers.CharField(required=False, max_length=200)
    premise_id = serializers.CharField(required=False, max_length=200)
    frequency_id = serializers.UUIDField(required=False)
    repeat_every_id = serializers.UUIDField(required=False)
    recurring_id = serializers.UUIDField(required=False)
    # actual_start_time = serializers.CharField(required=False, max_length=200)
    # actual_end_time = serializers.CharField(required=False, max_length=200)
    # actual_duration = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = ServiceAppointment
        fields = '__all__'

    def create(self, validated_data, user):
        validated_data = set_service_appointment_validated_data(validated_data)
        # if ServiceAppointment.objects.filter(consumer_service_contract_detail_id=validated_data['consumer_service_contract_detail_id'],
        #                                      work_order_master_id=validated_data['work_order_master_id'], is_active=True).exists():
        #     raise CustomAPIException(SERVICE_APPOINTMENT_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
        with transaction.atomic():
            appointment_obj = super(ServiceAppointmentSerializer, self).create(validated_data)
            appointment_obj.created_by = user.id
            appointment_obj.created_date = datetime.utcnow()
            appointment_obj.tenant = user.tenant
            appointment_obj.save()
            appointment_obj.sa_number = generate_service_appointment_no(appointment_obj)
            appointment_obj.save()
            return appointment_obj

    def update(self, instance, validated_data, user):
        validated_data = set_service_appointment_validated_data(validated_data)
        with transaction.atomic():
            appointment_obj = super(ServiceAppointmentSerializer, self).update(instance, validated_data)
            # appointment_obj.state = 5
            appointment_obj.updated_by = user.id
            appointment_obj.updated_date = datetime.utcnow()
            # appointment_obj.is_active = True
            appointment_obj.save()
            return appointment_obj


class ServiceAppointmentViewSerializer(serializers.ModelSerializer):
    tenant = TenantStatusViewSerializer(many=False, required=True, source='get_tenant')
    consumer_service_contract_detail_id = ConsumerServiceContractDetailViewSerializer(many=False, required=True, source='get_consumer_service_contract_detail_id')
    asset_id = AssetShortListSerializer(many=False, required=False, source='get_asset')
    work_order_master_id = WorkOrderMasterShortListSerializer(many=False, required=True, source='get_service')
    created_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)
    updated_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)
    state = ChoiceField(choices=ServiceAppointment.CHOICES)
    frequency_id = GlobalLookupShortViewSerializer(many=False, source='get_frequency_name')
    repeat_every_id = GlobalLookupShortViewSerializer(many=False, source='get_repeat_every_name')
    recurring_id = GlobalLookupShortViewSerializer(many=False, source='get_recurring_name')
    # state_id = serializers.ReadOnlyField(source='get_state')
    # city_id = serializers.ReadOnlyField(source='get_city')
    # area_id = AreaShortViewSerializer(many=False, required=False, source='get_area')
    # sub_area_id = serializers.ReadOnlyField(source='get_sub_area')
    

    class Meta:
        model = ServiceAppointment
        fields = ('__all__')
