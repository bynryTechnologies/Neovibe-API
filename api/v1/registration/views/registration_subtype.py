from rest_framework import generics, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULTS
from rest_framework.exceptions import APIException
from v1.commonapp.views.custom_exception import InvalidTokenException, InvalidAuthorizationException
from v1.commonapp.views.pagination import StandardResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from v1.registration.models.registration_subtype import RegistrationSubType as RegistrationSubTypeModel,get_registration_subtype_by_id_string
from v1.registration.serializers.registration_subtype import RegistrationSubTypeListSerializer,RegistrationSubTypeSerializer,RegistrationSubTypeViewSerializer
from v1.commonapp.views.logger import logger
from v1.commonapp.common_functions import is_token_valid, get_payload, is_authorized
from rest_framework.response import Response
from v1.userapp.decorators import is_token_validate, role_required
from v1.utility.models.utility_master import get_utility_by_id_string
from v1.commonapp.common_functions import is_authorized, is_token_valid, get_user_from_token
from v1.commonapp.views.custom_exception import InvalidAuthorizationException, InvalidTokenException, CustomAPIException
from v1.commonapp.views.logger import logger
from master.models import get_user_by_id_string
from api.messages import *
from api.constants import *

# API Header
# API end Point: api/v1/registration/utility/:id_string/subtype/list
# API verb: GET
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Registration SubType list
# Usage: API will fetch all Registration Subtype list
# Tables used: Registration SubType
# Author: Chinmay
# Created on: 30/11/2020

class RegistrationSubTypeList(generics.ListAPIView):
    try:
        serializer_class = RegistrationSubTypeListSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('name', 'tenant__id_string',)
        ordering_fields = ('name', 'tenant',)
        ordering = ('name',)  # always give by default alphabetical order
        search_fields = ('name', 'tenant__name',)

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    utility = get_utility_by_id_string(self.kwargs['id_string'])
                    queryset = RegistrationSubTypeModel.objects.filter(utility=utility, is_active=True)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Registration Sub Type not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Admin', sub_module='Utility')

# API Header
# API end Point: api/v1/registration/subtype
# API verb: POST
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Registration post
# Usage: API will Post the Registartion SubType
# Tables used: Registration SubType
# Author: Chinmay
# Created on: 30/11/2020
class RegistrationSubType(GenericAPIView):

    @is_token_validate
    #role_required(ADMIN, UTILITY_MASTER, EDIT)
    def post(self, request):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            serializer = RegistrationSubTypeSerializer(data=request.data)
            if serializer.is_valid(raise_exception=False):
                registration_subtype_obj = serializer.create(serializer.validated_data, user)
                view_serializer = RegistrationSubTypeViewSerializer(instance=registration_subtype_obj, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULTS: view_serializer.data,
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    STATE: ERROR,
                    RESULTS: list(serializer.errors.values())[0][0],
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger().log(e, 'HIGH', module='Admin', sub_module='Utility')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULTS: str(e),
            }, status=res.status_code)


# API Header
# API end Point: api/v1/registration/subtype/:id_string
# API verb: GET,PUT
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Registration Type corresponding to the id
# Usage: API will fetch and update Registration SubTypes for a given id
# Tables used: Registration SubTypes
# Author: Chinmay
# Created on: 30/11/2020


class RegistrationSubTypeDetail(GenericAPIView):

    @is_token_validate
    #role_required(ADMIN, UTILITY_MASTER, EDIT)
    def get(self, request, id_string):
        try:
            registration_subtype = get_registration_subtype_by_id_string(id_string)
            if registration_subtype:
                serializer = RegistrationSubTypeViewSerializer(instance=registration_subtype, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULTS: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'MEDIUM', module='Admin', sub_module='Utility')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULTS: str(e),
            }, status=res.status_code)

    @is_token_validate
    #role_required(ADMIN, UTILITY_MASTER, EDIT)
    def put(self, request, id_string):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            registration_subtype_obj = get_registration_subtype_by_id_string(id_string)
            if "name" not in request.data:
                request.data['name'] = registration_subtype_obj.name
            if registration_subtype_obj:
                serializer = RegistrationSubTypeSerializer(data=request.data)
                if serializer.is_valid(raise_exception=False):
                    registration_subtype_obj = serializer.update(registration_subtype_obj, serializer.validated_data, user)
                    view_serializer = RegistrationSubTypeViewSerializer(instance=registration_subtype_obj,
                                                          context={'request': request})
                    return Response({
                        STATE: SUCCESS,
                        RESULTS: view_serializer.data,
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        STATE: ERROR,
                        RESULTS: list(serializer.errors.values())[0][0],
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'HIGH', module='Admin', sub_module='Utility')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULTS: str(e),
            }, status=res.status_code)
        
