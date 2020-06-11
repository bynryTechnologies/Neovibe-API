import traceback
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from api.messages import *
from master.models import get_user_by_id_string
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.models.area import get_area_by_id
from v1.commonapp.serializers.area import GetAreaSerializer
from v1.commonapp.views.logger import logger
from v1.userapp.models.user_area import get_area_by_user_id, get_record_by_values
from v1.userapp.serializers.user_area import UserAreaSerializer, UserAreaViewSerializer
from v1.userapp.views.common_functions import set_user_area_validated_data


# API Header
# API end Point: api/v1/user/:id_string/area
# API verb: GET, POST, PUT
# Package: Basic
# Modules: User
# Sub Module: User
# Interaction: View, Add, Edit user area
# Usage: View, Add, Edit User Area
# Tables used: 2.5 Users & Privileges - User Area
# Author: Arpita
# Created on: 02/06/2020


class UserArea(GenericAPIView):

    def get(self, request, id_string):
        try:
            response, user_obj = is_token_valid(self.request.headers['token'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    area_list = []
                    user = get_user_by_id_string(id_string)
                    user_areas = get_area_by_user_id(user.id)
                    if user_areas:
                        for user_area in user_areas:
                            area_obj = get_area_by_id(user_area.area_id)
                            area = GetAreaSerializer(instance=area_obj, context={'request': request})
                            area_list.append(area.data)
                        return Response({
                            STATE: SUCCESS,
                            DATA: area_list,
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

    def post(self, request, id_string):
        try:
            response, user_id_string = is_token_valid(self.request.headers['token'])
            if response:
                if is_authorized(1, 1, 1, user_id_string):
                    data = []
                    for area in request.data['areas']:
                        validate_data = {'user_id': str(id_string), 'area_id': area['area_id_string']}
                        serializer = UserAreaSerializer(data=validate_data)
                        if serializer.is_valid(raise_exception=False):
                            user = get_user_by_id_string(user_id_string)
                            user_area_obj = serializer.create(serializer.validated_data, user)
                            view_serializer = UserAreaViewSerializer(instance=user_area_obj,
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


def put(self, request, id_string):
        try:
            response, user = is_token_valid(self.request.headers['token'])
            if response:
                if is_authorized(1, 1, 1, user):
                    data = []
                    for area in request.data['areas']:
                        validate_data = {'user_id': str(id_string), 'area_id': area['area_id_string'],
                                         "is_active": area['is_active']}
                        validated_data = set_user_area_validated_data(validate_data)
                        serializer = UserAreaSerializer(data=validated_data)
                        if serializer.is_valid(raise_exception=False):
                            user_area = get_record_by_values(str(id_string), validate_data['area_id'])
                            if user_area:
                                user_area_obj = serializer.update(user_area, serializer.validated_data, user)
                            else:
                                user_area_obj = serializer.create(serializer.validated_data, user)
                            view_serializer = UserAreaViewSerializer(instance=user_area_obj,
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

