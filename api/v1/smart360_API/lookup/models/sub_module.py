# Table Header
# Module : Consumer Care & Ops
# Table Type : Lookup (Local)
# Table Name : 2.12.3 Sub module
# Description : This table will save all the sub modules.Create Consumer Registration table start.
# Frequency of data changes : Low
# Sample Table Data :
# Reference Table : 2.6.1 Service Request
# Author :
# Creation Date :

# change history
# <ddmmyyyy>-<changes>-<Author>

import datetime  # importing package for datetime
import uuid  # importing package for GUID

from django.db import models  # importing package for database
from api.v1.smart360_API.lookup.models.activity import Activity


# Create Sub Module table start


class SubModule(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    sub_module = models.CharField(null=False, blank=False)
    activity = models.ForeignKey(Activity, null=False, blank=False)
    name = models.CharField(max_length=200, null=False, blank=False)
    created_by = models.IntegerField(null=False, blank=False)
    updated_by = models.IntegerField(null=False, blank=False)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.sub_module

    def __unicode__(self):
        return self.sub_module


# Create Sub Module table end

def get_sub_module_by_id(id):
    return SubModule.objects.get(id=id)
