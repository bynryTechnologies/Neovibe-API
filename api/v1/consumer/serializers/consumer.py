from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from v1.consumer.models.consumer_master import ConsumerMaster
from v1.consumer.views.common_functions import *


class ConsumerViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = ConsumerMaster
        fields = ('__all__')


class ConsumerSerializer(serializers.ModelSerializer):
    country_id = serializers.CharField(required=False, max_length=200)
    state_id = serializers.CharField(required=False, max_length=200)
    city_id = serializers.CharField(required=False, max_length=200)
    cycle_id = serializers.CharField(required=False, max_length=200)
    route_id = serializers.CharField(required=False, max_length=200)
    scheme_id = serializers.CharField(required=False, max_length=200)
    area_id = serializers.CharField(required=False, max_length=200)
    sub_area_id = serializers.CharField(required=False, max_length=200)
    utility_service_plan_id = serializers.CharField(required=False, max_length=200)
    category_id = serializers.CharField(required=False, max_length=200)
    sub_category_id = serializers.CharField(required=False, max_length=200)
    consumer_status_id = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = ConsumerMaster
        validators = [UniqueTogetherValidator(queryset=ConsumerMaster.objects.all(), fields=('phone_mobile',),
                                              message='Consumer already exists!')]
        fields = ('__all__')

    def create(self, validated_data, user):
        validated_data =  set_consumer_validated_data(validated_data)
        with transaction.atomic():
            consumer_obj = super(ConsumerSerializer, self).create(validated_data)
            consumer_obj.tenant = user.tenant
            consumer_obj.utility = user.utility
            consumer_obj.consumer_no = consumer_obj.id
            consumer_obj.save()
            return consumer_obj

    def update(self, instance, validated_data, user):
        validated_data = set_consumer_validated_data(validated_data)
        with transaction.atomic():
            consumer_obj = super(ConsumerSerializer, self).update(instance, validated_data)
            return consumer_obj