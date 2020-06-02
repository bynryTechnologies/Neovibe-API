import traceback
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from api.messages import *
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.models.skills import get_skill_by_id
from v1.commonapp.serializers.skill import GetSkillSerializer
from v1.commonapp.views.logger import logger
from v1.userapp.models.user_master import get_user_by_id_string
from v1.userapp.models.user_skill import get_skill_by_user_id, get_record_by_values
from v1.userapp.serializers.user_skill import UserSkillSerializer, UserSkillViewSerializer
from v1.userapp.views.common_functions import is_user_skill_data_verified, set_user_skill_validated_data


# API Header
# API end Point: api/v1/user/:id_string/skill
# API verb: GET, POST, PUT
# Package: Basic
# Modules: User
# Sub Module: User
# Interaction: View, Add, Edit user skill
# Usage: View, Add, Edit User Skill
# Tables used: 2.5 Users & Privileges - User Skill
# Author: Arpita
# Created on: 02/06/2020


class UserSkill(GenericAPIView):

    def get(self, request, id_string):
        try:
            if is_token_valid(self.request.headers['token']):
                if is_authorized():
                    skill_list = []
                    user = get_user_by_id_string(id_string)
                    user_skills = get_skill_by_user_id(user.id)
                    if user_skills:
                        for user_skill in user_skills:
                            skill_obj = get_skill_by_id(user_skill.skill_id)
                            skill = GetSkillSerializer(instance=skill_obj, context={'request': request})
                            skill_list.append(skill.data)
                        return Response({
                            STATE: SUCCESS,
                            DATA: skill_list,
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
            if is_token_valid(self.request.headers['token']):
                if is_authorized():
                    data = []
                    if is_user_skill_data_verified(request):
                        success, user = is_token_valid(self.request.headers['token'])
                        for skill in request.data['skills']:
                            validate_data = {'user_id': str(id_string), 'skill_id': skill['skill_id_string']}
                            validated_data = set_user_skill_validated_data(validate_data)
                            serializer = UserSkillSerializer(data=validated_data)
                            if serializer.is_valid():
                                user_skill_obj = serializer.create(serializer.validated_data, user)
                                view_serializer = UserSkillViewSerializer(instance=user_skill_obj,
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
                    data = []
                    if is_user_skill_data_verified(request):
                        success, user = is_token_valid(self.request.headers['token'])
                        for skill in request.data['skills']:
                            validate_data = {'user_id': str(id_string), 'skill_id': skill['skill_id_string'],
                                             "is_active": skill['is_active']}
                            validated_data = set_user_skill_validated_data(validate_data)
                            serializer = UserSkillSerializer(data=validated_data)
                            if serializer.is_valid():
                                user_skill = get_record_by_values(str(id_string), validate_data['skill_id'])
                                if user_skill:
                                    user_skill_obj = serializer.update(user_skill, serializer.validated_data, user)
                                else:
                                    user_skill_obj = serializer.create(serializer.validated_data, user)
                                view_serializer = UserSkillViewSerializer(instance=user_skill_obj,
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
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
