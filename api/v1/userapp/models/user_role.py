
# module: All  | sub-module - All
# table type :
# table name :
# table description : Skills of a particular user will be stored in this table
# frequency of data changes :
# sample tale data :
# reference tables :
# author : Saloni Monde
# created on : 25/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime

from v1.commonapp.models.department import get_department_by_id
from v1.commonapp.models.form_factor import get_form_factor_by_id
from v1.tenant.models.tenant_master import TenantMaster
from v1.userapp.models.role_status import get_role_status_by_id
from v1.userapp.models.role_sub_type import get_role_sub_type_by_id
from v1.userapp.models.role_type import get_role_type_by_id
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database


# Create User Role table start

class UserRole(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    type_id = models.BigIntegerField(blank=True, null=True)
    sub_type_id = models.BigIntegerField(blank=True, null=True)
    form_factor_id = models.BigIntegerField(blank=True, null=True)
    department_id = models.BigIntegerField(blank=True, null=True)
    role_ID = models.CharField(max_length=200,blank=True, null=True)
    role = models.CharField(max_length=200,blank=False, null=False)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.id

    def __unicode__(self):
        return self.id

    @property
    def get_role_type(self):
        role_type = get_role_type_by_id(self.type_id)
        return role_type.name

    @property
    def get_role_sub_type(self):
        sub_type = get_role_sub_type_by_id(self.sub_type_id)
        return sub_type.name

    @property
    def get_user_status(self):
        status = get_role_status_by_id(self.status_id)
        return status.status

    @property
    def get_form_factor(self):
        form_factor = get_form_factor_by_id(self.form_factor_id)
        return form_factor.name

    @property
    def get_department(self):
        department = get_department_by_id(self.department_id)
        return department.name


# Create User Role table end


def get_role_by_id(id):
    return UserRole.objects.filter(id=id, is_active=True).last()


def get_role_by_id_string(id_string):
    return UserRole.objects.filter(id_string=id_string, is_active=True).last()


def get_role_by_tenant_id_string(id_string):
    return UserRole.objects.filter(tenant__id_string=id_string, is_active=True)