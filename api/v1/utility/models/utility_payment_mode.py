import uuid  # importing package for guid
from datetime import datetime  # importing package for datetime

from v1.payment.models.payment_mode import get_payment_mode_by_id
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database
from v1.commonapp.views.custom_exception import CustomAPIException
from rest_framework import status
from v1.payment.models.payment_type import get_payment_type_by_id
from v1.utility.models.utility_product import get_utility_product_by_id
from django.utils import timezone # importing package for datetime


# Create Utility Payment Mode table start


class UtilityPaymentMode(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    payment_mode_id = models.BigIntegerField(null=True, blank=True)
    utility_product_id = models.BigIntegerField(null=True, blank=True)
    name = models.CharField(max_length=200, blank=False, null=False)
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
    def get_payment_mode_key(self):
        mode = get_payment_mode_by_id(self.payment_mode_id)
        return mode.key

    @property
    def get_utility_product(self):
        utility_product = get_utility_product_by_id(self.utility_product_id)
        return utility_product
    
   


def get_utility_payment_mode_by_id(id):
    try:
        return UtilityPaymentMode.objects.filter(id=id)
    except Exception as e:
        raise CustomAPIException("Utility Payment Mode does not exists.", status_code=status.HTTP_404_NOT_FOUND)


def get_utility_payment_mode_by_id_string(id_string):
    try:
        return UtilityPaymentMode.objects.get(id_string=id_string)
    except:
        return False
# Create Utility Payment Mode table end.