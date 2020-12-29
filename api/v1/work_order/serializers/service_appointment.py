__author__ = "Priyanka"
from django.db import transaction
from datetime import datetime
from rest_framework import serializers, status
import random
from rest_framework.validators import UniqueTogetherValidator
from api.settings import DISPLAY_DATE_TIME_FORMAT
from v1.work_order.models.service_appointments import ServiceAppointment
from v1.work_order.views.common_functions import set_service_appointment_validated_data
from v1.tenant.serializers.tenant import TenantStatusViewSerializer
from v1.consumer.serializers.consumer_master import ConsumerListSerializer
from v1.asset.serializer.asset import AssetShortListSerializer
from v1.work_order.serializers.work_order_master import WorkOrderMasterShortListSerializer
from v1.work_order.serializers.service_appointment_status import ServiceAppointmentStatusListSerializer
from v1.work_order.views.common_functions import generate_service_appointment_no
from v1.commonapp.views.custom_exception import CustomAPIException
from api.messages import WORK_ORDER_ALREADY_EXIST

class ServiceAppointmentSerializer(serializers.ModelSerializer):
    utility_id = serializers.CharField(required=False, max_length=200)
    consumer_id = serializers.CharField(required=False, max_length=200)
    asset_id = serializers.CharField(required=False, max_length=200)
    service_id = serializers.CharField(required=False, max_length=200)
    sa_name = serializers.CharField(required=True, max_length=200)
    sa_description = serializers.CharField(required=True, max_length=200)
    sa_date = serializers.CharField(required=False, max_length=200)
    sa_time = serializers.CharField(required=False, max_length=200)
    sa_estimated_effort = serializers.CharField(required=False, max_length=200)
    alternative_contact = serializers.CharField(required=False, max_length=200)
    alternative_address = serializers.CharField(required=False, max_length=200)
    actual_start_time = serializers.CharField(required=False, max_length=200)
    actual_end_time = serializers.CharField(required=False, max_length=200)
    actual_duration = serializers.CharField(required=False, max_length=200)
    status_id = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = ServiceAppointment
        fields = ('__all__')

    def create(self, validated_data, user):
        validated_data = set_service_appointment_validated_data(validated_data)
        if ServiceAppointment.objects.filter(consumer_id=validated_data['consumer_id'],service_id=validated_data['service_id'],
                                             asset_id=validated_data['asset_id'], tenant=user.tenant,
                                             utility_id=validated_data['utility_id']).exists():
            raise CustomAPIException(WORK_ORDER_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
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
            appointment_obj.updated_by = user.id
            appointment_obj.updated_date = datetime.utcnow()
            appointment_obj.is_active = True
            appointment_obj.save()
            return appointment_obj

class ServiceAppointmentViewSerializer(serializers.ModelSerializer):
    tenant = TenantStatusViewSerializer(many=False, required=True, source='get_tenant')
    consumer_id = ConsumerListSerializer(many=False, required=True, source='get_consumer')
    asset_id = AssetShortListSerializer(many=False, required=True, source='get_asset')
    service_id = WorkOrderMasterShortListSerializer(many=False, required=True, source='get_service')
    status_id = ServiceAppointmentStatusListSerializer(many=False, required=True, source='get_status')
    created_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    updated_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)

    class Meta:
        model = ServiceAppointment
        fields = ('__all__')

