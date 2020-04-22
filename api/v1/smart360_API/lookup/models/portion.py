import datetime #importing package for datetime
import uuid #importing package for GUID

from django.db import models #importing package for database

#table header : Portion
#table type: lookup
#table name: 2.12.44 Portion  (Local)
#table description: It is lookup tables to be used in various tables. It portion and ID of various portion to be used by Operator or Utility
#frequency of data changes: low
#sample table data:
#reference tables:2.3.1. Consumer Master
#auther: Gauri
#creation date: 21/4/2020

#change history
#<22/4/2020>-<ForeignKey removed from Created by , updated by fields>-<Gauri>


class Portion(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True) #TODO: remove _id: Done
    tenant = models.ForeignKey(TenantMaster,null=False, blank=False)  #Table name : Done
    utility = models.ForeignKey(UtilityMaster,null=False, blank=False)  # Table name:Done
    portion_name = models.CharField(null=False, blank=False)#TODO: Name: Done
    city_id = models.CharField(null=False, blank=False) #TODO: remove foreignkey :Done
    created_by = models.CharField(null=False, blank=False) #TODO: remove foreignkey : Done
    updated_by = models.CharField(null=False, blank=False) #TODO: remove foreignkey : Done
    created_date = models.DateTime(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTime(null=True, blank=True, default=datetime.now())
    is_active = models.Boolean(default=False)


    def __str__(self):
        return self.portion_name

    def __unicode__(self):
        return self.portion_name