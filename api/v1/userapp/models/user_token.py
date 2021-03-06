# table header
# module: All  | sub-module - All
# table type : Master
# table name : 2.5.1. Role Master
# table description : All users unique tokens will be saved in this table along with user_id
# frequency of data changes : Low
# sample tale data :"atg23466hdkksk89"
# reference tables : 2.5.4 Product/Services Table
# author : Saloni Monde
# created on : 24/04/2020
# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database
from django.utils import timezone # importing package for datetime


# Create User Token table start

class UserToken(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    token = models.CharField(max_length=200, null=True, blank=True)
    form_factor_id = models.BigIntegerField(null=True, blank=True)
    user_id = models.BigIntegerField(null=True, blank=True)
    ip_address = models.CharField(max_length=200,null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)

    def __str__(self):
        return self.token

    def __unicode__(self):
        return self.token

# Create User Token table end


def get_token_by_user_id(id):
    return UserToken.objects.filter(user_id=id, is_active=True).last()


def get_token_by_token(token):
    return UserToken.objects.get(token=token, is_active=True)


def check_token_exists(token):
    return UserToken.objects.filter(token=token, is_active=True).exists()


def check_token_exists_for_user(token, user_id):
    return UserToken.objects.filter(token=token, user_id=user_id, is_active=True).exists()