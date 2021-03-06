from datetime import datetime
from django.db import transaction
from rest_framework import serializers
from v1.payment.models.payment import Payment
from v1.payment.serializer.payment_channel import PaymentChannelListSerializer
from v1.payment.serializer.payment_mode import PaymentModeListSerializer
from v1.payment.serializer.payment_sub_type import PaymentSubTypeListSerializer
from v1.payment.serializer.payment_type import PaymentTypeListSerializer
from v1.payment.views.common_functions import generate_receipt_no, set_payment_validated_data


class ChoiceField(serializers.ChoiceField):

    def to_representation(self, obj):
        return self._choices[obj]


class PaymentListSerializer(serializers.ModelSerializer):
    payment_type = PaymentTypeListSerializer(many=False, source='get_payment_type')
    # payment_sub_type = PaymentSubTypeListSerializer(many=False, source='get_payment_sub_type')
    payment_mode = PaymentModeListSerializer(many=False, source='get_payment_mode')
    payment_channel = PaymentChannelListSerializer(many=False, source='get_payment_channel')
    state = ChoiceField(choices=Payment.CHOICES)

    class Meta:
        model = Payment
        fields = ('id_string', 'transaction_amount', 'transaction_charges', 'state', 'payment_type',
                  'payment_mode', 'payment_channel', 'transaction_id', 'transaction_date')


class PaymentViewSerializer(serializers.ModelSerializer):
    payment_type = PaymentTypeListSerializer(many=False, source='get_payment_type')
    # payment_sub_type = PaymentSubTypeListSerializer(many=False, source='get_payment_sub_type')
    payment_mode = PaymentModeListSerializer(many=False, source='get_payment_mode')
    payment_channel = PaymentChannelListSerializer(many=False, source='get_payment_channel')
    state = ChoiceField(choices=Payment.CHOICES)

    class Meta:
        model = Payment
        fields = ('id_string', 'consumer_no' ,'identification_id', 'transaction_amount', 'transaction_charges', 'transaction_id', 'state', 'payment_type',
                  'payment_mode', 'payment_channel','created_date')


class PaymentSerializer(serializers.ModelSerializer):
    utility = serializers.CharField(required=False, max_length=200)
    payment_type_id = serializers.CharField(required=False, max_length=200)
    payment_mode_id = serializers.CharField(required=False, max_length=200)
    payment_channel_id = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = Payment
        fields = '__all__'

    def create(self, validated_data, obj, user):
        validated_data = set_payment_validated_data(validated_data)
        with transaction.atomic():
            payment = super(PaymentSerializer, self).create(validated_data)
            payment.identification_id = obj.id
            payment.tenant = obj.tenant
            payment.utility = obj.utility
            payment.receipt_no = generate_receipt_no(payment)
            payment.created_by = user.id
            payment.created_date = datetime.utcnow()
            payment.is_active = True
            payment.save()
            return payment

    def update(self, instance, validated_data, user):
        validated_data = set_payment_validated_data(validated_data)
        with transaction.atomic():
            payment = super(PaymentSerializer, self).update(instance, validated_data)
            payment.updated_by = user.id
            payment.updated_date = datetime.utcnow()
            payment.save()
        return payment
