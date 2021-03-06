# Table Header
# module: Consumer Care & Ops | sub-module - Consumer, Registration, Metering, Billing, Payments, Services, Complaints
# Table Type : Lookup (Global)
# Table Name : 2.12.19 Payment Mode
# Description : It is a global lookup table that stores various modes of payments
# Frequency of data changes : Low
# sample Table Data : "Cash", "Digital", "Cheque/dd"
# Reference Table : 2.3.1. Consumer Master, 2.7.2. Employee_bank_details, 2.7.8. Bank details.
# Author : Jayshree Kumbhare
# Creation Date : 21-04-2020

# change history
# <ddmmyyyy><changes><author>

import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database
from django.utils import timezone # importing package for datetime

# Create Payment Mode table start
class PaymentMode(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=200, blank=False, null=False)
    key = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)

    def __str__(self):
        return self.name + " " + str(self.id_string)

    def __unicode__(self):
        return self.name
# Create Payment Mode table end


def get_payment_mode_by_id_string(id_string):
    try:
        return PaymentMode.objects.get(id_string = id_string)
    except:
        return False

def get_payment_mode_by_id(id):
    try:
        return PaymentMode.objects.get(id = id)
    except:
        return False