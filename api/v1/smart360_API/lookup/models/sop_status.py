# Table Header : SOP Status
# Table Type : Lookup (Local)
# Table Name : 2.12.79 SOP Status
# Description : It  SOP Status and ID of various SOP Status to be used by Operator or Utility
# Frequency of data changes : Low
# Sample Table Data :
# Reference Table : 2.6.7 Closure Report Transaction
# Auther : Jayshree
# Creation Date : 22/04/2020


import datetime
import uuid
from django.db import models
# Start the Code

class SopStatus(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    sop_status = models.CharField(max_length=30, blank=False, null=False)
    created_by = models.IntegerField(null=False, blank=False)
    updated_by = models.IntegerField(null=False, blank=False)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.sop_status

    def __unicode__(self):
        return self.sop_status
# End the Code