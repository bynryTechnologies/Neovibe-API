from django.urls import path
from v1.consumer.views.consumer import *
from v1.consumer.views.consumer_audit_log import ConsumerAuditLogList
from v1.consumer.views.consumer_credit_rating import ConsumerCreditRatingList
from v1.consumer.views.consumer_meter import ConsumerMeterList
from v1.consumer.views.consumer_category import ConsumerCategoryList,ConsumerCategory,ConsumerCategoryDetail
from v1.consumer.views.consumer_offer_master import ConsumerOfferMasterList
from v1.consumer.views.consumer_service_contract_details import ConsumerServiceContractDetailList
from v1.consumer.views.consumer_subcategory import ConsumerSubCategoryDetail,ConsumerSubCategoryList,ConsumerSubCategory
from v1.consumer.views.consumer_ownership import ConsumerOwnership,ConsumerOwnershipDetail,ConsumerOwnershipList
from v1.consumer.views.consumer_consent import ConsumerConsentList,ConsumerConsentDetail,ConsumerConsent
from v1.consumer.views.consumer_support import ConsumerSupportList,ConsumerSupportDetail,ConsumerSupport
from v1.consumer.views.consumer_faq import ConsumerFaq,ConsumerFaqDetail,ConsumerFaqList
from v1.consumer.views.service_type import ServiceType,ServiceTypeList,ServiceTypeDetail
from v1.consumer.views.service_sub_type import ServiceSubType,ServiceSubTypeDetail,ServiceSubTypeList
from v1.consumer.views.consumer import ConsumerDetail,Consumer,ConsumerBillList,ConsumerBillDetail,ConsumerPayment,ConsumerPaymentDetail,ConsumerPaymentList,ConsumerComplaintList,ConsumerComplaintDetail,ConsumerScheme,ConsumerSchemeDetail,ConsumerComplaint

urlpatterns = [
    path('utility/<uuid:id_string>/list', ConsumerList.as_view()),
    path('<uuid:id_string>', ConsumerDetail.as_view()),
    path('', Consumer.as_view()),
    path('<uuid:id_string>/audit-log/list', ConsumerAuditLogList.as_view()),
    path('<uuid:id_string>/bill/list', ConsumerBillList.as_view()),
    path('<uuid:id_string>/credit-rating/list', ConsumerCreditRatingList.as_view()),
    path('bill/<uuid:id_string>', ConsumerBillDetail.as_view()),
    path('<uuid:id_string>/payment', ConsumerPayment.as_view()),
    path('payment/<uuid:id_string>', ConsumerPaymentDetail.as_view()),
    path('<uuid:id_string>/payment/list', ConsumerPaymentList.as_view()),
    path('<uuid:id_string>/complaint/list', ConsumerComplaintList.as_view()),
    path('<uuid:id_string>/complaint', ConsumerComplaint.as_view()),
    path('complaint/<uuid:id_string>', ConsumerComplaintDetail.as_view()),
    path('<uuid:id_string>/scheme', ConsumerScheme.as_view()),
    path('scheme/<uuid:id_string>', ConsumerSchemeDetail.as_view()),
    path('<uuid:id_string>/category/list', ConsumerCategoryList.as_view()),
    path('<uuid:id_string>/sub-category/list', ConsumerSubCategoryList.as_view()),
    path('<uuid:id_string>/ownership/list', ConsumerOwnershipList.as_view()),
    path('<uuid:id_string>/offer/list', ConsumerOfferMasterList.as_view()),
    path('<uuid:id_string>/meter/list', ConsumerMeterList.as_view()),
    path('<uuid:id_string>/payment',ConsumerPayment.as_view()),
    path('payment/<uuid:id_string>',ConsumerPaymentDetail.as_view()),
    path('<uuid:id_string>/payment/list',ConsumerPaymentList.as_view()),
    path('<uuid:id_string>/complaint/list',ConsumerComplaintList.as_view()),
    path('<uuid:id_string>/complaint',ConsumerComplaint.as_view()),
    path('complaint/<uuid:id_string>',ConsumerComplaintDetail.as_view()),
    path('<uuid:id_string>/scheme',ConsumerScheme.as_view()),
    path('scheme/<uuid:id_string>',ConsumerSchemeDetail.as_view()),
    path('utility/<uuid:id_string>/category/list',ConsumerCategoryList.as_view()),
    path('category/<uuid:id_string>',ConsumerCategoryDetail.as_view()),
    path('category',ConsumerCategory.as_view()),
    path('utility/<uuid:id_string>/subcategory/list',ConsumerSubCategoryList.as_view()),
    path('subcategory/<uuid:id_string>',ConsumerSubCategoryDetail.as_view()),
    path('subcategory',ConsumerSubCategory.as_view()),
    path('utility/<uuid:id_string>/ownership/list',ConsumerOwnershipList.as_view()),
    path('ownership/<uuid:id_string>',ConsumerOwnershipDetail.as_view()),
    path('ownership',ConsumerOwnership.as_view()),
    path('utility/<uuid:id_string>/consent/list',ConsumerConsentList.as_view()),
    path('consent/<uuid:id_string>',ConsumerConsentDetail.as_view()),
    path('consent',ConsumerConsent.as_view()),
    path('utility/<uuid:id_string>/support/list',ConsumerSupportList.as_view()),
    path('support/<uuid:id_string>',ConsumerSupportDetail.as_view()),
    path('support',ConsumerSupport.as_view()),
    path('utility/<uuid:id_string>/faq/list',ConsumerFaqList.as_view()),
    path('faq/<uuid:id_string>',ConsumerFaqDetail.as_view()),
    path('faq',ConsumerFaq.as_view()),
    path('utility/<uuid:id_string>/service/type/list',ServiceTypeList.as_view()),
    path('service/type/<uuid:id_string>',ServiceTypeDetail.as_view()),
    path('service/type',ServiceType.as_view()),
    path('utility/<uuid:id_string>/service/subtype/list',ServiceSubTypeList.as_view()),
    path('service/subtype/<uuid:id_string>', ServiceSubTypeDetail.as_view()),
    path('service/subtype', ServiceSubType.as_view()),
    path('<uuid:id_string>/service-contract-detail/list', ConsumerServiceContractDetailList.as_view()),
    path('<uuid:id_string>/note', ConsumerNote.as_view()),
    path('<uuid:id_string>/note/list', ConsumerNoteList.as_view())

    # path('<uuid:id_string>/ownerships',ConsumerOwnershipList.as_view()),
]