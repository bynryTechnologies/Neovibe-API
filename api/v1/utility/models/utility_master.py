__author__ = "aki"

# table header
# module: Utility | sub-module - All
# table type : Master
# table name : 2.1  Utility Master  `  
# table description : It is Utility Master table. It will contain details for Utility details
# frequency of data changes : Low
# sample tale data : "BGCL1","BGCL2","BGCL3",
# reference tables :
# author : Gauri Deshmukh
# created on : 24/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from django.db import models  # importing package for database


# Create Utility Master table start.

class UtilityMaster(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    short_name = models.CharField(max_length=200, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    phone_no = models.CharField(max_length=200, blank=True, null=True)
    email_id = models.CharField(max_length=200, blank=True, null=True)
    company_id = models.CharField(max_length=200, blank=True, null=True)
    pan_no = models.CharField(max_length=200, blank=True, null=True)
    tax_id = models.CharField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    short_logo = models.CharField(max_length=200, blank=True, null=True)
    long_logo = models.CharField(max_length=200, blank=True, null=True)
    status_id = models.BigIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name + " " + str(self.id_string)

    def __unicode__(self):
        return self.name

    def get_tenant(self):
        return self.tenant

# Create Utility Master table end.


def get_utility_by_id(id):
    try:
        return UtilityMaster.objects.get(id = id)
    except:
        return False


def get_utility_by_id_string(id_string):
    try:
        return UtilityMaster.objects.get(id_string=id_string, is_active=True)
    except:
        return False


def get_utility_by_name(name):
    utility = UtilityMaster.objects.get(name=name)
    return utility.id