# table header
# module: Work Order | sub-module -
# Table Type : Lookup (Global)
# Table Name : MaterialType
# Description : It is a global lookup table that stores Material Types.
# Frequency of data changes : Low
# Sample table :
# Reference Table :Material Type
# Author : Chinmay
# Creation Date : 23/12/2020

# change history
# <ddmmyyyy><changes><author>

import uuid  # importing package for guid
from datetime import datetime  # importing package for datetime
from django.db import models  # importing package for database

from v1.commonapp.views.custom_exception import ObjectNotFoundException
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.utils import timezone # importing package for datetime


# Create Material table start


class MaterialType(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, blank=False, null=False)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    @property
    def get_tenant(self):
        return self.tenant

    @property
    def get_utility(self):
        return self.utility


# Create Material Type table end

def get_material_type_by_tenant_id_string(id_string):
    return MaterialType.objects.filter(tenant__id_string=id_string)


def get_material_type_by_utility_id_string(id_string):
    return MaterialType.objects.filter(utility__id_string=id_string)


def get_material_type_by_id(id):
    try:
        return MaterialType.objects.get(id=id)
    except:
        return False


def get_material_type_by_id_string(id_string):
    try:
        return MaterialType.objects.get(id_string=id_string)
    except:
        return False
