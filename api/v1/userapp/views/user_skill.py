import traceback
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from api.messages import *
from api.constants import *
from master.models import get_user_by_id_string
from v1.commonapp.common_functions import get_user_from_token
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.commonapp.views.logger import logger
from v1.userapp.decorators import is_token_validate, role_required
from v1.userapp.models.user_skill import get_skill_by_user_id, get_record_by_values
from v1.userapp.serializers.user_skill import UserSkillSerializer, UserSkillViewSerializer
from v1.userapp.views.common_functions import set_user_skill_validated_data


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

    @is_token_validate
    #role_required(ADMIN, UTILITY_MASTER, EDIT)
    def get(self, request, id_string):
        try:
            data = {}
            skill_list = []
            user = get_user_by_id_string(id_string)
            if user:
                data['email'] = user.email
                data['id_string'] = id_string
                user_skills = get_skill_by_user_id(user.id)
                if user_skills:
                    for user_skill in user_skills:
                        skill = UserSkillViewSerializer(instance=user_skill, context={'request': request})
                        skill_list.append(skill.data['skill'])
                    data['skills']  = skill_list
                    return Response({
                        STATE: SUCCESS,
                        DATA: data,
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        STATE: ERROR,
                        DATA: SKILL_NOT_ASSIGNED,
                    }, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({
                    STATE: EXCEPTION,
                    DATA: ID_STRING_NOT_FOUND,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'MEDIUM', module = 'Admin', sub_module = 'User Skills')
            return Response({
                STATE: EXCEPTION,
                DATA: '',
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @is_token_validate
    #role_required(ADMIN, UTILITY_MASTER,  EDIT)
    def post(self, request, id_string):
        try:
            skill_list = []
            data = {}
            user_obj = get_user_by_id_string(id_string)
            if user_obj:
                data['email'] = user_obj.email
                data['id_string'] = id_string
                for skill in request.data:
                    validate_data = {'user_id': str(id_string), 'skill_id': skill['skill_id_string']}
                    serializer = UserSkillSerializer(data=validate_data)
                    if serializer.is_valid(raise_exception=False):
                        user_id_string = get_user_from_token(request.headers['Authorization'])
                        user = get_user_by_id_string(user_id_string)
                        user_skill_obj = serializer.create(serializer.validated_data, user)
                        view_serializer = UserSkillViewSerializer(instance=user_skill_obj,
                                                                 context={'request': request})
                        skill_list.append(view_serializer.data['skill'])
                    else:
                        return Response({
                            STATE: ERROR,
                            RESULTS: serializer.errors,
                        }, status=status.HTTP_400_BAD_REQUEST)
                data['skills'] = skill_list
                return Response({
                    STATE: SUCCESS,
                    RESULTS: data,
                }, status=status.HTTP_201_CREATED)
            else:
                raise CustomAPIException(ID_STRING_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'HIGH', module = 'Admin', sub_module = 'User Skills')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)

    @is_token_validate
    #role_required(ADMIN, UTILITY_MASTER,  EDIT)
    def put(self, request, id_string):
        try:
            skill_list = []
            data = {}
            user_obj = get_user_by_id_string(id_string)
            if user_obj:
                data['email'] = user_obj.email
                data['id_string'] = id_string
                for skill in request.data['skills']:
                    validate_data = {'user_id': str(id_string), 'skill_id': skill['skill_id_string'],
                                     "is_active": skill['is_active']}
                    validated_data = set_user_skill_validated_data(validate_data)
                    serializer = UserSkillSerializer(data=validated_data)
                    if serializer.is_valid(raise_exception=False):
                        user_skill = get_record_by_values(str(id_string), validate_data['skill_id'])
                        user_id_string = get_user_from_token(request.headers['token'])
                        user = get_user_by_id_string(user_id_string)
                        if user_skill:
                            user_skill_obj = serializer.update(user_skill, serializer.validated_data, user)
                        else:
                            user_skill_obj = serializer.create(serializer.validated_data, user)
                        view_serializer = UserSkillViewSerializer(instance=user_skill_obj,
                                                                 context={'request': request})
                        skill_list.append(view_serializer.data['skill'])
                    else:
                        return Response({
                            STATE: ERROR,
                            RESULTS: serializer.errors,
                        }, status=status.HTTP_400_BAD_REQUEST)
                data['skills'] = skill_list
                return Response({
                    STATE: SUCCESS,
                    RESULTS: data,
                }, status=status.HTTP_200_OK)
            else:
                raise CustomAPIException(ID_STRING_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'HIGH', module = 'Admin', sub_module = 'User Skilss')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)
