from rest_framework import generics, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULTS
from v1.commonapp.models.sub_area import SubArea as SubAreaModel, get_sub_area_by_id_string
from v1.commonapp.serializers.sub_area import SubAreaListSerializer, SubAreaViewSerializer, SubAreaSerializer
from v1.commonapp.views.custom_exception import CustomAPIException, InvalidAuthorizationException, InvalidTokenException
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.utility.models.utility_master import get_utility_by_id_string
from api.messages import *
from api.constants import *
from master.models import get_user_by_id_string
from v1.userapp.decorators import is_token_validate, role_required
from v1.commonapp.common_functions import is_token_valid, is_authorized, get_user_from_token
from v1.commonapp.models.area import get_area_by_id_string
from v1.commonapp.models.sub_area import get_sub_area_by_id_string
from django.db import transaction


# API Header
# API end Point: api/v1/utility/:id_string/subarea/list
# API verb: GET
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: SubArea list
# Usage: API will fetch all SubArea list
# Tables used: SubArea
# Author: Chinmay
# Created on: 11/11/2020
class SubAreaList(generics.ListAPIView):
    try:
        serializer_class = SubAreaListSerializer
        pagination_class = StandardResultsSetPagination

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    utility = get_utility_by_id_string(self.kwargs['id_string'])
                    queryset = SubAreaModel.objects.filter(utility=utility, is_active=True)
                    if 'area_id' in self.request.query_params:
                        area = get_area_by_id_string(self.request.query_params['area_id'])
                        queryset = queryset.filter(area_id=area.id)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException(SUBAREA_NOT_FOUND, status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Admin', sub_module='Utility')


class SubAreaListByArea(generics.ListAPIView):
    try:
        serializer_class = SubAreaListSerializer
        pagination_class = StandardResultsSetPagination

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    area = get_area_by_id_string(self.kwargs['id_string'])
                    queryset = SubAreaModel.objects.filter(area_id=area.id, is_active=True)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException(SUBAREA_NOT_FOUND, status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Admin', sub_module='Utility')


# API Header
# API end Point: api/v1/utility/area
# API verb: POST
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: SubArea post
# Usage: API will Post the Subarea
# Tables used: SubArea
# Author: Chinmay
# Created on: 10/11/2020
class SubArea(GenericAPIView):

    @is_token_validate
    @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def post(self, request):
        try:
            with transaction.atomic():
                user_id_string = get_user_from_token(request.headers['Authorization'])
                user = get_user_by_id_string(user_id_string)
                serializer = SubAreaSerializer(data=request.data)
                if serializer.is_valid(raise_exception=False):
                    subarea_obj = serializer.create(serializer.validated_data, user)
                    view_serializer = SubAreaViewSerializer(instance=subarea_obj, context={'request': request})
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
# API end Point: api/v1/utility/subarea/:id_string
# API verb: GET,PUT
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: SubArea corresponding to the id
# Usage: API will fetch and update SubAreas for a given id
# Tables used: SubArea
# Author: Chinmay
# Created on: 10/11/2020


class SubAreaDetail(GenericAPIView):

    @is_token_validate
    @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def get(self, request, id_string):
        try:
            subarea = get_sub_area_by_id_string(id_string)
            if subarea:
                serializer = SubAreaViewSerializer(instance=subarea, context={'request': request})
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
            subarea_obj = get_sub_area_by_id_string(id_string)
            if "name" not in request.data:
                request.data['name'] = subarea_obj.name
            if subarea_obj:
                serializer = SubAreaSerializer(data=request.data)
                if serializer.is_valid(raise_exception=False):
                    subarea_obj = serializer.update(subarea_obj, serializer.validated_data, user)
                    view_serializer = SubAreaViewSerializer(instance=subarea_obj,
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
