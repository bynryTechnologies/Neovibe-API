# table header
# module: Sourcing
# table type : Master
# table name : SupplierProduct
# table description : The Product table saves the basic Product/Services details of any Supplier
# frequency of data changes : High
# sample table data :
# reference tables : None
# author : Jayshree Kumbhare
# created on : 24/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime

from v1.supplier.models.product_category import get_supplier_product_category_by_id
from v1.supplier.models.product_subcategory import get_supplier_product_subcategory_by_id
from v1.supplier.models.supplier import get_supplier_by_id
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database
from django.utils import timezone # importing package for datetime


# Create Product Service Table start

class SupplierProduct(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    supplier = models.BigIntegerField(null=True, blank=True)
    type = models.BigIntegerField(null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    image = models.URLField(null=True, blank=True)
    product_category = models.BigIntegerField(null=True, blank=True)
    product_subcategory = models.BigIntegerField(null=True, blank=True)
    rate = models.DecimalField(max_digits=12, decimal_places=2, default=0, null=True, blank=True)
    quantity = models.BigIntegerField(null=True, blank=True)
    unit = models.BigIntegerField(null=True, blank=True)
    status = models.BigIntegerField(null=True, blank=True)
    source_type = models.BigIntegerField(null=True, blank=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    @property
    def get_supplier(self):
        supplier = get_supplier_by_id(self.supplier)
        return supplier

    @property
    def get_product_category(self):
        product_category = get_supplier_product_category_by_id(self.product_category)
        return product_category

    @property
    def get_product_subcategory(self):
        product_subcategory = get_supplier_product_subcategory_by_id(self.product_subcategory)
        return product_subcategory

# Create Product Service table end.


def get_supplier_product_by_id_string(id_string):
    try:
        return SupplierProduct.objects.get(id_string = id_string)
    except:
        return False


def get_supplier_product_by_id(id):
    try:
        return SupplierProduct.objects.get(id = id)
    except:
        return False
