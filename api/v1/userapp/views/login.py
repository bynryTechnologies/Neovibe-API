import traceback
import jwt
from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.messages import *
from api.settings import SECRET_KEY
from v1.commonapp.views.logger import logger
from v1.userapp.models.user_master import get_user_by_username, get_user_by_id_string
from v1.userapp.models.user_token import UserToken, get_token_by_user_id


# API Header
# API end Point: api/v1/user/login
# API verb: GET
# Package: Basic
# Modules: User
# Interaction: user list
# Usage: API will fetch required data for user list
# Tables used: 2.5.3. User Details
# Author: Arpita
# Created on: 29/04/2020

def login(user):
    try:
        user_obj = get_user_by_username(user.username)
        token_obj = get_token_by_user_id(user_obj.id)
        if token_obj:
            token_obj.delete()
        payload = {'id_string': str(user_obj.id_string)}
        encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')
        token_obj = UserToken(user_id=user_obj.id, token=encoded_jwt)
        token_obj.save()
        return token_obj.token
    except Exception as e:
        logger().log(e, 'ERROR', user='test', name='test')
        return False


class LoginApiView(APIView):
    """Login Api View"""

    def post(self, request, format=None):
        try:
            username = request.data['username']
            password = request.data['password']

            auth = authenticate(username=username, password=password)

            if auth:
                token = login(auth)  # Call Login function

                if not token:
                    return Response({
                        STATE: FAIL,
                        RESULTS: INVALID_CREDENTIALS,
                    }, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    return Response({
                        STATE: SUCCESS,
                        RESULTS: SUCCESSFULLY_DATA_RETRIEVE,
                        Token: token,
                    }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: FAIL,
                    RESULTS: INVALID_CREDENTIALS,
                }, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as ex:
            print('file: {} api {} execption {}'.format('user', 'POST login', str(traceback.print_exc(ex))))
            logger().log(ex, 'ERROR', user='test', name='test')
            return Response({
                STATE: FAIL,
                RESULTS: SERVER_ERROR.format(str(ex)),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
