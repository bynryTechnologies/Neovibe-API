import datetime
import uuid
from django.db import models
# Table Type : Lookup
# Table Name : 2.12.22 Channel
# Description : It Payment Channel and ID of various Payment Channel to be used by Operator or Utility
# Frequency of data changes : Low
# Reference Table :
# Auther : Jayshree
# Creation Date : 21-04-2020



class Channel(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    channel_name = models.CharField(max_length=30, blank=False, null=False)
    created_by = models.IntegerField(null=False, blank=False)
    updated_by = models.IntegerField(null=False, blank=False)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.channel_name

    def __unicode__(self):
        return self.channel_name
