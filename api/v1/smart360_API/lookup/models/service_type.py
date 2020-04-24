# Table Header
# Table Type : Lookup (Local)
# Table Name : 2.12.73 Service Type
# Description : Service type and ID of Service type to be used by Operator or Utility
# Frequency of data changes : Low
# Sample Table Data : Installation, Conversion, Repair, Maintenance, Outage, Emergency, Meter Reading.
# Reference Table : 2.6.2 SOP Master
# Author : Jayshree Kumbhare
# Creation Date : 22/04/2020

# change history
# <ddmmyyyy>-<changes>-<Author>

import datetime  # importing package for datetime
import uuid  # importing package for GUID

from django.db import models  # importing package for database


# Create Service Type table start

class ServiceType(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    name = models.CharField(max_length=200, blank=False, null=False)
    created_by = models.IntegerField(null=False, blank=False)
    updated_by = models.IntegerField(null=False, blank=False)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def __unicode__(self):
<<<<<<< HEAD
        return self.name

# Create Service Type table end
=======
        return self.service_type

def get_service_type_by_id_string(id_string):
    return ServiceType.objects.get(id_string = id_string)
# End the Code
>>>>>>> a2d5c7e1cef5f059ef038fd4cea4a92035bc8c68
