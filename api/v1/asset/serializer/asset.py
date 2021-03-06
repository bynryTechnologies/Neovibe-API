__author__ = "Priyanka"

from v1.commonapp.views.settings_reader import SettingReader
setting_reader = SettingReader()
from rest_framework import serializers
from datetime import datetime
from django.db import transaction
from v1.asset.models.asset_master import Asset as AssetTbl
from v1.asset.models.asset_status import AssetStatus as AssetStatusTbl
from v1.asset.views.common_function import set_asset_validated_data
from django.db import transaction
from v1.asset.serializer.asset_status import AssetStatusListSerializer
from v1.asset.serializer.category import AssetCategoryListSerializer
from v1.asset.serializer.sub_category import AssetSubCategoryListSerializer
from v1.commonapp.serializers.city import CitySerializer
from v1.commonapp.serializers.area import AreaListSerializer
from v1.commonapp.serializers.sub_area import SubAreaListSerializer


class AssetShortListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetTbl
        fields = ('name','id_string')


class AssetListSerializer(serializers.ModelSerializer):

    tenant_name = serializers.ReadOnlyField(source='tenant.name')
    category_id = AssetCategoryListSerializer(many=False, required=True, source='get_category')
    sub_category_id = AssetSubCategoryListSerializer(many=False, required=True, source='get_sub_category')
    status_id = AssetStatusListSerializer(many=False, required=True, source='get_status')
    city_id = CitySerializer(many=False, required=True, source='get_city')
    area_id = AreaListSerializer(many=False, required=True, source='get_area')
    sub_area_id = SubAreaListSerializer(many=False, required=True, source='get_sub_area')
    manufacturing_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)
    installation_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)
    expiry_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)
    created_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)

    class Meta:
        model = AssetTbl
        fields = ('id_string', 'tenant_name', 'name', 'asset_no', 'description', 'address', 'serial_no', 'manufacturer', 'make',
            'model', 'lat', 'long', 'manufacturing_date',
            'installation_date', 'expiry_date', 'asset_life', 'asset_value', 'deprecation_method', 'deprecation_rate',
            'flag',
             'city_id', 'area_id', 'sub_area_id', 'category_id', 'sub_category_id','status_id','created_date')


class AssetViewSerializer(serializers.ModelSerializer):

    tenant_name = serializers.ReadOnlyField(source='tenant.name')
    manufacturing_date = serializers.DateTimeField(format=setting_reader.get_display_date_format())
    installation_date = serializers.DateTimeField(format=setting_reader.get_display_date_format())
    expiry_date = serializers.DateTimeField(format=setting_reader.get_display_date_format())
    created_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(),read_only=True)
    category_id = AssetCategoryListSerializer(many=False, required=True, source='get_category')
    sub_category_id = AssetSubCategoryListSerializer(many=False, required=True, source='get_sub_category')
    status_id = AssetStatusListSerializer(many=False, required=True, source='get_status')
    city_id = CitySerializer(many=False, required=True, source='get_city')
    area_id = AreaListSerializer(many=False, required=True, source='get_area')
    sub_area_id = SubAreaListSerializer(many=False, required=True, source='get_sub_area')



    class Meta:
        model = AssetTbl
        fields = ('id_string', 'tenant_name', 'name', 'asset_no', 'description', 'address', 'serial_no', 'manufacturer', 'make',
            'model', 'lat', 'long', 'manufacturing_date','installation_date', 'expiry_date', 'asset_life', 'asset_value', 'deprecation_method', 'deprecation_rate',
            'flag','city_id', 'area_id', 'sub_area_id', 'category_id', 'sub_category_id','status_id','created_date')


class AssetSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False, max_length=200)
    asset_no = serializers.CharField(required=False, max_length=200)
    description = serializers.CharField(required=False, max_length=200)
    serial_no = serializers.CharField(required=False, max_length=200)
    manufacturer = serializers.CharField(required=False, max_length=200)
    make = serializers.CharField(required=False, max_length=200)
    model = serializers.CharField(required=False, max_length=200)
    city_id = serializers.CharField(required=False, max_length=200)
    area_id = serializers.CharField(required=False, max_length=200)
    sub_area_id = serializers.CharField(required=False, max_length=200)
    address = serializers.CharField(required=False, max_length=200)
    category_id = serializers.CharField(required=False, max_length=200)
    sub_category_id = serializers.CharField(required=False, max_length=200)
    lat = serializers.CharField(required=False, max_length=200)
    long = serializers.CharField(required=False, max_length=200)
    manufacturing_date = serializers.DateTimeField(format="%Y-%m-%d")
    installation_date = serializers.DateTimeField(format="%Y-%m-%d")
    expiry_date = serializers.DateTimeField(format="%Y-%m-%d")
    asset_life = serializers.CharField(required=False, max_length=200)
    asset_value = serializers.CharField(required=False, max_length=200)
    deprecation_method = serializers.CharField(required=False, max_length=200)
    deprecation_rate = serializers.CharField(required=False, max_length=200)
    status_id = serializers.CharField(required=False, max_length=200)
    flag = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = AssetTbl
        fields =  ('__all__')


    def create(self, validated_data, user):
        validated_data = set_asset_validated_data(validated_data)
        if AssetTbl.objects.filter(**validated_data).exists():
            return False
        else:
            with transaction.atomic():
                asset_obj = super(AssetSerializer, self).create(validated_data)
                asset_obj.created_by = user.id
                asset_obj.tenant = user.tenant
                asset_obj.utility = user.utility
                asset_obj.save()
                asset_no = str(asset_obj.name) + str(asset_obj.tenant) + str(asset_obj.utility)
                asset_obj.asset_no = asset_no
                asset_obj.save()
                return asset_obj

    def update(self, instance, validated_data, user):
            validated_data = set_asset_validated_data(validated_data)
            with transaction.atomic():
                asset_obj = super(AssetSerializer, self).update(instance, validated_data)
                asset_obj.updated_by = user.id
                asset_obj.updated_date = datetime.now()
                asset_obj.save()
                return asset_obj