# table header
# module: All  | sub-module - All
# table type :
# table name :
# table description : A master table that stores user wise privileges.
# frequency of data changes : Low
# sample tale data :
# reference tables :
# author : Saloni Monde
# created on : 25/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime

from master.models import get_user_by_id, get_user_by_id_string
from v1.tenant.models.tenant_master import TenantMaster, get_tenant_by_id
from v1.userapp.models.role import get_role_by_id, get_role_by_id_string
from v1.userapp.models.role_privilege import get_role_privilege_by_role_id
from v1.utility.models.utility_master import UtilityMaster, get_utility_by_id
from django.db import models  # importing package for database
from django.utils import timezone # importing package for datetime


# Create User Privilege table start

class UserRole(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    user_id = models.BigIntegerField(null=True, blank=True)
    role_id = models.BigIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)

    # def __str__(self):
    #     return self.user_id

    def __unicode__(self):
        return self.user_id

    @property
    def get_tenant(self):
        return get_tenant_by_id(self.tenant.id)

    @property
    def get_utility(self):
        return get_utility_by_id(self.utility.id)

    @property
    def get_user(self):
        return get_user_by_id(self.user_id)

    @property
    def get_role(self):
        return get_role_by_id(self.role_id)

    @property
    def get_role_privilege(self):
        return get_role_privilege_by_role_id(self.role_id)

    # class Meta:
    #     unique_together = ('role_id', 'user_id',)

# Create User Privilege table end


def get_privilege_by_id_string(id_string):
    return UserRole.objects.get(id_string=id_string, is_active=True)


def get_user_role_by_user_id(id):
    return UserRole.objects.filter(user_id=id, is_active=True)

def get_user_role_by_user_id_string(id_string):
    try:
        return UserRole.objects.filter(id_string=id_string, is_active=True)
    except:
        return False

def get_user_role_by_role_id(id):
    return UserRole.objects.filter(role_id=id, is_active=True)


def get_record_by_values(user_id_string,role_id_string):
    user = get_user_by_id_string(user_id_string)
    role = get_role_by_id_string(role_id_string)
    return UserRole.objects.filter(user_id=user.id, role_id=role.id).last()


def get_record_values_by_id(user_id,role_id_string):
    try:
        role = get_role_by_id_string(role_id_string)
        return UserRole.objects.get(user_id=user_id,role_id=role.id)
    except:
        return False


def check_role_exists(id):
    return UserRole.objects.filter(user_id=id, is_active=True)


def get_role_count_by_user(user_id):
    role = UserRole.objects.filter(user_id=user_id).count()
    if role == 1:
        role_obj = UserRole.objects.get(user_id=user_id)
        get_role = get_role_by_id(role_obj.role_id)
        return get_role.role
    elif role > 1:
        return 'multiple'
    else:
        return 'No Role Attached'



