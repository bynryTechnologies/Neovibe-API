__author__ = 'priyanka'

import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from v1.campaign.models.campaign import Campaign
from v1.campaign.models.campaign_status import CampaignStatus
from v1.consumer.models.consumer_category import ConsumerCategory
from v1.consumer.models.consumer_sub_category import ConsumerSubCategory
from v1.commonapp.models.frequency import Frequency




class CampaignTestCase(APITestCase):

    # dummy data to save in test database
    def setUp(self):
        self.valid_payload = {
            "tenant":1,
            "campaign_name":"Smart360 UnitTesting",
            "start_date":"2020-06-13",
            "end_date":"2020-07-10",
            "description":"This is for UnitTesting of POST Method ",
            "frequency_id_string":"1874cf50-c3d7-478f-b6c3-5814062f1873",
            "potential_consumers":500,
            "actual_consumers":400,
            "budget_amount":1000,
            "actual_amount":500,

        }
        self.invalid_payload = {
            "tenant": "",
            "campaign_name":"Smart360 UnitTesting",
            "start_date":"2020-06-13",
            "end_date":"2020-07-10",
            "description":"This is for UnitTesting of POST Method ",
            "frequency_id_string":"",
        }

        self.update_payload = {
            "tenant": "1",
            "campaign_name":"Smart360 UnitTesting",
            "start_date":"2021-01-01",
            "end_date":"2021-02-01",
        }

    # for save valid campaign details
    def create_valid_campaign(self):
        tenant_obj = TenantMaster.objects.create(name="tenant_test")
        User.objects.create(tenant=tenant_obj,user_type_id=1, user_subtype_id=1, form_factor_id=1, middle_name="Testing")
        response = self.client.post("api/v1/campaign/", self.valid_payload)
        print("response",response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # for save invalid campaign details and through error
    def create_invalid_campaign(self):
        tenant_obj = TenantMaster.objects.create(name="tenant_test")
        User.objects.create(tenant=tenant_obj,user_type_id=1, user_subtype_id=1,form_factor_id=1,middle_name="Testing")
        response = self.client.post("api/v1/campaign/", self.invalid_payload)
        print("response",response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # for getting all campaign list by search, filter, and total records
    def get_all_campaign(self):
        tenant_obj = TenantMaster.objects.create(name="tenant_test")
        User.objects.create(tenant=tenant_obj,user_type_id=1,user_subtype_id=1,form_factor_id=1,middle_name="Testing")
        CampaignStatus.objects.create(tenant=tenant_obj,name="Created")
        ConsumerCategory.objects.create(tenant=tenant_obj,name="Domestic")
        ConsumerSubCategory.objects.create(tenant=tenant_obj,name="Builder",category=1)
        Frequency.objects.create(tenant=tenant_obj,name="Frequency")
        Campaign.objects.create(tenant=tenant_obj,name="Testing TDD")
        response = self.client.get(reverse('campaign_list'))
        print("response",response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # for getting single campaign details
    def get_single_campaign(self):
        tenant_obj = TenantMaster.objects.create(name="tenant_test")
        campaign_obj = Campaign.objects.create(tenant=tenant_obj,category_id=1,sub_category_id=1,frequency_id=1)
        ConsumerCategory.objects.create(tenant=tenant_obj, name="Domestic")
        ConsumerSubCategory.objects.create(tenant=tenant_obj, name="Builder",category=1)
        Frequency.objects.create(tenant=tenant_obj, name="Frequency")
        response = self.client.get(reverse('campaign_detail', args=[campaign_obj.id_string]))
        print("response",response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # for update single campaign record
    def update_valid_campaign(self):
        tenant_obj = TenantMaster.objects.create(name="tenant_test")
        campaign_obj = Campaign.objects.create(tenant=tenant_obj)
        response = self.client.put(reverse('campaign_data', args=[campaign_obj.id_string]), self.update_payload)
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# you can print API response in foloowing three different ways.
# print("response",response.content)
# print("response data", response.data)
# print("response json",json.loads(response.content))