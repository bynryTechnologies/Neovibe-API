# table header
# module: Purchase
# table type : Master
# table name : 2.7.1 Request Master
# table description : This table will store all pending,approved,partial and rejected requests.
# frequency of data changes : High
# sample table data :
# reference tables : None
# author : Jayshree Kumbhare
# created on : 25/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
import datetime  # importing package for datetime

from django.db import models  # importing package for database
from api.v1.smart360_API.tenant.models.tenant_master import TenantMaster
from api.v1.smart360_API.utility.models.utility_master import UtilityMaster

# Create Request Master table start

class RequestMaster(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    type = models.IntegerField(null=True, blank=True)
    short_name = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    requester_id = models.IntegerField(null=True, blank=True)
    approver_id = models.IntegerField(null=True, blank=True)
    asset_id = models.IntegerField(null=True, blank=True)
    request_date = models.DateField(null=True, blank=True, default=datetime.now())
    request_due_date = models.DateField(null=True, blank=True, default=datetime.now())
    request_status_id = models.IntegerField(null=True, blank=True)
    country_id = models.IntegerField(null=True, blank=True)
    state_id = models.IntegerField(null=True, blank=True)
    city_id = models.IntegerField(null=True, blank=True)
    department_id = models.IntegerField(null=True, blank=True)
    project_id = models.IntegerField(null=True, blank=True)
    category_id = models.IntegerField(null=True, blank=True)
    sub_category_id = models.IntegerField(null=True, blank=True)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __unicode__(self):
        return self.id

# Create Request Master table end.
