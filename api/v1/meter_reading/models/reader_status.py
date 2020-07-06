# Table Header
# Table Type : Lookup (Local)
# Table Name : 2.12.54 Reader Status
# Description : Reader Status and ID of Reader Status  to be used by Operator or Utility
# Frequency of data changes : Low
# Sample Table Data : "Door lock", "Address not found"
# Reference Table : 2.3.8.4 Meter Reading
# Author : Jayshree Kumbhare
# Creation Date : 21-04-2020

from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
import uuid  # importing package for GUID
from django.db import models  # importing package for database


# Create Reader Status table start

class ReaderStatus(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, blank=False, null=False)
    meter_status_id = models.BigIntegerField(blank=False, null=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

# Create Reader Status table end


def get_reader_status_by_id(id):
    try:
        return ReaderStatus.objects.get(id=id)
    except:
        return False


def get_reader_status_by_id_string(id_string):
    try:
        return ReaderStatus.objects.get(id_string=id_string)
    except:
        return False
