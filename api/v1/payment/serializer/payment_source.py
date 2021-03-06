from rest_framework import serializers
from v1.payment.models.payment_source import PaymentSource


class PaymentSourceListSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentSource
        fields = ('name', 'id_string')


class PaymentSourceViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = PaymentSource
        fields = ('id_string', 'name', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string')