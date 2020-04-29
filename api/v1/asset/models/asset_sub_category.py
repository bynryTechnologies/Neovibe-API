# table header
# module: O&M, Assets, Purchase, Store, Tender, Contract | sub-module - All
# table type : lookup (Local)
# table name : 2.12.86 Asset Sub-Category
# table description : A lookup table for sub-categories of assets.
# frequency of data changes : Low
# sample tale data :
# reference tables : 2.6.2.2 Asset Master
# author : Saloni Monde
# created on : 22/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database

# Create Asset Sub Category table start.

class AssetSubCategory(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    sub_category = models.CharField(max_length=200, blank=False, null=False)
    name = models.CharField(max_length=200, blank=False, null=False)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __unicode__(self):
        return self.sub_category

# Create Asset Sub Category table end.
