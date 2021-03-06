import uuid
from datetime import datetime
from django.db import models
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.utils import timezone # importing package for datetime


class UtilityServiceContractTemplate(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    template_name = models.CharField(max_length=200, null=True, blank=True)
    terms_and_conditions = models.CharField(max_length=2000, null=True, blank=True)
    entity = models.CharField(max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.utility.name + " " + str(self.id_string)

    def __unicode__(self):
        return self.utility.name


def get_utility_service_contract_template_by_id_string(id_string):
    try:
        return UtilityServiceContractTemplate.objects.get(id_string=id_string)
    except:
        False


def get_utility_service_contract_template_by_id(id):
    try:
        return UtilityServiceContractTemplate.objects.get(id=id)
    except:
        False

