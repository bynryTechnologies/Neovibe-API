__author__ = "aki"

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status, generics
from master.models import get_user_by_id_string
#from api.constants import ADMIN, VIEW, TENANT, EDIT
from v1.userapp.decorators import is_token_validate, role_required
from v1.commonapp.views.custom_exception import InvalidAuthorizationException, InvalidTokenException
from v1.commonapp.views.logger import logger
from rest_framework.filters import OrderingFilter, SearchFilter
from v1.commonapp.common_functions import is_token_valid, is_authorized, get_user_from_token
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.tenant.models.tenant_master import get_tenant_by_id_string
from v1.tenant.serializers.tenant_bank_detail import TenantBankDetailViewSerializer, TenantBankDetailSerializer
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULT
from v1.tenant.models.tenant_bank_details import TenantBankDetail as TenantBankDetailTbl, \
    get_tenant_bank_details_by_id_string


# API Header
# API end Point: api/v1/tenant/id_string/bank/list
# API verb: GET
# Package: Basic
# Modules: Tenant
# Sub Module: Bank Details
# Interaction: View bank detail list
# Usage: This will display list of bank.
# Tables used: Tenant Bank Details
# Author: Akshay
# Created on: 20/05/2020

class TenantBankList(generics.ListAPIView):
    try:
        serializer_class = TenantBankDetailViewSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('tenant__id_string',)
        ordering_fields = ('bank_name',)
        ordering = ('bank_name',)  # always give by default alphabetical order
        search_fields = ('bank_name', 'branch_city' )

        def get_queryset(self):
            if is_token_valid(self.request.headers['token']):
                if is_authorized(1,1,1,1):
                    queryset = TenantBankDetailTbl.objects.filter(tenant__id_string=self.kwargs['id_string'], is_active=True)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'MEDIUM', module='ADMIN', sub_module='TENANT/BANK')
        raise APIException


# API Header
# API end Point: api/v1/tenant/id_string/bank
# API verb: POST
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: Add Tenant Bank
# Usage: Add Tenant Bank in the system
# Tables used: Tenant Bank Details
# Auther: Akshay
# Created on: 20/5/2020

class TenantBank (GenericAPIView):
    serializer_class = TenantBankDetailSerializer

    @is_token_validate
    #role_required(ADMIN, TENANT, EDIT)
    def post(self, request, id_string):
        try:
            user_id_string = get_user_from_token(request.headers['token'])
            user = get_user_by_id_string(user_id_string)
            tenant_obj = get_tenant_by_id_string(id_string)
            if tenant_obj:
                serializer = TenantBankDetailSerializer(data=request.data)
                if serializer.is_valid():
                    tenant_bank_obj = serializer.create(serializer.validated_data, tenant_obj, user)
                    serializer = TenantBankDetailViewSerializer(tenant_bank_obj, context={'request': request})
                    return Response({
                        STATE: SUCCESS,
                        RESULT: serializer.data,
                    }, status=status.HTTP_201_CREATED)
                else:
                    return Response({
                        STATE: ERROR,
                        RESULT: serializer.errors,
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            logger().log(ex, 'HIGH', module='ADMIN', sub_module='TENANT/BANK')
            response = self.handle_exception(ex)
            return Response({
                STATE: EXCEPTION,
                ERROR: str(ex)
            }, status=response.status_code)


# API Header
# API end Point: api/v1/tenant/bank/id_string
# API verb: Put,Get
# Package: Basic
# Modules: Tenant
# Sub Module: Bank
# Interaction: Get Tenant Bank , Update Tenant Bank
# Usage: Add and Update Tenant Bank in the system
# Tables used:  Tenant Bank details
# Auther: Akshay
# Created on: 18/5/2020

class TenantBankDetail(GenericAPIView):
    serializer_class = TenantBankDetailSerializer

    @is_token_validate
    #role_required(ADMIN, TENANT, VIEW)
    def get(self, request, id_string):
        try:
            tenant_bank_obj = get_tenant_bank_details_by_id_string(id_string)
            if tenant_bank_obj:
                serializer = TenantBankDetailViewSerializer(tenant_bank_obj, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULT: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            logger().log(ex, 'MEDIUM', module='ADMIN', sub_module='TENANT/BANK')
            response = self.handle_exception(ex)
            return Response({
                STATE: EXCEPTION,
                ERROR: str(ex)
            }, status=response.status_code)

    @is_token_validate
    #role_required(ADMIN, TENANT, EDIT)
    def put(self, request, id_string):
        try:
            user_id_string = get_user_from_token(request.headers['token'])
            user = get_user_by_id_string(user_id_string)
            tenant_bank_obj = get_tenant_bank_details_by_id_string(id_string)
            if tenant_bank_obj:
                serializer = TenantBankDetailSerializer(data=request.data)
                if serializer.is_valid():
                    tenant_bank_obj = serializer.update(tenant_bank_obj, serializer.validated_data, user)
                    serializer = TenantBankDetailViewSerializer(tenant_bank_obj, context={'request': request})
                    return Response({
                        STATE: SUCCESS,
                        RESULT: serializer.data,
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        STATE: ERROR,
                        RESULT: serializer.errors,
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            logger().log(ex, 'HIGH', module='ADMIN', sub_module='TENANT/BANK')
            response = self.handle_exception(ex)
            return Response({
                STATE: EXCEPTION,
                ERROR: str(ex)
            }, status=response.status_code)
