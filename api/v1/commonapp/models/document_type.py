# Table Header
# module : All modules & sub-modules
# Table Type : Lookup (Global)
# Table Name : 2.12.12 Document Type
# Description : It is a global lookup table that will store types of documents
# Frequency of data changes : Low
# Sample Table Data : "ID Proof", "Address Proof"
# Reference Table : 2.3.3 Survey Transaction Table, 2.3.8 Campaign Transaction Table, 2.3.1. Consumer Master,
#                    2.3.2. Consumer - Registration, 2.7.1. Employee, 2.5.5 User Documents.
# Author : Jayshree Kumbhare
# Creation Date : 21-04-2020

# change history
# <ddmmyyyy><changes><author>

import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from django.db import models  # importing package for database

# Create Document Type table start

class DocumentType(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, blank=False, null=False)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

# Create Document Type table end
