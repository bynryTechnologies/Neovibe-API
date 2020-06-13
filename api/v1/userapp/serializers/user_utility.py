from django.db import transaction
from datetime import datetime

from rest_framework import serializers, status

from api.settings import DISPLAY_DATE_TIME_FORMAT
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.tenant.serializers.tenant_status import TenantStatusViewSerializer
from v1.userapp.models.user_utility import UserUtility
from v1.userapp.views.common_functions import set_user_utility_validated_data
from v1.utility.serializers.utility import UtilitySerializer


class GetUserUtilitySerializer(serializers.ModelSerializer):

    def get_created_date(self, obj):
        return obj.created_date.strftime(DISPLAY_DATE_TIME_FORMAT)

    utility = UtilitySerializer(many=False, required=True, source='get_utility')
    created_date = serializers.SerializerMethodField('get_created_date')

    class Meta:
        model = UserUtility
        fields = ('utility', 'id_string')


class UserUtilityViewSerializer(serializers.ModelSerializer):

    def get_created_date(self, obj):
        return obj.created_date.strftime(DISPLAY_DATE_TIME_FORMAT)

    tenant = TenantStatusViewSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')
    created_date = serializers.SerializerMethodField('get_created_date')

    class Meta:
        model = UserUtility
        fields = ('id_string', 'tenant', 'utility', 'created_date')


class UserUtilitySerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(required=False, max_length=200)
    utility_id = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = UserUtility
        fields = '__all__'

    def create(self, validate_data, user):
        validated_data = set_user_utility_validated_data(validate_data)
        if UserUtility.objects.filter(user_id=validated_data['user_id'], utility_id=validated_data['utility_id'], tenant=user.tenant,
                                        is_active=True).exists():
            raise CustomAPIException("Utility already exists for specified user!",
                                     status_code=status.HTTP_409_CONFLICT)
        else:
            with transaction.atomic():
                user_utility_obj = super(UserUtilitySerializer, self).create(validated_data)
                user_utility_obj.created_by = user.id
                user_utility_obj.updated_by = user.id
                user_utility_obj.created_date = datetime.utcnow()
                user_utility_obj.updated_date = datetime.utcnow()
                user_utility_obj.tenant = user.tenant
                user_utility_obj.is_active = True
                user_utility_obj.save()
                return user_utility_obj

    def update(self, instance, validated_data, user):
        with transaction.atomic():
            user_utility_obj = super(UserUtilitySerializer, self).update(instance, validated_data)
            user_utility_obj.updated_by = user.id
            user_utility_obj.updated_date = datetime.utcnow()
            user_utility_obj.is_active = True
            user_utility_obj.save()
            return user_utility_obj

