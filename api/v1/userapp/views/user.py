import traceback
import rest_framework
from django.contrib.auth.decorators import login_required
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics
from v1.utility.models.utility_master import get_utility_by_id_string
from v1.userapp.models.user_utility import UserUtility
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, UpdateAPIView
from api.messages import *
from api.constants import *
from master.models import get_all_users, get_user_by_id_string, get_user_by_email, is_email_exists, User as UserTbl
from v1.userapp.models.user_utility import UserUtility
from v1.commonapp.common_functions import get_user_from_token, is_token_valid, is_authorized
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.userapp.decorators import is_token_validate, role_required, utility_required
from v1.userapp.serializers.user import UserListSerializer, UserViewSerializer, UserSerializer, \
    ResetPasswordEmailSerializer, SetNewPasswordSerializer, ChangePasswordSerializer
from v1.utility.models.utility_master import get_utility_by_id_string
from v1.userapp.serializers.user_utility import UserUtilityViewSerializer
from v1.userapp.models.user_skill import UserSkill
from v1.userapp.models.user_leaves import UserLeaves
import datetime
from v1.work_order.models.service_appointments import get_service_appointment_by_id_string, ServiceAppointment
from v1.work_order.models.work_order_master import get_work_order_master_by_id
from v1.commonapp.models.skills import get_skill_by_id_string
from v1.userapp.serializers.user_skill import UserSkillViewSerializer
from v1.commonapp.serializers.note import NoteSerializer, NoteViewSerializer, NoteListSerializer
from v1.commonapp.models.notes import Notes, get_note_by_id_string
from master.models import USER_DICT
from v1.commonapp.serializers.lifecycle import LifeCycleListSerializer
from v1.commonapp.models.lifecycle import LifeCycle
from v1.userapp.views.task import save_user_timeline
from django.db import transaction
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse, reverse_lazy
# from v1.userapp.utlis import Util
from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated, AllowAny
from master.models import User
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from v1.commonapp.models.module import get_module_by_key
from v1.commonapp.models.sub_module import get_sub_module_by_key
from v1.tenant.models.tenant_master import get_tenant_by_id_string


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
    try:
        serializer_class = UserListSerializer
        pagination_class = StandardResultsSetPagination
        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('first_name', 'last_name', 'tenant__id_string')
        ordering_fields = ('first_name', 'last_name',)
        ordering = ('created_date',)  # always give by default alphabetical order
        search_fields = ('first_name', 'email',)
        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                user_list = []
                if is_authorized(1, 1, 1, user_obj):
                    if 'tenant_id_string' in self.request.query_params:
                        tenant = get_tenant_by_id_string(self.request.query_params['tenant_id_string'])
                        queryset = UserTbl.objects.filter(tenant=tenant,is_active=True)
                    else:   
                        if 'utility_id_string' in self.request.query_params:
                            utility = get_utility_by_id_string(self.request.query_params['utility_id_string'])
                            user_utility = UserUtility.objects.filter(utility = utility,is_active=True)
                            for user in user_utility:
                                user_list.append(user.user_id)
                            queryset = UserTbl.objects.filter(id__in=user_list,is_active=True)
                        else:
                            queryset = UserTbl.objects.filter(is_active=True)    
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException(USER_NOT_FOUND, status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='USER', sub_module='USER')


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

    @is_token_validate
    #@role_required(USER, USER, EDIT)
    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid(raise_exception=False):
                if not is_email_exists(request.data['email']):
                    user_id_string = get_user_from_token(request.headers['Authorization'])
                    user = get_user_by_id_string(user_id_string)
                    with transaction.atomic():
                        user_obj = serializer.create(serializer.validated_data, user)

                        # State change for user start
                        user_obj.change_state(USER_DICT["ACTIVE"])
                        # State change for user end

                        # Timeline code start
                        transaction.on_commit(
                            lambda: save_user_timeline.delay(user_obj, "User", "User Created", "ACTIVE", user))
                        # Timeline code end

                    user_obj.save()
                    view_serializer = UserViewSerializer(instance=user_obj, context={'request': request})
                    return Response({
                        STATE: SUCCESS,
                        RESULTS: view_serializer.data,
                    }, status=status.HTTP_201_CREATED)
                else:
                    raise CustomAPIException(USER_ALREADY_EXISTS, status_code=status.HTTP_409_CONFLICT)
            else:
                return Response({
                    STATE: ERROR,
                    RESULTS: list(serializer.errors.values())[0][0],
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger().log(e, 'HIGH', module='USER', sub_module='USER')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)

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

    @is_token_validate
    #@role_required(USER, USER, EDIT)
    def get(self, request, id_string):
        try:
            user = get_user_by_id_string(id_string)
            if user:
                serializer = UserViewSerializer(instance=user, context={'request': request})
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
            logger().log(e, 'MEDIUM', module='USER', sub_module='USER')
            return Response({
                STATE: EXCEPTION,
                RESULTS: str(e),
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @is_token_validate
    #@role_required(USER, USER, EDIT)
    def put(self, request, id_string):
        try:
            user_obj = get_user_by_id_string(id_string)
            if user_obj:
                serializer = UserSerializer(data=request.data)
                if serializer.is_valid(raise_exception=False):
                    user_id_string = get_user_from_token(request.headers['token'])
                    user = get_user_by_id_string(user_id_string)
                    user_obj = serializer.update(user_obj, serializer.validated_data, user)
                    view_serializer = UserViewSerializer(instance=user_obj, context={'request': request})
                    return Response({
                        STATE: SUCCESS,
                        RESULTS: view_serializer.data,
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        STATE: ERROR,
                        RESULTS: list(serializer.errors.values())[0][0],
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                raise CustomAPIException(ID_STRING_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'HIGH', module='Admin', sub_module='User')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)


# API Header
# API end Point: api/v1/available-resource/list
# API verb: GET
# Package: Basic
# Modules: User
# Sub Module: User
# Interaction: View resource list
# Usage: Used for user list. Get all the records in pagination mode. It also have input params to filter/ search and
# sort in addition to pagination.
# Tables used: 2.5.3. User Details
# Author: Priyanka
# Created on: 18/01/2021


class ResourceList(generics.ListAPIView):
    try:
        serializer_class = UserSkillViewSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('tenant__id_string',)
        ordering_fields = ('tenant__id_string',)
        search_fields = ('tenant__id_string',)

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    utility = get_utility_by_id_string(self.kwargs['utility_id_string'])
                    appointment_obj = get_service_appointment_by_id_string(self.kwargs['appointment_id_string'])

                    skill_id_list = []
                    user_list = []
                    user_skill_list = []
                    uesr_leaves_list = []

                    if appointment_obj:
                        work_order_obj = get_work_order_master_by_id(appointment_obj.work_order_master_id)
                        for skill_obj in work_order_obj.json_obj['skill_details']:
                            skill_id = get_skill_by_id_string(skill_obj['id_string'])
                            skill_id_list.append(skill_id.id)

                    user_utility_objs = UserUtility.objects.filter(utility=utility, is_active=True)
                    if user_utility_objs:
                        for user_utility_obj in user_utility_objs:
                            user_obj = UserTbl.objects.filter(id=user_utility_obj.user_id, form_factor_id=2,
                                                              is_active=True).last()
                            if user_obj:
                                user_list.append(user_obj)

                        user_skills = UserSkill.objects.filter(user_id__in=[user.id for user in user_list],
                                                               skill_id__in=skill_id_list, is_active=True).distinct(
                            'user_id')
                        for user_skill in user_skills:
                            user_skill_list.append(user_skill.user_id)

                        user_leaves_obj = UserLeaves.objects.filter(user_id__in=user_skill_list,
                                                                    date__date=appointment_obj.sa_date.date())
                        for user_leaves in user_leaves_obj:
                            uesr_leaves_list.append(user_leaves.user_id)

                        queryset = user_skills.filter().exclude(user_id__in=uesr_leaves_list)

                        return queryset
                    else:
                        raise CustomAPIException("User Utility not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        print('=========>',e)
        logger().log(e, 'MEDIUM', module='Admin', sub_module='Utility')


# API Header
# API end Point: api/v1/bulk-assign/resource/list
# API verb: POST
# Package: Basic
# Modules: User
# Sub Module: User
# Interaction: Add users
# Usage: Get User
# Tables used: User 
# Author: Priyanka
# Created on: 05/02/2020

class BulkAssignResourceList(generics.ListAPIView):
    try:
        serializer_class = UserSkillViewSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('tenant__id_string',)
        ordering_fields = ('tenant__id_string',)
        search_fields = ('tenant__id_string',)

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    utility = get_utility_by_id_string(self.kwargs['utility_id_string'])
                    a = self.request.query_params.get('selectedRow')
                    a = a.split(',')

                    appointment_obj = ServiceAppointment.objects.filter(id_string__in=a)
                    workOrderList = []
                    skill_id_list = []
                    user_list = []
                    user_skill_list = []
                    uesr_leaves_list = []
                    appointment_date = []
                    for a in appointment_obj:
                        appointment_date.append((a.sa_date).date())
                        workOrderList.append(get_work_order_master_by_id(a.work_order_master_id))

                    for work_order in workOrderList:
                        for skill_obj in work_order.json_obj['skill_details']:
                            skill_id = get_skill_by_id_string(skill_obj['id_string'])
                            skill_id_list.append(skill_id.id)

                    user_utility_objs = UserUtility.objects.filter(utility=utility, is_active=True)

                    if user_utility_objs:
                        for user_utility_obj in user_utility_objs:
                            user_obj = UserTbl.objects.filter(id=user_utility_obj.user_id, form_factor_id=2,
                                                              is_active=True).last()
                            if user_obj:
                                user_list.append(user_obj)

                        user_skills = UserSkill.objects.filter(user_id__in=[user.id for user in user_list],
                                                               skill_id__in=skill_id_list, is_active=True).distinct(
                            'user_id')
                        for user_skill in user_skills:
                            user_skill_list.append(user_skill.user_id)

                        user_leaves_obj = UserLeaves.objects.filter(user_id__in=user_skill_list,
                                                                    date__date__in=appointment_date)
                        for user_leaves in user_leaves_obj:
                            uesr_leaves_list.append(user_leaves.user_id)

                        queryset = user_skills.filter().exclude(user_id__in=uesr_leaves_list)

                        return queryset
                    else:
                        raise CustomAPIException("User Utility not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Admin', sub_module='Utility')








# API Header
# API end Point: api/v1/user/:id_string/note
# API verb: POST
# Package: Basic
# Modules: S&M
# Sub Module: User
# Interaction: Add User note
# Usage: Add
# Tables used: Note
# Author: Priyanka
# Created on: 06/02/2021
class UserNote(GenericAPIView):

    @is_token_validate
    # #role_required(S&M, S_AND_M_USER, EDIT)
    def post(self, request, user_id_string, utility_id_string):
        try:
            id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(id_string)
            user_obj = get_user_by_id_string(user_id_string)
            utility_obj = get_utility_by_id_string(utility_id_string)
            module = get_module_by_key("USER")
            sub_module = get_sub_module_by_key("USER")
            serializer = NoteSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                note_obj = serializer.create(serializer.validated_data, user)
                note_obj.identification_id = user_obj.id
                note_obj.tenant = user_obj.tenant
                note_obj.utility = utility_obj
                note_obj.module_id = module
                note_obj.sub_module_id = sub_module
                note_obj.save()
                view_serializer = NoteViewSerializer(instance=note_obj, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULT: view_serializer.data,
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: list(serializer.errors.values())[0][0],
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger().log(e, 'HIGH', module='Consumer Ops', sub_module='Consumer')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)


# API Header
# API end Point: api/v1/utility/note/:id_string
# API verb: GET,PUT
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: City corresponding to the id
# Usage: API will fetch and update Cities for a given id
# Tables used: City
# Author: Chinmay
# Created on: 10/11/2020


class UserNoteDetail(GenericAPIView):
    @is_token_validate
    @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def put(self, request, id_string, utility_id_string):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            user_note_obj = get_note_by_id_string(id_string)
            utility_obj = get_utility_by_id_string(utility_id_string)
            module = get_module_by_key("USER")
            sub_module = get_sub_module_by_key("USER")
            if user_note_obj:
                serializer = NoteSerializer(data=request.data)
                if serializer.is_valid(raise_exception=False):
                    user_note_obj = serializer.update(user_note_obj, serializer.validated_data, user)
                    user_note_obj.identification_id = user.id
                    user_note_obj.tenant = user.tenant
                    user_note_obj.utility = utility_obj
                    user_note_obj.module_id = module
                    user_note_obj.sub_module_id = sub_module
                    user_note_obj.save()
                    view_serializer = NoteViewSerializer(instance=user_note_obj,
                                                         context={'request': request})
                    return Response({
                        STATE: SUCCESS,
                        RESULTS: view_serializer.data,
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        STATE: ERROR,
                        RESULTS: list(serializer.errors.values())[0][0],
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'HIGH', module='Admin', sub_module='Utility')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULTS: str(e),
            }, status=res.status_code)


class UserNoteDetailList(GenericAPIView):
    @is_token_validate
    # @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def get(self, request, id_string):
        try:
            user_note = get_note_by_id_string(id_string)
            if user_note:
                serializer = NoteViewSerializer(instance=user_note, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULTS: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'MEDIUM', module='Admin', sub_module='Utility')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULTS: str(e),
            }, status=res.status_code)


# API Header
# API end Point: api/v1/user/:id_string/note/list
# API verb: POST
# Package: Basic
# Modules: S&M
# Sub Module: User
# Interaction: Add User note
# Usage: Add
# Tables used: Note
# Author: Priyanka
# Created on: 06/02/2021
class UserNoteList(generics.ListAPIView):
    try:
        serializer_class = NoteListSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('tenant__id_string',)
        ordering_fields = ('tenant',)
        search_fields = ('tenant__name',)

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    user = get_user_by_id_string(self.kwargs['id_string'])
                    queryset = Notes.objects.filter(is_active=True)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Notes not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='S&M', sub_module='User')


# API Header
# API end Point: api/v1/user/:id_string/life-cycles
# API verb: GET
# Package: Basic
# Modules: S&M, Consumer Care, Consumer Ops
# Sub Module: User
# Interaction: User lifecycles
# Usage: API will fetch required data for User lifecycles
# Tables used: LifeCycles
# Author: Priyanka
# Created on: 16/02/2021
class UserLifeCycleList(generics.ListAPIView):
    try:
        serializer_class = LifeCycleListSerializer

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    user_obj = get_user_by_id_string(self.kwargs['id_string'])
                    module = get_module_by_key("S&M")
                    sub_module = get_sub_module_by_key("S_AND_M_USER")
                    queryset = LifeCycle.objects.filter(object_id=user_obj.id, module_id=module,
                                                        sub_module_id=sub_module, is_active=True)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Lifecycles not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='S&M', sub_module='User')


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            email = request.data['email']
            if is_email_exists(request.data['email']):
                user = get_user_by_email(email)
                uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
                token = PasswordResetTokenGenerator().make_token(user)
                absurl = 'http://localhost:4200/reset-password/' + uidb64 + '/' + token
                # current_site=get_current_site(request=request).domain
                # relativeLink=reverse('password-reset-complete',kwargs={'uidb64':uidb64, 'token':token})
                # absurl='http://'+current_site+ relativeLink
                email_body = 'Hello, \n Use link below to reset your password \n' + absurl
                # data = {'email_body':email_body, 'to_email':user.email, 'email_subject':'Reset your password'}
                send_mail('Reset Your Password', email_body, 'chinmay.pathak@bynry.com', [user.email],
                          fail_silently=False)
                # try:
                #     send_mail('Subject here', 'Here is the message.', 'gaurav.satpute@bynry.com', ['satputegaurav18@gmail.com'],fail_silently=False)
                # except Exception as e:
                #     print(e)
                # Util.send_email(data)
                return Response({
                    STATE: SUCCESS,
                    RESULTS: 'we have sent you a link to reset password',
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: FAIL,
                    RESULTS: 'You entered wrong email address',
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'HIGH', module='Admin', sub_module='User')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request, uidb64, token):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)


# class ChangePasswordView(UpdateAPIView):
#     serializer_class = ChangePasswordSerializer
#     model = User
#     # permission_classes = (IsAuthenticated,)
#
#     def get_object(self, queryset=None):
#         obj = self.request.user
#         print("OBJ",obj)
#         return obj
#
#     def update(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         serializer = self.get_serializer(data=request.data)
#
#         if serializer.is_valid():
#             # Check old password
#             if not self.object.check_password(serializer.data.get("old_password")):
#                 return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
#             # set_password
#             self.object.set_password(serializer.data.get("new_password"))
#             self.object.save()
#             response = {
#                 'status': 'success',
#                 'code': status.HTTP_200_OK,
#                 'message': 'Password updated successfully',
#                 'data': []
#             }
#
#             return Response(response)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(generics.UpdateAPIView):

    @is_token_validate
    @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def put(self, request, id_string):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            if user:
                serializer = ChangePasswordSerializer(data=request.data)
                if serializer.is_valid(raise_exception=False):
                    print(serializer.validated_data['password'])
                    user_obj = serializer.update(user, serializer.validated_data, user)
                    return Response({
                        STATE: SUCCESS,
                        # RESULTS: view_serializer.data,
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        STATE: ERROR,
                        RESULTS: list(serializer.errors.values())[0][0],
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'HIGH', module='Admin', sub_module='Utility')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULTS: str(e),
            }, status=res.status_code)
