import traceback
import uuid

import jwt

from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.messages import *
from api.settings import SECRET_KEY
from v1.commonapp.models.form_factor import get_form_factor_by_id
from v1.commonapp.views.logger import logger
from v1.userapp.models.login_trail import LoginTrail
from v1.userapp.models.user_master import get_user_by_username, authenticate_user, get_user_by_username_password
from v1.userapp.models.user_token import UserToken, get_token_by_user_id


# def authenticate(username, password):
#     encrypted_password = make_password(password)
#     if authenticate_user(username, encrypted_password):
#         return get_user_by_username_password(username, encrypted_password)
#     else:
#         return False


def validate_login_data(request):
    if 'username' in request.data and 'password' in request.data:
        return True
    else:
        return False


def set_login_trail(username, password, status):
    LoginTrail(
        username=username,
        password=password,
        status=status
    ).save()


def login(request, user):
    try:
        user_obj = get_user_by_username(user.username)
        form_factor = get_form_factor_by_id(user_obj.form_factor_id)
        if form_factor.name == 'Mobile':
            if request.data['imei'] != user_obj.imei:
                return False
        payload = {'user_id_string': str(user_obj.id_string), 'string': str(uuid.uuid4().hex[:6].upper())}
        encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        token_obj = UserToken(
            tenant=user_obj.tenant,
            form_factor=user_obj.form_factor_id,
            user_id=user_obj.id,
            token=encoded_jwt,
            ip_address=ip,
            created_by=user.id,
            is_active=True
        )
        token_obj.save()
        return token_obj.token
    except Exception as e:
        logger().log(e, 'ERROR', user='test', name='test')
        return False


# API Header
# API end Point: api/v1/user/login
# API verb: GET
# Package: Basic
# Modules: User
# Interaction: user list
# Usage: API will fetch required data for user list
# Tables used: 2.5.3. User Details
# Author: Arpita
# Created on: 23/05/2020


class LoginApiView(APIView):
    """Login Api View"""

    def post(self, request, format=None):
        try:
            if validate_login_data(request):
                username = request.data['username']
                password = request.data['password']

                auth = authenticate(username=username, password=password)

                if auth:
                    token = login(request, auth)  # Call Login function

                    if not token:
                        set_login_trail(username, password, 'Fail')
                        return Response({
                            STATE: FAIL,
                            RESULTS: INVALID_CREDENTIALS,
                        }, status=status.HTTP_401_UNAUTHORIZED)
                    else:
                        set_login_trail(username, password, 'Success')
                        return Response({
                            STATE: SUCCESS,
                            RESULTS: SUCCESSFULLY_DATA_RETRIEVE,
                            Token: token,
                        }, status=status.HTTP_200_OK)
                else:
                    set_login_trail(username, password, 'Fail')
                    return Response({
                        STATE: FAIL,
                        RESULTS: INVALID_CREDENTIALS,
                    }, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as ex:
            print('file: {} api {} execption {}'.format('user', 'POST login', str(traceback.print_exc(ex))))
            logger().log(ex, 'ERROR', user='test', name='test')
            return Response({
                STATE: FAIL,
                RESULTS: SERVER_ERROR.format(str(ex)),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
