# table header
# module: All  | sub-module - All
# table type : Master
# table name :  User Privileges
# table description : A master table that stores role wise privileges.
# frequency of data changes : Low
# sample tale data : "view only", "validation 1", "validation 2"
# reference tables : 2.5.4 Product/Services Table
# author : Saloni Monde
# created on : 24/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime

# from v1.commonapp.models.sub_module import get_submodule_by_module_id
from master.models import get_user_by_id
from v1.commonapp.models.module import get_module_by_id, get_module_by_id_string
from v1.commonapp.models.sub_module import get_sub_module_by_id, get_sub_module_by_id_string
from v1.tenant.models.tenant_master import TenantMaster, get_tenant_by_id
from v1.userapp.models.privilege import get_privilege_by_id, get_privilege_by_id_string
from v1.utility.models.utility_master import UtilityMaster, get_utility_by_id
from django.db import models  # importing package for database
from django.utils import timezone # importing package for datetime


# Create Role Privilege table start

class UserPrivilege(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    user_id = models.BigIntegerField(null=True, blank=True)
    role_id = models.BigIntegerField(null=True, blank=True)
    module_id = models.BigIntegerField(null=True, blank=True)
    sub_module_id = models.BigIntegerField(null=True, blank=True)
    privilege_id = models.BigIntegerField(null=True, blank=True) # View, Edit
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)

    def __str__(self):
        return self.tenant.name

    def __unicode__(self):
        return self.tenant.name

    @property
    def get_tenant(self):
        return get_tenant_by_id(self.tenant_id)

    @property
    def get_utility(self):
        return get_utility_by_id(self.utility_id)

    @property
    def get_all_submodules(self):
        return True

    @property
    def get_user(self):
        return get_user_by_id(self.user_id)

    @property
    def get_module(self):
        return get_module_by_id(self.module_id)

    @property
    def get_sub_module(self):
        return get_sub_module_by_id(self.sub_module_id)

    @property
    def get_privilege(self):
        return get_privilege_by_id(self.privilege_id)

    # class Meta:
    #     unique_together = ('role_id', 'module_id', 'sub_module_id', 'privilege_id',)

    # Create Role Privilege table end


def get_user_privilege_by_user_id(user_id):
    return UserPrivilege.objects.filter(user_id=user_id, is_active=True)


def get_record_values_by_id(user_id,module_id,sub_module_id,privilege_id):
    return UserPrivilege.objects.filter(user_id=user_id, module_id=module_id, sub_module_id=sub_module_id, privilege_id=privilege_id, is_active=True).last()


def check_user_privilege_exists(user_id,module_id,sub_module_id,privilege_id):
    return UserPrivilege.objects.filter(user_id=user_id, module_id=module_id, sub_module_id=sub_module_id, privilege_id=privilege_id, is_active=True).exists()
