__author__ = "aki"

import traceback
from api.constants import *
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULTS
from v1.userapp.decorators import is_token_validate, role_required
from v1.commonapp.models.notes import get_notes_by_utility_id_string, get_note_by_id_string
from v1.commonapp.views.logger import logger
from v1.utility.models.utility_master import get_utility_by_id_string
from v1.utility.serializers.notes import NoteSerializer


# API Header
# API end Point: api/v1/utility/id_string/notes
# API verb: GET, POST
# Package: Basic
# Modules: Utility
# Sub Module: Notes
# Interaction: for get and add utility notes
# Usage: API will fetch and add all notes under utility.
# Tables used: 2.5.12 Notes
# Author: Akshay
# Created on: 13/05/2020


class UtilityNoteList(GenericAPIView):
    @is_token_validate
    @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def get(self, request, id_string):
        try:
            utility_notes_obj = get_notes_by_utility_id_string(id_string)
            if utility_notes_obj:
                serializer = NoteSerializer(utility_notes_obj, many=True, context={'request': request})
                if serializer.is_valid():
                    return Response({
                        STATE: SUCCESS,
                        RESULTS: serializer.data,
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        STATE: SUCCESS,
                        RESULTS: serializer.errors,
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            logger().log(ex, 'MEDIUM', module='ADMIN', sub_module='UTILITY/NOTE')
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(ex))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @is_token_validate
    @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def post(self, request, id_string):
        try:
            utility_obj = get_utility_by_id_string(id_string)
            if utility_obj:
                serializer = NoteSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.validated_data['utility'] = utility_obj.id
                    serializer.create(serializer.validated_data, request.user)
                    return Response({
                        STATE: SUCCESS,
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        STATE: SUCCESS,
                        RESULTS: serializer.errors,
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            logger().log(ex, 'MEDIUM', module='ADMIN', sub_module='UTILITY/NOTE')
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(ex))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# API Header
# API end Point: api/v1/utility/note/id_string
# API verb: GET, PUT
# Package: Basic
# Modules: Utility
# Sub Module: Notes
# Interaction: for get and edit utility note
# Usage: API will fetch and edit note under utility.
# Tables used: 2.5.12 Notes
# Author: Gauri Deshmukh
# Created on: 13/05/2020


class UtilityNoteDetail(GenericAPIView):
    @is_token_validate
    @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def get(self, request, id_string):
        try:
            utility_notes_obj = get_note_by_id_string(id_string)
            if utility_notes_obj:
                serializer = NoteSerializer(utility_notes_obj, context={'request': request})
                if serializer.is_valid():
                    return Response({
                        STATE: SUCCESS,
                        RESULTS: serializer.data,
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        STATE: SUCCESS,
                        RESULTS: serializer.errors,
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            logger().log(ex, 'MEDIUM', module='ADMIN', sub_module='UTILITY/NOTE')
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(ex))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @is_token_validate
    @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def put(self, request, id_string):
        try:
            utility_note_obj = get_note_by_id_string(id_string)
            if utility_note_obj:
                serializer = NoteSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.create(serializer.validated_data, request.user)
                    return Response({
                        STATE: SUCCESS,
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        STATE: SUCCESS,
                        RESULTS: serializer.errors,
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            logger().log(ex, 'MEDIUM', module='ADMIN', sub_module='UTILITY/NOTE')
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(ex))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
