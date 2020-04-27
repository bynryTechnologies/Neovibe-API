# table header
# module: Sourcing
# table type : Master
# table name : 2.5.11 Terms & Conditions
# table description : The Terms table saves the terms and condition details of Supplier or Contract
# frequency of data changes : High
# sample table data : "Condition 1", "Condition 2"
# reference tables : None
# author : Jayshree Kumbhare
# created on : 24/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database


# Create Terms And Condition Table start

class TermsAndCondition(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    contract = models.IntegerField(null=True, blank=True)
    terms_name = models.CharField(max_length=200, blank=True, null=True)
    terms = models.CharField(max_length=500, blank=True, null=True)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.terms_name

    def __unicode__(self):
        return self.terms_name

# Create Terms and Conditions table end.
