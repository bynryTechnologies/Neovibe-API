# table header
# module: Sourcing
# table type : Master
# table name : 2.5.9 Supplier Invoice
# table description : The Invoice table saves the Invoice details of Supplier or Contract
# frequency of data changes : High
# sample table data :
# reference tables : None
# author : Jayshree Kumbhare
# created on : 24/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime

from v1.contract.models.contract import get_contract_by_id
from v1.supplier.models.supplier import get_supplier_by_id
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database
from decimal import Decimal  # importing package for float number
from django.utils import timezone # importing package for datetime


# Create Invoice Table start

class SupplierInvoice(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    contract = models.BigIntegerField(null=True, blank=True)
    supplier = models.BigIntegerField(null=True, blank=True)
    supplier_financial = models.BigIntegerField(null=True, blank=True)
    demand = models.BigIntegerField(null=True, blank=True)
    invoice_no = models.BigIntegerField(null=True, blank=True)
    invoice_amount = models.FloatField(max_length=80, blank=False, null=False, default=Decimal(0.00))
    invoice_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    due_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    status_id = models.BigIntegerField(null=True, blank=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.invoice_no)

    def __unicode__(self):
        return str(self.invoice_no)

    @property
    def get_supplier(self):
        supplier = get_supplier_by_id(self.supplier)
        return supplier

    @property
    def get_contract(self):
        contract = get_contract_by_id(self.contract)
        return contract

# Create Invoice table end.


def get_supplier_invoice_by_id(id):
    try:
        return SupplierInvoice.objects.get(id=id)
    except:
        return False


def get_supplier_invoice_by_id_string(id_string):
    try:
        return SupplierInvoice.objects.get(id_string=id_string)
    except:
        return False


def get_contract_invoice_by_id(id):
    try:
        return SupplierInvoice.objects.get(id=id)
    except:
        return False


def get_contract_invoice_by_id_string(id_string):
    try:
        return SupplierInvoice.objects.get(id_string=id_string)
    except:
        return False

