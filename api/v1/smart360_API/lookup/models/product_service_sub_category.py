# table header
# module: Asset, Sourcing | sub-module - All
# table type : lookup (Local)
# table name : 2.12.66 Product/Services Sub-Category
# table description : A lookup table for sub-categories of products and services.
# frequency of data changes : Low
# sample tale data :
# reference tables : 2.5.4 Product/Services Table
# author : Saloni Monde
# created on : 21/04/2020


# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
import datetime  # importing package for datetime

from django.db import models  # importing package for database


# Create Product Service Sub Category table start.

class ProductServiceSubCategory(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    name = models.CharField(max_length=200, blank=False, null=False)
    category = models.CharField(blank=False, null=False)
    is_active = models.BooleanField(default=False)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

# Create Product Service Sub Category table end.
