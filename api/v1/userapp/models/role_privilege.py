# table header
# module: All  | sub-module - All
# table type : Master
# table name : 2.5.2. Role Privileges
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
from v1.commonapp.models.module import get_module_by_id, get_module_by_id_string
from v1.commonapp.models.sub_module import get_sub_module_by_id, get_sub_module_by_id_string
from v1.tenant.models.tenant_master import TenantMaster, get_tenant_by_id
from v1.userapp.models.privilege import get_privilege_by_id, get_privilege_by_id_string
from v1.userapp.models.role import get_role_by_id, get_role_by_id_string
from v1.utility.models.utility_master import UtilityMaster, get_utility_by_id
from django.db import models  # importing package for database
from django.utils import timezone # importing package for datetime


# Create Role Privilege table start

class RolePrivilege(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    role_id = models.BigIntegerField(null=True, blank=True)
    module_id = models.BigIntegerField(null=True, blank=True)
    sub_module_id = models.BigIntegerField(null=True, blank=True)
    privilege_id = models.BigIntegerField(null=True, blank=True) # View, Edit
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True)

    # def __str__(self):
    #     return self.id

    def __unicode__(self):
        return self.role_id

    @property
    def get_tenant(self):
        return get_tenant_by_id(self.tenant_id)

    @property
    def get_utility(self):
        return get_utility_by_id(self.utility_id)

    @property
    def get_all_submodules(self):
        return  True

    @property
    def get_role(self):
        return get_role_by_id(self.role_id)

    @property
    def get_module(self):
        return get_module_by_id(self.module_id)

    @property
    def get_sub_module(self):
        return get_sub_module_by_id(self.sub_module_id)

    @property
    def get_privilege(self):
        return get_privilege_by_id(self.privilege_id)

    # Create Role Privilege table end


def get_role_privilege_by_role_id(role_id):
    return RolePrivilege.objects.filter(role_id=role_id, is_active=True)


def get_role_privilege_by_id_string(id_string):
    return RolePrivilege.objects.filter(id=id_string, is_active=True).last()


def get_role_privilege_by_module_id(module_id, role_id):
    return RolePrivilege.objects.filter(module_id=module_id, role_id=role_id, is_active=True)


def get_role_privilege_by_sub_module_id(sub_module_id, role_id):
    return RolePrivilege.objects.filter(sub_module_id=sub_module_id, role_id=role_id, is_active=True)


def get_privilege_by_role_id(role_id):
    privilege_list = []
    privileges = RolePrivilege.objects.filter(role_id=role_id, is_active=True)
    for privilege in privileges:
        data = get_privilege_by_id(privilege.privilege_id)
        privilege_list.append({"id_string":data.id_string, "name":data.name})
    return privilege_list


def get_privilege_by_sub_module_id(sub_module_id,module_id):
    privilege = RolePrivilege.objects.filter(module_id=module_id, sub_module_id=sub_module_id, is_active=True).last()
    return get_privilege_by_id(privilege.privilege_id)


def get_record_by_values(role_id, module_id_string, sub_module_id_string, privilege_id_string):
    print(role_id, module_id_string, sub_module_id_string, privilege_id_string)
    module = get_module_by_id_string(module_id_string)
    sub_module = get_sub_module_by_id_string(sub_module_id_string)
    privilege = get_privilege_by_id_string(privilege_id_string)
    return RolePrivilege.objects.filter(role_id=role_id,module_id=module.id, sub_module_id=sub_module.id, privilege_id=privilege.id, is_active=True).last()


def get_record_values_by_id(role_id,module_id,sub_module_id,privilege_id):
    return RolePrivilege.objects.filter(role_id=role_id, module_id=module_id, sub_module_id=sub_module_id, privilege_id=privilege_id, is_active=True).last()


def check_role_privilege_exists(roles, module_id, sub_module_id, privilege_id):
    for role in roles:
        print('++++++++++++',role.role_id, module_id, sub_module_id, privilege_id)
        if RolePrivilege.objects.filter(role_id=role.role_id, module_id=module_id, sub_module_id=sub_module_id, privilege_id=privilege_id, is_active=True).exists():
            return True
    return False


def get_module_by_role_id(role_id):
    module_list = []
    check_module_list = []
    modules = RolePrivilege.objects.filter(role_id=role_id, is_active=True)
    for module in modules:
        sub_module_list = []

        if not module.module_id in check_module_list:
            check_sub_module_list = []

            check_module_list.append(module.module_id)
            module_data = get_module_by_id(module.module_id)

            sub_modules = get_role_privilege_by_module_id(module_data.id, role_id)

            for sub_module in sub_modules:
                privilege_list = []

                if not sub_module.sub_module_id in check_sub_module_list:
                    check_privilege_list = []

                    check_sub_module_list.append(sub_module.sub_module_id)
                    privileges = get_role_privilege_by_sub_module_id(sub_module.sub_module_id,role_id)

                    for privilege in privileges:
                        if not privilege.privilege_id in check_privilege_list:
                            check_privilege_list.append(privilege.privilege_id)
                            privilege_data = get_privilege_by_id(privilege.privilege_id)
                            privilege_list.append({
                                "id_string": privilege_data.id_string,
                                "name": privilege_data.name
                            })

                    sub_module_data = get_sub_module_by_id(sub_module.sub_module_id)
                    sub_module_list.append({
                        "id_string": sub_module_data.id_string,
                        "name": sub_module_data.name,
                        "privilege" : privilege_list
                    })
            module_list.append({
                    "id_string" : module_data.id_string,
                    "name" : module_data.name,
                    "sub_module" : sub_module_list,
                    "short_desc" : module_data.short_desc,
                    "long_desc" : module_data.long_desc
                })
    return {'module' : module_list}