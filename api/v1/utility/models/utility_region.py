import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database
from v1.commonapp.models.region import get_region_by_id



class UtilityRegion(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=True, on_delete=models.SET_NULL) 
    utility = models.ForeignKey(UtilityMaster, blank=False, null=True, on_delete=models.SET_NULL) 
    region_id = models.BigIntegerField(null=True, blank=True)
    label = models.CharField(max_length=200, blank=False, null=False) 
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.label

    def __unicode__(self):
        return self.label
    
    @property
    def get_region(self):
        region = get_region_by_id(self.region_id)
        return region


