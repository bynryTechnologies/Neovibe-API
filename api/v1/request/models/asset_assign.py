# table header
# module: Purchase
# table type : Master
# table name : 2.7.2 Asset Assign Table
# table description : This table will store all the assign assets.
# frequency of data changes : High
# sample table data :
# reference tables : None
# author : Jayshree Kumbhare
# created on : 25/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database
from django.utils import timezone # importing package for datetime


# Create Asset Assign table start

class AssetAssign(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    request_master = models.BigIntegerField(null=True, blank=True)
    asset = models.BigIntegerField(null=True, blank=True)
    quantity = models.CharField(max_length=200, blank=True, null=True)
    assign_quantity = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    get_pass_number = models.CharField(max_length=200, blank=True, null=True)
    country = models.BigIntegerField(null=True, blank=True)
    state = models.BigIntegerField(null=True, blank=True)
    city = models.BigIntegerField(null=True, blank=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True,default=timezone.now)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.id

    def __unicode__(self):
        return self.id

# Create Asset Assign table end.
