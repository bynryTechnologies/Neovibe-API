from rest_framework import serializers
from v1.commonapp.models.sub_area import SubArea


class SubAreaListSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubArea
        fields = ('name', 'id_string')


class SubAreaViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = SubArea
        fields = ('id_string', 'name', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string')