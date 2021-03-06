import uuid
from datetime import datetime
from django.db import models
from v1.consumer.models.consumer_category import get_consumer_category_by_id
from v1.consumer.models.consumer_sub_category import get_consumer_sub_category_by_id
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.contrib.postgres.fields import JSONField
from v1.utility.models.utility_product import get_utility_product_by_id
from django.utils import timezone # importing package for datetime



class UtilityServiceContractMaster(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, null=True, blank=True)
    service_obj = JSONField(null=True, blank=True)
    utility_product_id = models.BigIntegerField(null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    deposite_amount = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=4)
    consumer_category_id = models.BigIntegerField(null=True, blank=True)
    consumer_sub_category_id = models.BigIntegerField(null=True, blank=True)
    service_contract_template_id = models.BigIntegerField(null=True, blank=True)
    terms = models.CharField(max_length=1000, null=True, blank= True)
    duration = models.BigIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.utility.name + " " + str(self.id_string)

    def __unicode__(self):
        return self.utility.name


    @property
    def get_consumer_category(self):
        category = get_consumer_category_by_id(self.consumer_category_id)
        return category

    @property
    def get_consumer_sub_category(self):
        sub_category = get_consumer_sub_category_by_id(self.consumer_sub_category_id)
        return sub_category

    @property
    def get_utility_product_by_id(self):
        utility_product = get_utility_product_by_id(self.utility_product_id)
        return utility_product    


def get_utility_service_contract_master_by_id_string(id_string):
    try:
        return UtilityServiceContractMaster.objects.get(id_string=id_string)
    except:
        False


def get_utility_service_contract_master_by_id(id):
    try:
        return UtilityServiceContractMaster.objects.get(id=id)
    except:
        False
