__author__ = "Arpita"
from django.db import transaction
from rest_framework import serializers

from v1.commonapp.models.document import Document
from v1.commonapp.models.notes import Notes
from v1.commonapp.serializers.module import ModuleSerializer
from v1.commonapp.serializers.service_type import ServiceTypeSerializer
from v1.commonapp.serializers.sub_module import SubModuleSerializer
from v1.tenant.serializers.tenant import TenantSerializer
from v1.userapp.serializers.user import UserSerializer, GetUserSerializer
from v1.userapp.views.common_functions import set_note_validated_data
from v1.utility.serializers.utility import UtilitySerializer


class NoteViewSerializer(serializers.ModelSerializer):
    tenant = TenantSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')
    module = ModuleSerializer(many=False, required=True, source='get_module')
    sub_module = SubModuleSerializer(many=False, required=True, source='get_sub_module')
    service_type = ServiceTypeSerializer(many=False, required=True, source='get_service_type')

    class Meta:
        model = Notes
        fields = ('id_string', 'tenant', 'utility', 'module', 'sub_module', 'service_type', 'note_name', 'note_color',
                  'note', 'is_active', 'created_date')


class NoteSerializer(serializers.ModelSerializer):
    module_id = serializers.CharField( required=False, max_length=200)
    sub_module_id = serializers.CharField(required=False, max_length=200)
    service_type_id = serializers.CharField(required=False, max_length=200)
    identification_id = serializers.CharField(required=False, max_length=200)
    note_name = serializers.CharField(required=False, max_length=200)
    note_color = serializers.CharField(required=False, max_length=200)
    note = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = Notes
        fields = '__all__'

    def create(self, validated_data, user):
        validated_data =  set_note_validated_data(validated_data)
        with transaction.atomic():
            note = super(NoteSerializer, self).create(validated_data)
            note.identification_id = user.id
            note.created_by = user.id
            note.tenant = user.tenant
            note.utility = user.utility
            note.is_active = True
            note.save()
            return note


class NoteListSerializer(serializers.ModelSerializer):
    tenant = TenantSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')
    module = ModuleSerializer(many=False, required=True, source='get_module')
    sub_module = SubModuleSerializer(many=False, required=True, source='get_sub_module')
    service_type = ServiceTypeSerializer(many=False, required=True, source='get_service_type')
    identification = UserSerializer(many=False, required=True, source='get_user_identification')

    class Meta:
        model = Document
        fields = ('id_string', 'tenant', 'utility', 'module', 'sub_module', 'service_type', 'identification',
                  'note_name', 'note_color', 'note', 'status', 'is_active', 'created_by', 'created_date')
