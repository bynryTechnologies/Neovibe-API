__author__ = "Arpita"

from rest_framework import serializers

from v1.tenant.models.tenant_master import TenantMaster


class TenantSerializer(serializers.ModelSerializer):

    class Meta:
        model = TenantMaster
        fields = ('name', 'id_string')
