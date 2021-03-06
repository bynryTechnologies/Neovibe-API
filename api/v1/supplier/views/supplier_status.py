__author__ = "aki"

from rest_framework.exceptions import APIException
from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from v1.commonapp.views.custom_exception import InvalidTokenException, InvalidAuthorizationException
from v1.commonapp.views.logger import logger
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.supplier.serializers.supplier_status import SupplierStatusViewSerializer
from v1.supplier.models.supplier_status import SupplierStatus as SupplierStatusTbl


# API Header
# API end Point: api/v1/supplier/status/list
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: Supplier status list
# Usage: API will fetch required data for supplier status list against filter and search
# Tables used: SupplierStatus
# Author: Akshay
# Created on: 28/05/2020

class SupplierStatusList(generics.ListAPIView):
    try:
        serializer_class = SupplierStatusViewSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('id_string',)
        ordering_fields = ('name',)
        ordering = ('name',) # always give by default alphabetical order
        search_fields = ('name',)

        def get_queryset(self):
            if is_token_valid(self.request.headers['token']):
                if is_authorized():
                    queryset = SupplierStatusTbl.objects.filter(is_active=True)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'ERROR')
        raise APIException