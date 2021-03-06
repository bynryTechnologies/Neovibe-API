from rest_framework import serializers,status
from v1.payment.models.payment_mode import PaymentMode as PaymentModeTbl
from django.db import transaction
from v1.payment.views.common_functions import set_payment_mode_validated_data
from datetime import datetime
from api.messages import PAYMENT_MODE_ALREADY_EXIST
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.utility.models.utility_payment_mode import UtilityPaymentMode as UtilityPaymentModeTbl


class PaymentModeListSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentModeTbl
        fields = ('name', 'id_string','is_active','created_by','created_date')


class PaymentModeViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = UtilityPaymentModeTbl
        fields = ('id_string', 'name', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string')


class PaymentModeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200,
                                 error_messages={"required": "The field name is required."})
    utility_id = serializers.CharField(required=False, max_length=200)
    tenant_id = serializers.CharField(required=False, max_length=200)
    payment_mode_id = serializers.CharField(required=False, max_length=200)
    # utility_product_id = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = UtilityPaymentModeTbl
        fields = '__all__'

    def create(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_payment_mode_validated_data(validated_data)
            if UtilityPaymentModeTbl.objects.filter(name=validated_data['name'], tenant_id=validated_data['tenant_id'],
                                        utility_id=validated_data['utility_id']).exists():
                raise CustomAPIException(PAYMENT_MODE_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:
                
                payment_mode_obj = super(PaymentModeSerializer, self).create(validated_data)
                payment_mode_obj.created_by = user.id
                payment_mode_obj.created_date = datetime.utcnow()
                payment_mode_obj.save()
                return payment_mode_obj

    def update(self, instance, validated_data, user):
        validated_data = set_payment_mode_validated_data(validated_data)
        with transaction.atomic():
            payment_mode_obj = super(PaymentModeSerializer, self).update(instance, validated_data)
            payment_mode_obj.tenant = user.tenant
            payment_mode_obj.updated_by = user.id
            payment_mode_obj.updated_date = datetime.utcnow()
            payment_mode_obj.save()
            return payment_mode_obj