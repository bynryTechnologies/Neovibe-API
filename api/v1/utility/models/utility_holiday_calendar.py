import uuid  # importing package for guid
from datetime import datetime  # importing package for datetime
from django.db import models  # importing package for database
from django.contrib.postgres.fields import JSONField

# Create work_order Master table start
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from v1.utility.models.utility_leave_type import get_utility_leave_by_id
from django.utils import timezone # importing package for datetime

# table header
# module: Work Order | sub-module -
# table type: Master
# table name:Utility Holiday Calendar
# table description: It contains the list of Holidays of Utility
# #frequency of data changes: Low
# sample table data:
# reference tables:
# Author : Chinmay Pathak
# Creation Date : 29/12/2020


class UtilityHolidayCalendar(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, blank=True, null=True)
    date = models.DateField(null=False, blank=False, default=timezone.now)
    start_time = models.TimeField(null=True, auto_now=False, auto_now_add=False)
    end_time = models.TimeField(null=True, auto_now=False, auto_now_add=False)
    holiday_type_id = models.BigIntegerField(null=False, blank=False)
    description = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    @property
    def get_holiday_type(self):
        holiday_type = get_utility_leave_by_id(self.holiday_type_id)
        return holiday_type


# Create work_order_master table end

def get_utility_holiday_calendar_by_tenant_id_string(id_string):
    return UtilityHolidayCalendar.objects.filter(tenant__id_string=id_string)


def get_utility_holiday_calendar_by_utility_id_string(id_string):
    return UtilityHolidayCalendar.objects.filter(utility__id_string=id_string)


def get_utility_holiday_calendar_by_id(id):
    try:
        return UtilityHolidayCalendar.objects.get(id=id)
    except:
        return False


def get_utility_holiday_calendar_by_id_string(id_string):
    try:
        return UtilityHolidayCalendar.objects.get(id_string=id_string)
    except:
        return False
