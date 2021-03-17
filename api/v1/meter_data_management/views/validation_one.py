__author__ = "aki"

from rest_framework.exceptions import APIException
from rest_framework import generics
from v1.commonapp.views.logger import logger
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from v1.commonapp.views.custom_exception import InvalidTokenException, InvalidAuthorizationException
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.meter_data_management.models.meter_reading import MeterReading as MeterReadingTbl
from v1.meter_data_management.serializers.validation_one import ValidationOneViewSerializer


# API Header
# API end Point: api/v1/meter-data/validation-one/schedule-log/<uuid:schedule_log>/read-cycle/<uuid:read_cycle>/list
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: meter reading list
# Usage: API will fetch required data for meter reading list against filter and search
# Tables used: Meter Reading
# Author: Akshay
# Created on: 16/03/2021


class ValidationOneList(generics.ListAPIView):
    try:
        serializer_class = ValidationOneViewSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('utility__id_string',)
        ordering_fields = ('utility__id_string',)
        ordering = ('utility__id_string',) # always give by default alphabetical order
        search_fields = ('utility__name',)

        def get_serializer_context(self):
            """
            Extra context provided to the serializer class.
            """
            token, user_obj = is_token_valid(self.request.headers['Authorization'])
            return {
                'user_id_string': user_obj,
                'schedule_log_id_string': self.kwargs['schedule_log'],
                'read_cycle_id_string': self.kwargs['read_cycle'],
            }

        def get_queryset(self):
            token, user_obj = is_token_valid(self.request.headers['Authorization'])
            if token:
                if is_authorized(1,1,1,user_obj):
                    queryset = MeterReadingTbl.objects.filter(is_active=True)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'LOW', module='CONSUMER OPS', sub_module='METER DATA')
        raise APIException