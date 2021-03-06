__author__ = "Arpita"

from datetime import datetime
from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from v1.commonapp.views.settings_reader import SettingReader
setting_reader = SettingReader()
from v1.tenant.serializers.tenant_status import TenantStatusViewSerializer
from v1.userapp.models.user_type import UserType
from v1.utility.serializers.utility import UtilitySerializer


class GetUserTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserType
        fields = ('name', 'id_string','key')


class UserTypeListSerializer(serializers.ModelSerializer):
    tenant = TenantStatusViewSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')
    created_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)
    updated_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)

    class Meta:
        model = UserType
        fields = ('id_string', 'tenant', 'utility', 'name', 'created_date', 'updated_date')


class UserTypeViewSerializer(serializers.ModelSerializer):
    tenant = TenantStatusViewSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')
    created_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)
    updated_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)

    class Meta:
        model = UserType
        fields = ('id_string', 'tenant', 'utility', 'name', 'created_date', 'updated_date')


class UserTypeSerializer(serializers.ModelSerializer):
    print('====UserTypeSerializer====')
    
    name = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = UserType
        validators = [UniqueTogetherValidator(queryset=UserType.objects.all(), fields=('name',), message='User Type already exists!')]
        fields = '__all__'

    def create(self, validated_data, user):
        with transaction.atomic():
            type_obj = super(UserTypeSerializer, self).create(validated_data)
            type_obj.created_by = user.id
            type_obj.updated_by = user.id
            type_obj.created_date = datetime.utcnow()
            type_obj.updated_date = datetime.utcnow()
            type_obj.tenant = user.tenant
            type_obj.utility = user.utility
            type_obj.is_active = True
            type_obj.save()
            return type_obj

    def update(self, instance, validated_data, user):
        with transaction.atomic():
            type_obj = super(UserTypeSerializer, self).update(instance, validated_data)
            type_obj.updated_by = user.id
            type_obj.updated_date = datetime.utcnow()
            type_obj.is_active = True
            type_obj.save()
            return type_obj
