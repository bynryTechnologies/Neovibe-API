import uuid
from datetime import datetime
from django.db import models
from v1.consumer.models.offer_sub_type import get_offer_sub_type_by_id
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from v1.utility.models.utility_module import get_utility_module_by_id
from v1.utility.models.utility_sub_module import get_utility_submodule_by_id
from django.contrib.postgres.fields import JSONField
from django.utils import timezone # importing package for datetime


class ConsumerOfferMaster(models.Model):
    CHOICES = (
        (0, 'CREDIT'),
        (1, 'DEBIT'),
    )
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility_product_id = models.BigIntegerField(null=True, blank=True)
    module_id = models.BigIntegerField(null=True, blank=True)
    submodule_id = models.BigIntegerField(null=True, blank=True)
    offer_name = models.CharField(max_length=200, null=True, blank=True)
    offer_type_id = models.BigIntegerField(null=True, blank=True)
    offer_sub_type_id = models.BigIntegerField(null=True, blank=True)
    offer_code = models.CharField(max_length=200, null=True, blank=True)
    offer_image = models.CharField(max_length=200, null=True, blank=True)
    offer_max_amount = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=4)
    offer_percentage = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=4)
    description = models.CharField(max_length=2000, null=True, blank=True)
    effective_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    expiry_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    category = models.BigIntegerField(choices=CHOICES, default=0)
    service_obj = JSONField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.offer_code

    def __unicode__(self):
        return self.offer_code

    @property
    def get_offer_sub_type(self):
        return get_offer_sub_type_by_id(self.offer_sub_type_id)

    @property
    def get_sub_module(self):
        return get_utility_submodule_by_id(self.submodule_id)

    @property
    def get_module(self):
        return get_utility_module_by_id(self.module_id)


def get_consumer_offer_master_by_id_string(id_string):
    try:
        return ConsumerOfferMaster.objects.get(id_string=id_string)
    except:
        return False


def get_consumer_offer_master_by_id(id):
    try:
        return ConsumerOfferMaster.objects.get(id=id,is_active=True)
    except:
        return False


def get_consumer_emi_offer_master_by_id(id):
    try:
        return ConsumerOfferMaster.objects.get(id=id,is_active=True,category=1)
    except:
        return False
