# Table Header
# Module: Consumer Care | Sub-Module : Meter Reading, Billing
# Table Type : Master (Global)
# Table Name : 2.4.6. Consumer Token
# Description : All users unique tokens will be saved in this table along with user_id
# Frequency of data changes : High
# Sample table :
# Reference Table : None
# Author : Jayshree Kumbhare
# Creation Date : 23/04/2020


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster

from django.db import models  # importing package for database


# Create Consumer Token Table Start.

class ConsumerToken(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    consumer = models.BigIntegerField(null=True, blank=True)
    token = models.CharField(max_length=500, null=True, blank=True)
    form_factor = models.BigIntegerField(null=True, blank=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.token

    def __unicode__(self):
        return self.token

# Create Consumer Token table end.
