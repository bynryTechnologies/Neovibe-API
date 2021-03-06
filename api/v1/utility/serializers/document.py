__author__ = "Aki"

from rest_framework import serializers
from v1.commonapp.models.document import Document as DocumentTbl
from v1.commonapp.serializers.document_sub_type import DocumentSubTypeSerializer
from v1.commonapp.serializers.document_type import DocumentTypeSerializer
from v1.tenant.serializers.tenant import TenantMasterSerializer
from v1.utility.serializers.utility import UtilitySerializer


class DocumentSerializer(serializers.ModelSerializer):
    tenant = TenantMasterSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')
    document_type = DocumentTypeSerializer(many=False, required=True, source='get_type')
    document_sub_type = DocumentSubTypeSerializer(many=False, required=True, source='get_sub_type')

    class Meta:
        model = DocumentTbl
        fields = ('id_string', 'tenant', 'utility', 'document_type', 'document_sub_type', 'name', 'link',
                  'is_active')

    def create(self, validated_data, user):
        document = super(DocumentSerializer, self).create(validated_data)
        document.created_by = user
        document.save()
        return document
