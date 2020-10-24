import traceback

from rest_framework import status,generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from v1.commonapp.views.logger import logger
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULT
from rest_framework.exceptions import APIException
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from v1.commonapp.common_functions import is_token_valid, is_authorized
from api.messages import *
from v1.commonapp.models.department import Department as DepartmentTbl,get_department_by_tenant_id_string, get_department_by_id_string
from v1.commonapp.serializers.department import DepartmentListSerializer, DepartmentViewSerializer
from v1.commonapp.views.pagination import StandardResultsSetPagination

# API Header
# API end Point: api/v1/department/list
# API verb: GET
# Package: Basic
# Modules: Lookup
# Sub Module: Lookup
# Interaction: View Departments
# Usage: This will get the list of departments
# Tables used: Lookup - 2.12.16 Lookup - Department
# Author: Arpita
# Created on: 06/05/2020
# Updated on: 12/05/2020


class DepartmentList(generics.ListAPIView):
    try:
        serializer_class = DepartmentListSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('tenant__id_string', 'utility__id_string')
        ordering_fields = ('name', 'tenant__name', 'utility__name')
        ordering = ('name',)  # always give by default alphabetical order
        search_fields = ('name', 'tenant__name', 'utility__name',)

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1,1,1,user_obj):
                    queryset = DepartmentTbl.objects.filter(utility__id_string=self.kwargs['id_string'], is_active=True)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'ERROR')
        raise APIException


# API Header
# API end Point: api/v1/department
# API verb: GET
# Package: Basic
# Modules: Lookup
# Sub Module: Lookup
# Interaction: View Department
# Usage: This will get the detail of department
# Tables used: Lookup - 2.12.16 Lookup - Department
# Author: Arpita
# Created on: 12/05/2020


class Department(GenericAPIView):

    def get(self, request, id_string):
        try:
            department = get_department_by_id_string(id_string)
            if department:
                serializer = DepartmentViewSerializer(instance=department, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    DATA: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: EXCEPTION,
                    DATA: '',
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({
                STATE: EXCEPTION,
                DATA: '',
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)