import traceback
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.decorators import permission_classes
from v1.commonapp.common_functions import is_authorized, is_token_valid, get_user_from_token
from v1.utility.models.utility_master import get_utility_by_id_string
from v1.commonapp.views.custom_exception import InvalidAuthorizationException, InvalidTokenException, CustomAPIException
from api.messages import *
from api.constants import *
from master.models import get_user_by_id_string
from v1.commonapp.common_functions import get_user_from_token
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.userapp.decorators import utility_required, is_token_validate, role_required
from v1.userapp.models.role import get_role_by_id_string, get_all_role, get_role_by_type_and_sub_type, Role as RoleModel
from v1.userapp.serializers.role import RoleListSerializer, RoleSerializer, RoleDetailViewSerializer

# API Header
# API end Point: api/v1/role/list
# API verb: GET
# Package: Basic
# Modules: Roles & Privileges
# Sub Module: Role
# Interaction: View role list
# Usage: Used for role list. Gets all the records in pagination mode. It also have input params to filter/search and
# sort in addition to pagination.
# Tables used: 2.5.1. Users & Privileges - Role
# Author: Arpita
# Created on: 04/05/2020
# Updated on: 09/05/2020


class RoleList(generics.ListAPIView):
    serializer_class = RoleListSerializer
    pagination_class = StandardResultsSetPagination

    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_fields = ('role', 'tenant__id_string', 'utility__id_string')
    ordering_fields = ('role',)
    ordering = ('created_date',)  # always give by default alphabetical order
    search_fields = ('role',)

    def get_queryset(self):
        queryset = get_all_role()
        return queryset


# API Header
# API end Point: api/v1/role
# API verb: POST
# Package: Basic
# Modules: Roles & Privileges
# Sub Module: Role
# Interaction: Add roles
# Usage: Add Role
# Tables used: 2.5.1. Users & Privileges - Role
# Author: Arpita
# Created on: 05/05/2020
# Updated on: 12/05/2020

class Role(GenericAPIView):

    @is_token_validate
    #role_required(ADMIN, UTILITY_MASTER,  EDIT)
    def post(self, request, format=None):
        try:
            serializer = RoleSerializer(data=request.data)
            if serializer.is_valid(raise_exception=False):
                user_id_string = get_user_from_token(request.headers['Authorization'])
                user = get_user_by_id_string(user_id_string)
                role_obj = serializer.create(serializer.validated_data, user)
                view_serializer = RoleDetailViewSerializer(instance=role_obj, context={'request': request})
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
            logger().log(e, 'HIGH', module = 'Admin', sub_module = 'Role')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)


# API Header
# API end Point: api/v1/role/:id_string
# API verb: GET, PUT
# Package: Basic
# Modules: Roles & Privileges
# Sub Module: Role
# Interaction: Get roles, Put roles
# Usage: Get Role, Put roles
# Tables used: 2.5.1. Users & Privileges - Role
# Author: Arpita
# Created on: 05/05/2020
# Updated on: 12/05/2020

class RoleDetail(GenericAPIView):

    @is_token_validate
    #role_required(DEMOM, DEMOSM, EDIT)
    def get(self, request, id_string):
        try:
            role = get_role_by_id_string(id_string)
            if role:
                serializer = RoleDetailViewSerializer(instance=role, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULTS: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: EXCEPTION,
                    RESULTS: ID_STRING_NOT_FOUND,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'MEDIUM', module = 'Admin', sub_module = 'Role')
            return Response({
                STATE: EXCEPTION,
                RESULTS: '',
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @is_token_validate
    #role_required(ADMIN, UTILITY_MASTER,  EDIT)
    def put(self, request, id_string):
        try:
            role_obj = get_role_by_id_string(id_string)
            if role_obj:
                serializer = RoleSerializer(data=request.data)
                if serializer.is_valid(raise_exception=False):
                    user_id_string = get_user_from_token(request.headers['token'])
                    user = get_user_by_id_string(user_id_string)
                    role_obj = serializer.update(role_obj, serializer.validated_data, user)
                    view_serializer = RoleDetailViewSerializer(instance=role_obj, context={'request': request})
                    return Response({
                        STATE: SUCCESS,
                        RESULTS: view_serializer.data,
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        STATE: ERROR,
                        RESULTS: serializer.errors,
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                raise CustomAPIException(ID_STRING_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'HIGH', module = 'Admin', sub_module = 'Role')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)


# API Header
# API end Point: api/v1/type/:id_string/sub-type/:id_string
# API verb: GET
# Package: Basic
# Modules: Roles & Privileges
# Sub Module: Role
# Interaction: Get role
# Usage: Get Role
# Tables used: 2.5.1. Users & Privileges - Role
# Author: Arpita
# Created on: 30/10/2020
# Updated on: 30/10/2020

class GetRoleDetail(GenericAPIView):

    @is_token_validate
    #role_required(ADMIN, UTILITY_MASTER, EDIT)
    def get(self, request, type_id_string, sub_type_id_string):
        try:
            role_list = []
            roles = get_role_by_type_and_sub_type(type_id_string, sub_type_id_string)
            if roles:
                for role in roles:
                    serializer = RoleDetailViewSerializer(instance=role, context={'request': request})
                    role_list.append(serializer.data)
                return Response({
                    STATE: SUCCESS,
                    RESULTS: role_list,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: EXCEPTION,
                    RESULTS: ROLES_NOT_FOUND,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'MEDIUM', module = 'Admin', sub_module = 'Role')
            return Response({
                STATE: EXCEPTION,
                RESULTS: '',
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RoleListByUtility(generics.ListAPIView):
    try:
        serializer_class = RoleListSerializer
        pagination_class = StandardResultsSetPagination

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    utility = get_utility_by_id_string(self.kwargs['id_string'])
                    queryset = RoleModel.objects.filter(utility=utility, is_active=True)

                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Role not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Admin', sub_module='Role')

