# Table Header
# module : All modules & sub-modules
# Table Type : Lookup (Global)
# Table Name : 2.12.5 Country
# Description : A global lookup table that stores countries within the regions
# Frequency of data changes : Low
# Sample Table Data : India
# Reference Table : 2.3.1. Consumer Master, 2.3.2. Consumer - Registration, 2.7.7. Branch details, 2.5.3. Vendor Details
# Author : Jayshree Kumbhare
# Creation Date : 21-04-2020

# change history
# <ddmmyyyy><changes><author>

import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from django.db import models  # importing package for database
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster

# Create Country table start


class Country(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    key = models.CharField(max_length=200,blank=True, null=True)
    name = models.CharField(max_length=200, blank=False, null=False)
    region = models.BigIntegerField(null=False, blank=False)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

# Create Country table end


def get_country_by_id_string(id_string):
    return Country.objects.get(id_string = id_string)


def get_country_by_id(id):
    return Country.objects.get(id = id)

# End the Code
