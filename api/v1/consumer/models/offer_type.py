import uuid
from datetime import datetime
from django.db import models
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.utils import timezone # importing package for datetime


class OfferType(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL,related_name='offer_type_tenant')
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL,related_name='offer_type_utility')
    name = models.CharField(max_length=200, blank=False, null=False)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


def get_offer_type_by_id_string(id_string):
    try:
        return OfferType.objects.get(id_string = id_string)
    except:
        return False


def get_offer_type_by_id(id):
    try:
        return OfferType.objects.get(id = id)
    except:
        return False