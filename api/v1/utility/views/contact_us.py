# Tables used: Contact Us
# Author: Rohan
# Created on: 6/1/2021
from rest_framework import generics, status
from v1.commonapp.common_functions import is_token_valid, is_authorized, get_user_from_token
from v1.commonapp.views.custom_exception import CustomAPIException, InvalidAuthorizationException, InvalidTokenException
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.utility.models.contact_us import ContactUs as ContactUsModel, get_contact_us_by_id_string
from v1.utility.models.utility_master import get_utility_by_id_string
from v1.utility.serializers.contact_us import ContactUsListSerializer, ContactUsSerializer, ContactUsViewSerializer
from api.constants import *
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from v1.userapp.decorators import is_token_validate, role_required
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULTS
from api.messages import *
from master.models import get_user_by_id_string


class ContactUsList(generics.ListAPIView):
    try:
        serializer_class = ContactUsListSerializer
        pagination_class = StandardResultsSetPagination

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    utility = get_utility_by_id_string(self.kwargs['id_string'])
                    queryset = ContactUsModel.objects.filter(utility=utility, is_active=True)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Contact us details Not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Admin', sub_module='Admin')


# API Header
# API end Point: api/v1/utility/contact_us
# API verb: POST
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Area post
# Usage: API will Post the contact_us
# Tables used: Area
# Author: Chinmay
# Created on: 10/11/2020
class ContactUs(GenericAPIView):

    @is_token_validate
    @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def post(self, request):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            serializer = ContactUsSerializer(data=request.data)
            if serializer.is_valid(raise_exception=False):

                contact_us_obj = serializer.create(serializer.validated_data, user)
                view_serializer = ContactUsViewSerializer(instance=contact_us_obj, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULTS: view_serializer.data,
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    STATE: ERROR,
                    RESULTS: list(serializer.errors.values())[0][0],
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger().log(e, 'HIGH', module='Admin', sub_module='Utility')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULTS: str(e),
            }, status=res.status_code)


# API Header
# API end Point: api/v1/utility/contact-us/:id_string
# API verb: GET,PUT
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: ContactUS corresponding to the id
# Usage: API will fetch and update Contact US Details for a given id
# Tables used: ContactUs
# Author: Chinmay
# Created on: 17/03/2021


class ContactUsDetail(GenericAPIView):

    @is_token_validate
    @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def get(self, request, id_string):
        try:
            contact_us = get_contact_us_by_id_string(id_string)
            if contact_us:
                serializer = ContactUsViewSerializer(instance=contact_us, context={'request': request})
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

    @is_token_validate
    @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def put(self, request, id_string):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            contact_us_obj = get_contact_us_by_id_string(id_string)
            if "email" not in request.data:
                request.data['email'] = contact_us_obj.email
            if contact_us_obj:
                serializer = ContactUsSerializer(data=request.data)
                if serializer.is_valid(raise_exception=False):
                    contact_us_obj = serializer.update(contact_us_obj, serializer.validated_data, user)
                    view_serializer = ContactUsViewSerializer(instance=contact_us_obj,
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
