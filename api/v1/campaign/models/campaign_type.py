import uuid  # importing package for guid
from datetime import datetime  # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database
from v1.commonapp.views.custom_exception import CustomAPIException
from rest_framework import status
from django.utils import timezone # importing package for datetime

# Create Campaign Type table start


class CampaignType(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, blank=False, null=False)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name
    
    

def get_campaign_type_by_id(id):
    try:
        return CampaignType.objects.filter(id=id)
    except Exception as e:
        raise CustomAPIException("Campaign Type does not exists.", status_code=status.HTTP_404_NOT_FOUND)


def get_campaign_type_by_id_string(id_string):
    try:
        return CampaignType.objects.get(id_string=id_string)
    except:
        return False
# Create Campaign Type table end