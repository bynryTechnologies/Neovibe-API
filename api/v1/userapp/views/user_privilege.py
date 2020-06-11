import traceback
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status, generics
from api.messages import *
from master.models import get_user_by_id_string
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.models.sub_module import get_sub_module_by_id
from v1.commonapp.serializers.sub_module import SubModuleSerializer
from v1.commonapp.views.logger import logger
from v1.userapp.models.privilege import get_privilege_by_id
from v1.userapp.models.role_privilege import get_record_by_values
from v1.userapp.models.user_privilege import get_user_privilege_by_user_id, get_record_values_by_id
from v1.userapp.serializers.privilege import GetPrivilegeSerializer
from v1.userapp.serializers.user import GetUserSerializer
from v1.userapp.serializers.user_privilege import UserPrivilegeSerializer, UserPrivilegeViewSerializer
from v1.userapp.views.common_functions import set_user_privilege_validated_data


# API Header
# API end Point: api/v1/user/:id_string/privileges
# API verb: POST
# Package: Basic
# Modules: Roles & Privileges
# Sub Module: Privilege
# Interaction: Add user-privilege details
# Usage: Add privilege details
# Tables used: 2.5.1. Users & Privileges - User Privileges
# Author: Arpita
# Created on: 02/06/2020


class UserPrivilege(GenericAPIView):

    def post(self, request, format=None):
        try:
            response, user = is_token_valid(self.request.headers['token'])
            if response:
                if is_authorized(1, 1, 1, user):
                    data = []
                    module_list = request.data['module_id']
                    for module in module_list:
                        validate_data = {}
                        sub_module_list = module['sub_module_id']
                        for sub_module in sub_module_list:
                            validate_data['user_id'] = request.data['user_id']
                            validate_data['module_id'] = module['module_id']
                            validate_data['sub_module_id'] = sub_module['sub_module_id']
                            validate_data['privilege_id'] = sub_module['privilege_id']
                            validate_data['is_active'] = sub_module['is_active']
                            serializer = UserPrivilegeSerializer(data=validate_data)
                            if serializer.is_valid(raise_exception=False):
                                privilege_obj = serializer.create(serializer.validated_data, user)
                                view_serializer = UserPrivilegeViewSerializer(instance=privilege_obj,
                                                                          context={'request': request})
                                data.append(view_serializer.data)
                            else:
                                return Response({
                                    STATE: ERROR,
                                    RESULTS: serializer.errors,
                                }, status=status.HTTP_400_BAD_REQUEST)
                    return Response({
                        STATE: SUCCESS,
                        RESULTS: data,
                    }, status=status.HTTP_201_CREATED)
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
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)


# API Header
# API end Point: api/v1/user/:id_string/privileges
# API verb: POST
# Package: Basic
# Modules: Roles & Privileges
# Sub Module: Privilege
# Interaction: View privilege details, Edit privilege details
# Usage: View, Edit privilege details
# Tables used: 2.5.1. Users & Privileges - User Detail, User Privileges
# Author: Arpita
# Created on: 02/06/2020


class UserPrivilegeDetail(GenericAPIView):

    def get(self, request, id_string):
        try:
            response, user_obj = is_token_valid(self.request.headers['token'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    sub_modules = []
                    data = []
                    user = get_user_by_id_string(id_string)
                    if user:
                        users = GetUserSerializer(instance=user, context={'request': request})
                        data.append(users.data)
                        user_privileges = get_user_privilege_by_user_id(user.id)
                        for user_privilege in user_privileges:
                            sub_module_obj = get_sub_module_by_id(user_privilege.sub_module_id)
                            sub_module = SubModuleSerializer(instance=sub_module_obj, context={'request': request})
                            sub_modules.append(sub_module.data)
                            privilege_obj = get_privilege_by_id(user_privilege.privilege_id)
                            privilege = GetPrivilegeSerializer(instance=privilege_obj, context={'request': request})
                            index = sub_modules.index(sub_module.data)
                            sub_modules[index]['privilege'] = privilege.data

                        data[0]['sub_module'] = sub_modules
                        return Response({
                            STATE: SUCCESS,
                            RESULTS: data,
                        }, status=status.HTTP_200_OK)
                    else:
                        return Response({
                            STATE: EXCEPTION,
                            RESULTS: '',
                        }, status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response({
                        STATE: ERROR,
                        RESULTS: '',
                    }, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    STATE: ERROR,
                    RESULTS: '',
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logger().log(e, 'ERROR', user='test', name='test')
            return Response({
                STATE: EXCEPTION,
                RESULTS: '',
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, id_string):
        try:
            # Checking authentication start
            response, user = is_token_valid(self.request.headers['token'])
            if response:
                if is_authorized(1, 1, 1, user):
                    data = []
                    get_user = get_user_by_id_string(id_string)
                    if user:
                        module_list = request.data['module_id']
                        for module in module_list:
                            validate_data = {}
                            sub_module_list = module['sub_module_id']
                            for sub_module in sub_module_list:
                                validate_data['user_id'] = str(id_string)
                                validate_data['module_id'] = module['module_id']
                                validate_data['sub_module_id'] = sub_module['sub_module_id']
                                validate_data['privilege_id'] = sub_module['privilege_id']
                                validate_data['is_active'] = sub_module['is_active']
                                validated_data = set_user_privilege_validated_data(validate_data)
                                serializer = UserPrivilegeSerializer(data=validated_data)
                                if serializer.is_valid(raise_exception=False):
                                    user_privilege = get_record_values_by_id(get_user.id, validate_data['module_id'],
                                                                          validate_data['sub_module_id'],
                                                                          validate_data['privilege_id'])

                                    if user_privilege:
                                        user_privilege_obj = serializer.update(user_privilege, serializer.validated_data, user)
                                    else:
                                        user_privilege_obj = serializer.create(serializer.validated_data, user)
                                    view_serializer = UserPrivilegeViewSerializer(instance=user_privilege_obj,
                                                                                  context={'request': request})
                                    data.append(view_serializer.data)
                                else:
                                    return Response({
                                        STATE: ERROR,
                                        RESULTS: serializer.errors,
                                    }, status=status.HTTP_400_BAD_REQUEST)
                            return Response({
                                STATE: SUCCESS,
                                RESULTS: data,
                            }, status=status.HTTP_200_OK)
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
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)

