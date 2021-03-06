__author__ = "aki"

from django.contrib import admin
from v1.tender.models.tender import Tender
from v1.tender.models.tender_quotation import TenderQuotation
from v1.tender.models.tender_status import TenderStatus
from v1.tender.models.tender_terms_and_conditions import TenderTermsAndCondition
from v1.tender.models.tender_type import TenderType
from v1.tender.models.tender_vendor import TenderVendor


admin.site.register(Tender)
admin.site.register(TenderQuotation)
admin.site.register(TenderStatus)
admin.site.register(TenderVendor)
admin.site.register(TenderType)
admin.site.register(TenderTermsAndCondition)
