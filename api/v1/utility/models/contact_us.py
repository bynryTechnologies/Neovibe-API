import uuid
from django.db import models
from django.utils import timezone
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from v1.commonapp.views.custom_exception import CustomAPIException
from rest_framework import status


class ContactUs(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    email = models.CharField(max_length=200, blank=True, null=True)
    emergency_no = models.CharField(max_length=200, blank=True, null=True)
    working_days = models.CharField(max_length=200, blank=True, null=True)
    portal_site = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.email)

    def __unicode__(self):
        return str(self.email)


def get_contact_us_by_id(id):
    try:
        contact_us = ContactUs.objects.get(id=id)
        return contact_us
    except Exception as e:
        raise CustomAPIException("Contact Us Details not exists.", status_code=status.HTTP_404_NOT_FOUND)


def get_contact_us_by_id_string(id_string):
    try:
        return ContactUs.objects.get(id_string=id_string)
    except:
        return False
