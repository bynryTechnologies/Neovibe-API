# table header
# module: Tenant | sub-module - Tenant Subscription
# table type : Master
# table name : 1.2  Tenant Subscription Plan
# table description :  It will contain details for Tenant subscription Plan
# frequency of data changes : Medium
# sample tale data : "Plan - A"
# reference tables : 1.1 Tenant Master
# author : Gauri Deshmukh
# created on : 24/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
import datetime  # importing package for datetime

from django.db import models  # importing package for database


# Create Tenant Subscription Plan table start.

class TenantSubscriptionPlan(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    subscription_id = models.IntegerField(null=True, blank=True)
    short_name = models.IntegerField(null=True, blank=True)
    subcription_type = models.CharField(max_length=200, blank=False, null=False)
    description = models.CharField(max_length=500, blank=False, null=False)
    max_Utility  = models.IntegerField(null=True, blank=True)
    max_user = models.IntegerField(null=True, blank=True)
    max_consumer = models.IntegerField(null=True, blank=True)
    max_storage = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.id_string

    def __unicode__(self):
        return self.id_string

# Create Tenant Subscription Plan table end.
