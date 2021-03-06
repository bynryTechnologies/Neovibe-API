import uuid  # importing package for GUID
from datetime import datetime # importing package for datetime
from django.db import models  # importing package for database
from v1.commonapp.models.module import get_module_by_id
from django.utils import timezone # importing package for datetime

# Table Header
# Module : All
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

# Create Sub Module table start


class SubModule(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    module_id = models.BigIntegerField(null=True, blank=True)
    key = models.CharField(max_length=200, blank=True, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.key

    def __unicode__(self):
        return self.key

    @property
    def get_module(self):
        return get_module_by_id(self.module_id)


# Create Sub Module table end


def get_sub_module_by_id(id):
    try:
        return SubModule.objects.get(id=id)
    except:
        return False


def get_sub_module_by_key(key):
    try:
        return SubModule.objects.get(key=key, is_active=True).id
    except:
        return False


def get_sub_module_by_id_string(id_string):
    try:
        return SubModule.objects.get(id_string=id_string, is_active=True)
    except:
        return False


def get_all_sub_modules():
    return SubModule.objects.filter(is_active=True)


def get_submodule_by_module_id(id):
    return SubModule.objects.filter(module_id=id, is_active=True)


def get_sub_module_by_name(name):
    sub_module = SubModule.objects.get(name=name, is_active=True)
    return sub_module.id


def get_sub_module_id_by_key(key):
    try:
        return SubModule.objects.get(key=key, is_active=True).id
    except:
        False
