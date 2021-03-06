# Table Header
# module : Tenant
# Table Type : Lookup (Global)
# Table Name :
# Description : It is a global lookup table that stores the states with countries with respect to tenants
# Frequency of data changes : Low
# Sample Table Data : Maharashtra, Assam, Bihar.
# Reference Table :
# Author : Saloni Monde
# Creation Date : 05-05-2020

import uuid  # importing package for guid
from datetime import datetime  # importing package for datetime
from django.db import models  # importing package for database
from django.utils import timezone # importing package for datetime


# Create Tenant State table start

class TenantState(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    tenant_country_id = models.BigIntegerField(blank=True, null=True)
    tenant_region_id = models.BigIntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

# Create Tenant State table end


def get_tenant_state_by_id(id):
    try:
        return TenantState.objects.get(id=id)
    except:
        return False


def get_tenant_state_by_id_string(id_string):
    try:
        return TenantState.objects.get(id_string=id_string)
    except:
        return False



