# table header
# module: Utility | sub-module - All
# table type : Master
# table name :
# table description :  It will contain details of Modules available for the given Tenant
# frequency of data changes : Medium
# sample tale data : "Sub-Module1"
# reference tables :
# author : Saloni Monde
# created on : 05-05-2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime  # importing package for datetime
from v1.commonapp.models.module import get_module_by_id
from v1.commonapp.models.sub_module import get_sub_module_by_id
from v1.tenant.models.tenant_master import TenantMaster
from django.db import models  # importing package for database
from django.utils import timezone # importing package for datetime

# Create Tenant Sub-Module table start.


class TenantSubModule(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    module_id = models.BigIntegerField(null=True, blank=True)
    sub_module_id = models.BigIntegerField(null=True, blank=True)
    subscription_id = models.BigIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)

    def __str__(self):
        return str(self.sub_module_id)

    def __unicode__(self):
        return str(self.sub_module_id)

    @property
    def get_module(self):
        module = get_module_by_id(self.module_id)
        print("MODULE",module)
        return module

    @property
    def get_sub_module(self):
        sub_module = get_sub_module_by_id(self.sub_module_id)
        print("SUBMODULE",sub_module)
        return sub_module


# Create Utility Sub Module table end.


def get_tenant_submodule_by_id(id):
    try:
        return TenantSubModule.objects.get(id=id)
    except:
        return False


def get_tenant_submodule_by_id_string(id_string):
    try:
        return TenantSubModule.objects.get(id_string=id_string)
    except:
        return False
