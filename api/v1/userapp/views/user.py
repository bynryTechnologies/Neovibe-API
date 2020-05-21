import traceback
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from api.messages import *
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.userapp.models.role import get_role_by_id
from v1.userapp.models.user_bank_detail import get_bank_by_id
from v1.userapp.models.user_master import get_user_by_id_string, get_all_users, \
    get_user_by_id
from v1.userapp.models.user_role import get_user_role_by_user_id
from v1.userapp.serializers.bank_detail import UserBankViewSerializer
from v1.userapp.serializers.role import RoleViewSerializer
from v1.userapp.serializers.user import UserListSerializer, UserViewSerializer, UserPrivilegeViewSerializer, \
    UserSerializer
from v1.userapp.views.common_functions import is_user_data_verified, is_privilege_data_verified, add_user_privilege, \
    save_edited_privilege


# API Header
# API end Point: api/v1/user/list
# API verb: GET
# Package: Basic
# Modules: User
# Sub Module: User
# Interaction: View user list
# Usage: Used for user list. Get all the records in pagination mode. It also have input params to filter/ search and
# sort in addition to pagination.
# Tables used: 2.5.3. Users & Privileges - User Details
# Author: Arpita
# Created on: 11/05/2020
# Updated on: 21/05/2020


class UserList(generics.ListAPIView):
    serializer_class = UserListSerializer
    pagination_class = StandardResultsSetPagination

    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_fields = ('tenant__id_string', 'utility__id_string')
    ordering_fields = ('first_name', 'last_name',)
    ordering = ('created_date',)  # always give by default alphabetical order
    search_fields = ('first_name', 'email_id')

    def get_queryset(self):
        queryset = get_all_users()
        return queryset


# API Header
# API end Point: api/v1/user
# API verb: POST
# Package: Basic
# Modules: User
# Sub Module: User
# Interaction: Add users
# Usage: Add User
# Tables used: 2.5.3. Users & Privileges - User Details
# Author: Arpita
# Created on: 13/05/2020
# Updated on: 14/05/2020

class User(GenericAPIView):

    def post(self, request, format=None):
        try:
            if is_token_valid(self.request.headers['token']):
                if is_authorized():
                    if is_user_data_verified(request):
                        user = get_user_by_id(3)
                        serializer = UserSerializer(data=request.data)
                        if serializer.is_valid():
                            user_obj = serializer.create(serializer.validated_data, user)
                            view_serializer = UserViewSerializer(instance=user_obj, context={'request': request})
                            return Response({
                                STATE: SUCCESS,
                                RESULTS: view_serializer.data,
                            }, status=status.HTTP_201_CREATED)
                        else:
                            return Response({
                                STATE: ERROR,
                                RESULTS: serializer.errors,
                            }, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({
                            STATE: ERROR,
                        }, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({
                        STATE: ERROR,
                    }, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logger().log(e, 'ERROR', user='test', name='test')
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# API Header
# API end Point: api/v1/user/:id_string
# API verb: GET, PUT
# Package: Basic
# Modules: User
# Sub Module: User
# Interaction: View users, Edit users
# Usage: View, Edit User
# Tables used: 2.5.3. Users & Privileges - User Details
# Author: Arpita
# Created on: 13/05/2020
# Updated on: 21/05/2020


class UserDetail(GenericAPIView):

    def get(self, request, id_string):
        try:
            if is_token_valid(self.request.headers['token']):
                if is_authorized():
                    user = get_user_by_id_string(id_string)
                    if user:
                        serializer = UserViewSerializer(instance=user, context={'request': request})
                        return Response({
                            STATE: SUCCESS,
                            DATA: serializer.data,
                        }, status=status.HTTP_200_OK)
                    else:
                        return Response({
                            STATE: EXCEPTION,
                            DATA: '',
                        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    return Response({
                        STATE: ERROR,
                    }, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logger().log(e, 'ERROR', user='test', name='test')
            return Response({
                STATE: EXCEPTION,
                DATA: '',
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, id_string):
        try:
            if is_token_valid(self.request.headers['token']):
                if is_authorized():
                    if is_user_data_verified(request):
                        user = get_user_by_id(3)
                        user_obj = get_user_by_id_string(id_string)
                        if user_obj:
                            serializer = UserSerializer(data=request.data)
                            if serializer.is_valid():
                                user_obj = serializer.update(user_obj, serializer.validated_data, user)
                                view_serializer = UserViewSerializer(instance=user_obj, context={'request': request})
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
                            return Response({
                                STATE: ERROR,
                            }, status=status.HTTP_404_NOT_FOUND)
                    else:
                        return Response({
                            STATE: ERROR,
                        }, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({
                        STATE: ERROR,
                    }, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logger().log(e, 'ERROR', user='test', name='test')
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# API Header
# API end Point: api/v1/user/:id_string/bank
# API verb: GET, POST, PUT
# Package: Basic
# Modules: User
# Sub Module: User
# Interaction: View, Add, Edit user bank detail
# Usage: View, Add, Edit User bank detail
# Tables used: 2.5 Users & Privileges - User Bank Details
# Author: Arpita
# Created on: 21/05/2020


class UserBankDetail(GenericAPIView):

    def get(self, request, id_string):
        try:
            if is_token_valid(self.request.headers['token']):
                if is_authorized():
                    user = get_user_by_id_string(id_string)
                    bank = get_bank_by_id(user.bank_detail_id)
                    if user:
                        serializer = UserBankViewSerializer(instance=bank, context={'request': request})
                        return Response({
                            STATE: SUCCESS,
                            DATA: serializer.data,
                        }, status=status.HTTP_200_OK)
                    else:
                        return Response({
                            STATE: EXCEPTION,
                            DATA: '',
                        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    return Response({
                        STATE: ERROR,
                    }, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logger().log(e, 'ERROR', user='test', name='test')
            return Response({
                STATE: EXCEPTION,
                DATA: '',
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, id_string):
        try:
            if is_token_valid(self.request.headers['token']):
                if is_authorized():
                    if is_user_data_verified(request):
                        user = get_user_by_id(3)
                        user_obj = get_user_by_id_string(id_string)
                        if user_obj:
                            serializer = UserSerializer(data=request.data)
                            if serializer.is_valid():
                                user_obj = serializer.update(user_obj, serializer.validated_data, user)
                                view_serializer = UserViewSerializer(instance=user_obj, context={'request': request})
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
                            return Response({
                                STATE: ERROR,
                            }, status=status.HTTP_404_NOT_FOUND)
                    else:
                        return Response({
                            STATE: ERROR,
                        }, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({
                        STATE: ERROR,
                    }, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logger().log(e, 'ERROR', user='test', name='test')
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, id_string):
        try:
            if is_token_valid(self.request.headers['token']):
                if is_authorized():
                    if is_user_data_verified(request):
                        user = get_user_by_id(3)
                        user_obj = get_user_by_id_string(id_string)
                        if user_obj:
                            serializer = UserSerializer(data=request.data)
                            if serializer.is_valid():
                                user_obj = serializer.update(user_obj, serializer.validated_data, user)
                                view_serializer = UserViewSerializer(instance=user_obj, context={'request': request})
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
                            return Response({
                                STATE: ERROR,
                            }, status=status.HTTP_404_NOT_FOUND)
                    else:
                        return Response({
                            STATE: ERROR,
                        }, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({
                        STATE: ERROR,
                    }, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logger().log(e, 'ERROR', user='test', name='test')
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# API Header
# API end Point: api/v1/user/role
# API verb: GET
# Package: Basic
# Modules: User
# Sub Module: User
# Interaction: Get user role list
# Usage: get User role and privileges
# Tables used: 2.5.2. Users & Privileges - Role Privileges
# Author: Arpita
# Created on: 14/05/2020


class UserPrivilege(GenericAPIView):

    def get(self, request, id_string):
        try:
            user = get_user_by_id_string(id_string)
            privileges = get_user_role_by_user_id(user.id)
            for privilege in privileges:
                serializer = UserPrivilegeViewSerializer(instance=privilege, context={'request': request})

            if user:
                serializer = UserPrivilegeViewSerializer(instance=user, context={'request': request})
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


# API Header
# API end Point: api/v1/user/role
# API verb: POST, PUT
# Package: Basic
# Modules: User
# Sub Module: User
# Interaction: Add user notes, Edit user role and privilege
# Usage: Add, Edit User role and privileges
# Tables used: 2.5.2. Users & Privileges - Role Privileges
# Author: Arpita
# Created on: 14/05/2020
# Updated on: 21/05/2020

class UserRole(GenericAPIView):

    def get(self, request, id_string):
        try:
            if is_token_valid(self.request.headers['token']):
                if is_authorized():
                    role_list = []
                    user = get_user_by_id_string(id_string)
                    user_roles = get_user_role_by_user_id(user.id)
                    if user_roles:
                        for user_role in user_roles:
                            role_obj = get_role_by_id(user_role.role_id)
                            role = RoleViewSerializer(instance=role_obj, context={'request': request})
                            role_list.append(role.data)
                        return Response({
                            STATE: SUCCESS,
                            DATA: role_list,
                        }, status=status.HTTP_200_OK)
                    else:
                        return Response({
                            STATE: ERROR,
                            DATA: 'No records found.',
                        }, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({
                        STATE: ERROR,
                    }, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logger().log(e, 'ERROR', user='test', name='test')
            return Response({
                STATE: EXCEPTION,
                DATA: '',
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        try:

            # Request data verification start
            if is_privilege_data_verified(request):
                # Request data verification end

                # Save basic user details start
                user = get_user_by_id_string(request.data['user'])
                user_detail, result, error = add_user_privilege(request, user)
                if result:
                    data = {
                        "user_id_string": user_detail.id_string
                    }
                    return Response({
                        STATE: SUCCESS,
                        DATA: data,
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        STATE: EXCEPTION,
                        ERROR: error
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                # Save basic role details start
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, format=None):
        try:

            # Request data verification start
            if is_privilege_data_verified(request):
                # Request data verification end

                # Edit basic details start
                user = get_user_by_id_string(request.data['user'])
                user_detail, result, error = save_edited_privilege(request, user)
                if result:
                    data = {
                        "user_detail_id_string": user_detail.id_string
                    }
                    return Response({
                        STATE: SUCCESS,
                        DATA: data,
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        STATE: EXCEPTION,
                        ERROR: error
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                # Edit basic details start
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
