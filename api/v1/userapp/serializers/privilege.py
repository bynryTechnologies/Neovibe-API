__author__ = "Arpita"

from datetime import datetime

from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api.settings import DISPLAY_DATE_TIME_FORMAT
from v1.tenant.serializers.tenant_status import TenantStatusViewSerializer
from v1.userapp.models.privilege import Privilege
from v1.utility.serializers.utility import UtilitySerializer


class PrivilegeListSerializer(serializers.ModelSerializer):

    tenant = TenantStatusViewSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')
    created_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    updated_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)

    class Meta:
        model = Privilege
        fields = ('id_string', 'tenant', 'utility', 'name', 'created_date', 'updated_date')


class PrivilegeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = Privilege
        validators = [UniqueTogetherValidator(queryset=Privilege.objects.all(), fields=('name',), message='Privilege already exists!')]
        fields = '__all__'

    def create(self, validated_data, user):
        with transaction.atomic():
            privilege_obj = super(PrivilegeSerializer, self).create(validated_data)
            privilege_obj.created_by = user.id
            privilege_obj.updated_by = user.id
            privilege_obj.created_date = datetime.utcnow()
            privilege_obj.update_date = datetime.utcnow()
            privilege_obj.tenant = user.tenant
            privilege_obj.is_active = True
            privilege_obj.save()
            return privilege_obj

    def update(self, instance, validated_data, user):
        with transaction.atomic():
            privilege_obj = super(PrivilegeSerializer, self).update(instance, validated_data)
            privilege_obj.updated_by = user.id
            privilege_obj.updated_date = datetime.utcnow()
            privilege_obj.is_active = True
            privilege_obj.save()
            return privilege_obj


class PrivilegeViewSerializer(serializers.ModelSerializer):

    tenant = TenantStatusViewSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')
    created_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    updated_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)

    class Meta:
        model = Privilege
        fields = ('id_string', 'tenant', 'utility', 'name', 'created_date', 'updated_date')


class GetPrivilegeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Privilege
        fields = ('id_string', 'name')
