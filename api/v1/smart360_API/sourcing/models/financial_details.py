# table header
# module: Sourcing
# table type : Master
# table name : 2.5.2 Financial Details
# table description : Table saves the financial  details of any Supplier that exists in the system.
# frequency of data changes : High
# sample table data :
# reference tables : None
# author : Jayshree Kumbhare
# created on : 24/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
import datetime  # importing package for datetime

from django.db import models  # importing package for database


# Create Financial Details table start

class FinancialDetails(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    supplier_id = models.IntegerField(null=True, blank=True)
    account_Name = models.CharField(max_length=200, blank=True, null=True)
    account_No = models.CharField(max_length=200, blank=True, null=True)
    bank_Name = models.IntegerField(null=True, blank=True)
    branch_Name = models.CharField(max_length=200, blank=True, null=True)
    ifsc_code = models.CharField(max_length=200, blank=True, null=True)
    gst_no = models.CharField(max_length=200, blank=True, null=True)
    pan_no = models.CharField(max_length=200, blank=True, null=True)
    vat_no = models.CharField(max_length=200, blank=True, null=True)
    status_id = models.IntegerField(null=True, blank=True)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __unicode__(self):
        return self.id

# Create Financial Details table end.




