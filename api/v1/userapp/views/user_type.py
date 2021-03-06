__author__ = "priyanka"

import traceback

from rest_framework.exceptions import APIException
from rest_framework.generics import GenericAPIView
from rest_framework import generics, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULT
from master.models import User
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.views.custom_exception import InvalidAuthorizationException, InvalidTokenException
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.userapp.models.user_type import UserType as UserTypeTbl
from v1.userapp.serializers.user_type import GetUserTypeSerializer


# API Header
# API end Point: api/v1/user/type
# API verb: GET
# Package: Basic
# Modules: User
# Sub Module: User
# Interaction: Get User Type list
# Usage: API will fetch required data for User Type list 
# Tables used: User Type
# Author: Priyanka
# Created on: 19/11/2020



class UserTypeList(generics.ListAPIView):
    try:
        serializer_class = GetUserTypeSerializer
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
                    queryset = UserTypeTbl.objects.filter(is_active=True)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'ERROR')
        raise APIException