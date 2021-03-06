__author__ = "aki"

# table header
# module: Utility | sub-module - All
# table type : Master
# table name : 2.4 Utility SubModule
# table description :  It will contain details of Modules available for the given Utility
# frequency of data changes : Medium
# sample tale data : "Plan - A"
# reference tables : 2.1 Utility Master, 2.3. Utility Module
# author : Akshay
# created on : 24/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime  # importing package for datetime
from v1.commonapp.models.module import get_module_by_id
from v1.commonapp.models.sub_module import get_sub_module_by_id
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from v1.utility.models.utility_module import get_utility_module_by_id
from django.db import models  # importing package for database
from django.utils import timezone # importing package for datetime



# Create Utility Sub Module table start.

class UtilitySubModule(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    module_id = models.BigIntegerField(null=True, blank=True)
    submodule_id = models.BigIntegerField(null=True, blank=True)
    label = models.CharField(max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.label)

    def __unicode__(self):
        return str(self.label)

    @property
    def get_module(self):
        module = get_utility_module_by_id(self.module_id)
        return module

    @property
    def get_modules(self):
        module = get_module_by_id(self.module_id)
        return module

    @property
    def get_submodule(self):
        submodule = get_sub_module_by_id(self.submodule_id)
        return submodule


# Create Utility Sub Module table end.


def get_utility_submodule_by_id(id):
    try:
        return UtilitySubModule.objects.get(id=id)
    except:
        return False


def get_utility_submodule_by_id_string(id_string):
    try:
        return UtilitySubModule.objects.get(id_string=id_string)
    except:
        return False


def get_utility_submodules_by_tenant_id_string(id_string):
    return UtilitySubModule.objects.filter(tenant__id_string=id_string)


def get_utility_submodules_by_utility_id_string(id_string):
    return UtilitySubModule.objects.filter(utility__id_string=id_string)


def get_utility_submodules_by_module_id(id):
    return UtilitySubModule.objects.filter(module_id=id)

def get_utility_submodules_by_module_id_and_tenant_id_string(id,id_string):
    return UtilitySubModule.objects.filter(module_id=id,tenant__id_string=id_string)