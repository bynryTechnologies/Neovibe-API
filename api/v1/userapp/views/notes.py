import traceback

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from api.messages import *
from master.models import get_user_by_id_string
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.models.notes import get_notes_by_user_id, get_note_by_id_string
from v1.commonapp.models.service_type import get_service_type_by_name
from v1.commonapp.views.logger import logger
from v1.userapp.serializers.notes import NoteSerializer, NoteViewSerializer


# API Header
# API end Point: api/v1/user/:/note
# API verb: GET, POST, PUT
# Package: Basic
# Modules: User
# Sub Module: User
# Interaction: Get, Add, Edit user role and privilege
# Usage: Get, Add, Edit User role and privileges
# Tables used: 2.5.12 Notes
# Author: Arpita
# Created on: 14/05/2020
# Updated on: 21/05/2020


class UserNote(GenericAPIView):

    def get(self, request, id_string):
        try:
            response, user = is_token_valid(self.request.headers['token'])
            if response:
                if is_authorized(1, 1, 1, user):
                    data = []
                    user = get_user_by_id_string(id_string)
                    service_type = get_service_type_by_name('User')
                    user_notes_obj = get_notes_by_user_id(user.id,service_type.id)
                    if user_notes_obj:
                        for user_note in user_notes_obj:
                            serializer = NoteViewSerializer(instance=user_note, context={'request': request})
                            data.append(serializer.data)
                        return Response({
                            STATE: SUCCESS,
                            RESULTS: data,
                        }, status=status.HTTP_200_OK)
                    else:
                        return Response({
                            STATE: ERROR,
                            RESULTS: '',
                        }, status=status.HTTP_404_NOT_FOUND)
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
                RESULTS: '',
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, id_string):
        try:
            response, user = is_token_valid(self.request.headers['token'])
            if response:
                if is_authorized(1, 1, 1, user):
                    request.data['identification_id'] = str(id_string)
                    serializer = NoteSerializer(data=request.data)
                    if serializer.is_valid(raise_exception=False):
                        note_obj = serializer.create(serializer.validated_data, user)
                        view_serializer = NoteViewSerializer(instance=note_obj, context={'request': request})
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
                    request.data['identification_id'] = str(id_string)
                    note = get_note_by_id_string(request.data['note_id'])
                    if note:
                        serializer = NoteSerializer(data=request.data)
                        if serializer.is_valid(raise_exception=False):
                            note_obj = serializer.update(note, serializer.validated_data, user)
                            view_serializer = NoteViewSerializer(instance=note_obj, context={'request': request})
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
