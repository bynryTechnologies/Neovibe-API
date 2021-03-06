__author__ = "Priyanka"

from v1.commonapp.views.settings_reader import SettingReader
setting_reader = SettingReader()
from rest_framework import serializers
from v1.campaign.models.campaign import Campaign as CampaignTbl
from v1.campaign.models.campaign_status import CampaignStatus
from v1.campaign.models.campaign_objective import CampaignObjective
from v1.campaign.models.campaign_group import CampaignGroup
from v1.campaign.views.common_functions import set_validated_data
from datetime import datetime
from django.db import transaction
from v1.commonapp.serializers.area import AreaListSerializer
from v1.commonapp.serializers.sub_area import SubAreaListSerializer
from v1.consumer.serializers.consumer_category import ConsumerCategoryListSerializer
from v1.consumer.serializers.consumer_sub_category import ConsumerSubCategoryListSerializer
from v1.commonapp.serializers.frequency import FrequencySerializer

class CampaignGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = CampaignGroup
        fields = ('name','id_string')

class CampaignObjectiveSerializer(serializers.ModelSerializer):

    class Meta:
        model = CampaignObjective
        fields = ('name','id_string')

class CampaignStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = CampaignStatus
        fields = ('name','id_string')


class CampaignListSerializer(serializers.ModelSerializer):

    def get_created_date(self, obj):
        return obj.created_date.strftime(setting_reader.get_display_date_format())

    def get_start_date(self, obj):
        return obj.start_date.strftime(setting_reader.get_display_date_format())

    def get_end_date(self, obj):
        return obj.end_date.strftime(setting_reader.get_display_date_format())


    group_id = CampaignGroupSerializer(many=False, required=True, source='get_group')
    objective_id = CampaignObjectiveSerializer(many=False, required=True, source='get_objective')
    status_id = CampaignStatusSerializer(many=False, required=True, source='get_status')
    tenant_name = serializers.ReadOnlyField(source='tenant.name')
    frequency_id = FrequencySerializer(many=False, required=True, source='get_frequency')
    category_id = ConsumerCategoryListSerializer(many=False, required=True, source='get_category')
    sub_category_id = ConsumerSubCategoryListSerializer(many=False, required=True, source='get_sub_category')
    area_id = AreaListSerializer(many=False, required=True, source='get_area')
    sub_area_id = SubAreaListSerializer(many=False, required=True, source='get_sub_area')
    created_date = serializers.SerializerMethodField('get_created_date')
    start_date = serializers.SerializerMethodField('get_start_date')
    end_date = serializers.SerializerMethodField('get_end_date')

    class Meta:
        model = CampaignTbl
        fields = ('id_string', 'tenant_name', 'name', 'description', 'start_date', 'end_date',
                  'potential_consumers', 'actual_consumers', 'budget_amount', 'actual_amount', 'frequency_id',
                  'category_id',
                  'sub_category_id', 'area_id', 'sub_area_id', 'objective_id', 'group_id', 'status_id','created_date',
                  'is_active')


class CampaignViewSerializer(serializers.ModelSerializer):

    # def get_start_date(self, obj):
    #     start_date = datetime.strptime(obj.start_date , setting_reader.get_display_date_format())
    #     return start_date
    #
    # def get_end_date(self, obj):
    #     end_date = datetime.strptime(obj.end_date, setting_reader.get_display_date_format())
    #     return end_date

    group_id = CampaignGroupSerializer(many=False, required=True, source='get_group')
    objective_id = CampaignObjectiveSerializer(many=False, required=True, source='get_objective')
    status_id = CampaignStatusSerializer(many=False, required=True, source='get_status')
    tenant_name = serializers.ReadOnlyField(source='tenant.name')
    frequency_id = FrequencySerializer(many=False, required=True, source='get_frequency')
    category_id = ConsumerCategoryListSerializer(many=False, required=True, source='get_category')
    sub_category_id = ConsumerSubCategoryListSerializer(many=False, required=True, source='get_sub_category')
    area_id = AreaListSerializer(many=False, required=True, source='get_area')
    sub_area_id = SubAreaListSerializer(many=False, required=True, source='get_sub_area')
    created_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)
    start_date = serializers.DateTimeField(format=setting_reader.get_display_date_format())
    end_date = serializers.DateTimeField(format=setting_reader.get_display_date_format())

    class Meta:
        model = CampaignTbl
        fields = ('id_string', 'tenant_name', 'name',  'description','start_date','end_date',
                  'potential_consumers','actual_consumers','budget_amount','actual_amount','frequency_id','category_id',
                  'sub_category_id','area_id','sub_area_id','objective_id','group_id','status_id',
                  'is_active','created_date')


class CampaignSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False, max_length=200)
    group_id = serializers.CharField(required=False, max_length=200)
    objective_id = serializers.CharField(required=False, max_length=200)
    description = serializers.CharField(required=False, max_length=200)
    frequency_id = serializers.CharField(required=False, max_length=200)
    potential_consumers = serializers.CharField(required=False, max_length=200)
    actual_consumers = serializers.CharField(required=False, max_length=200)
    budget_amount = serializers.CharField(required=False, max_length=200)
    actual_amount = serializers.CharField(required=False, max_length=200)
    category_id = serializers.CharField(required=False, max_length=200)
    sub_category_id = serializers.CharField(required=False, max_length=200)
    start_date = serializers.DateTimeField(format="%Y-%m-%d")
    end_date = serializers.DateTimeField(format="%Y-%m-%d")
    area_id = serializers.CharField(required=False, max_length=200)
    sub_area_id = serializers.CharField(required=False, max_length=200)
    status_id = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = CampaignTbl
        fields =  ('id_string', 'name', 'group_id','objective_id', 'description',
                  'frequency_id','potential_consumers','actual_consumers','budget_amount','actual_amount','category_id',
                  'sub_category_id','start_date','end_date','area_id','sub_area_id','status_id')

    def create(self, validated_data, user):
        validated_data = set_validated_data(validated_data)
        if CampaignTbl.objects.filter(**validated_data).exists():
            return False
        else:
            with transaction.atomic():
                campaign_obj = super(CampaignSerializer, self).create(validated_data)
                campaign_obj.created_by = user.id
                # campaign_obj.created_date = datetime.now()
                campaign_obj.tenant = user.tenant
                campaign_obj.utility = user.utility
                campaign_obj.save()
                return campaign_obj

    def update(self, instance, validated_data, user):
            validated_data = set_validated_data(validated_data)
            with transaction.atomic():
                campaign_obj = super(CampaignSerializer, self).update(instance, validated_data)
                campaign_obj.updated_by = user.id
                # campaign_obj.updated_date = datetime.now()
                campaign_obj.save()
                return campaign_obj