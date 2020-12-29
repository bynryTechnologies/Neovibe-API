import uuid
from datetime import datetime
from django.db import models

from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster

# table header
# module: User | sub-module -
# table type: Master
# table name: Field Agent Live Location
# table description: It contains the list of Field Agent Live Location
# #frequency of data changes: high
# sample table data:
# reference tables:
# Author : Priyanka Kachare
# Creation Date : 16/12/2020


class FieldAgentLiveLocation(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    user_id = models.BigIntegerField(null=True, blank=True)
    latitude = models.CharField(max_length=200, blank=True, null=True)
    longitude = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.user_id

    def __unicode__(self):
        return self.user_id

    def get_tenant(self):
        return self.tenant


def get_field_agent_live_location_by_user_id(user_id):
    try:
        return FieldAgentLiveLocation.objects.get(user_id=user_id, is_active=True)
    except:
        return False

