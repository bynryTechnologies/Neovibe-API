# __author__ = "aki"
#
# from django.db import transaction
# from rest_framework import serializers
# from django.utils import timezone
# from v1.commonapp.views.settings_reader import SettingReader
#
# setting_reader = SettingReader()
# from v1.commonapp.serializers.module import ModuleShortViewSerializer
# from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
# from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
# from v1.utility.models.utility_module import UtilityModule as UtilityModuleTbl
# from v1.utility.views.common_functions import set_utility_module_validated_data
#
#
# class UtilityModuleShortViewSerializer(serializers.ModelSerializer):
#     module_id = ModuleShortViewSerializer(many=False, source='get_module')
#
#     class Meta:
#         model = UtilityModuleTbl
#         fields = ('id_string', 'label', 'module_id')
#
#
# class UtilityModuleViewSerializer(serializers.ModelSerializer):
#     tenant = TenantMasterViewSerializer(read_only=True)
#     utility = UtilityMasterViewSerializer(read_only=True)
#     # module_id = ModuleShortViewSerializer(many=False, source='get_module')
#     created_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)
#     updated_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)
#
#     class Meta:
#         model = UtilityModuleTbl
#         fields = ('id_string', 'is_active', 'label', 'created_date', 'updated_date', 'subscription_id', 'module_id',
#                   'tenant', 'utility',)
#
#
# class UtilityModuleSerializer(serializers.ModelSerializer):
#     label = serializers.CharField(required=True, max_length=200,
#                                   error_messages={"required": "The field label is required."})
#     tenant = serializers.UUIDField(required=True, source='tenant.id_string')
#     utility = serializers.UUIDField(required=True, source='utility.id_string')
#     module_id = serializers.UUIDField(required=False)
#
#     class Meta:
#         model = UtilityModuleTbl
#         fields = ('id_string', 'tenant', 'utility','label', 'subscription_id', 'module_id', 'is_active', 'created_by',
#                   'updated_by', 'created_date', 'updated_date')
#
#     def create(self, validated_data, user):
#         validated_data = set_utility_module_validated_data(validated_data)
#         if UtilityModuleTbl.objects.filter(tenant=validated_data["tenant"], utility=validated_data["utility"],
#                                            label=validated_data["label"]).exists():
#             return False
#         with transaction.atomic():
#             if 'tenant' in validated_data:
#                 tenant = validated_data.pop('tenant')
#             if 'utility' in validated_data:
#                 utility = validated_data.pop('utility')
#             utility_module_obj = super(UtilityModuleSerializer, self).create(validated_data)
#             utility_module_obj.updated_by = user.id
#             utility_module_obj.updated_date = timezone.now()
#             utility_module_obj.tenant_id = tenant
#             utility_module_obj.utility_id = utility
#             utility_module_obj.save()
#             return utility_module_obj
#
#     def update(self, instance, validated_data, user):
#         with transaction.atomic():
#             utility_module_obj = super(UtilityModuleSerializer, self).update(instance, validated_data)
#             utility_module_obj.updated_by = user.id
#             utility_module_obj.updated_date = timezone.now()
#             utility_module_obj.save()
#             return utility_module_obj
__author__ = "aki"

from django.db import transaction
from rest_framework import serializers
from django.utils import timezone
from v1.commonapp.views.settings_reader import SettingReader

setting_reader = SettingReader()
from v1.commonapp.serializers.module import ModuleShortViewSerializer
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.utility.models.utility_module import UtilityModule as UtilityModuleTbl
from v1.utility.views.common_functions import set_utility_module_validated_data
from v1.commonapp.views.custom_exception import CustomAPIException
from rest_framework import serializers, status


class UtilityModuleShortViewSerializer(serializers.ModelSerializer):
    module_id = ModuleShortViewSerializer(many=False, source='get_module')

    class Meta:
        model = UtilityModuleTbl
        fields = ('id_string', 'label', 'module_id')


class UtilityModuleViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer(read_only=True)
    utility = UtilityMasterViewSerializer(read_only=True)
    module_id = ModuleShortViewSerializer(many=False, source='get_module')
    created_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)
    updated_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)

    class Meta:
        model = UtilityModuleTbl
        fields = ('id_string', 'is_active', 'label', 'created_date', 'updated_date', 'subscription_id', 'module_id',
                  'tenant', 'utility',)


class UtilityModuleSerializer(serializers.ModelSerializer):
    tenant = serializers.UUIDField(required=True, source='tenant.id_string')
    utility = serializers.UUIDField(required=True, source='utility.id_string')
    module_id = serializers.UUIDField(required=True)

    class Meta:
        model = UtilityModuleTbl
        fields = ('id_string', 'label', 'tenant', 'utility', 'subscription_id', 'module_id', 'is_active', 'created_by',
                  'updated_by', 'created_date', 'updated_date')

    def create(self, validated_data, user):
        validated_data = set_utility_module_validated_data(validated_data)
        print("Inside Create",validated_data)
        if UtilityModuleTbl.objects.filter(tenant=validated_data["tenant"], utility=validated_data["utility"],
                                           module_id=validated_data["module_id"]).exists():
            raise CustomAPIException("Module Already Exist", status_code=status.HTTP_409_CONFLICT)
        else:
            with transaction.atomic():
                if 'tenant' in validated_data:
                    tenant = validated_data.pop('tenant')
                if 'utility' in validated_data:
                    utility = validated_data.pop('utility')
                print("Iinside Transaction")
                utility_module_obj = super(UtilityModuleSerializer, self).create(validated_data)
                print("In create", utility_module_obj)
                utility_module_obj.updated_by = user.id
                utility_module_obj.updated_date = timezone.now()
                utility_module_obj.tenant_id = tenant
                utility_module_obj.utility_id = utility
                utility_module_obj.save()
                return utility_module_obj

    def update(self, instance, validated_data, user):
        if UtilityModuleTbl.objects.filter(tenant=validated_data["tenant"], utility=validated_data["utility"],
                                           module_id=validated_data["module_id"]).exists():
            raise CustomAPIException("Module Already Exist", status_code=status.HTTP_409_CONFLICT)
        else:
            with transaction.atomic():
                utility_module_obj = super(UtilityModuleSerializer, self).update(instance, validated_data)
                utility_module_obj.updated_by = user.id
                utility_module_obj.updated_date = timezone.now()
                utility_module_obj.save()
                return utility_module_obj