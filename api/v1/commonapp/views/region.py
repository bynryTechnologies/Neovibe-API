
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULTS
from rest_framework import status, generics
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from api.messages import *
from master.models import get_user_by_id_string
from v1.billing.serializers.invoice_bill import *
from v1.commonapp.common_functions import is_authorized, is_token_valid, get_user_from_token
from v1.commonapp.views.custom_exception import CustomAPIException, InvalidAuthorizationException, InvalidTokenException
from v1.commonapp.views.logger import logger
from v1.complaint.models.complaint import *
from v1.complaint.serializers.complaint import *
from v1.consumer.serializers.consumer_scheme_master import *
from v1.payment.serializer.payment import *
from v1.userapp.decorators import is_token_validate, role_required
from v1.commonapp.serializers.region import RegionSerializer, RegionViewSerializer, RegionListSerializer
from v1.commonapp.models.region import Region as RegionModel
from v1.commonapp.models.region import get_region_by_id_string
from api.messages import *
from api.constants import *

# API Header
# API end Point: api/v1/:id_string/region/list
# API verb: GET
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: regions list
# Usage: API will fetch all region list
# Tables used: Region
# Author: Chinmay
# Created on: 09/11/2020


class RegionList(generics.ListAPIView):
    try:
        serializer_class = RegionListSerializer

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    queryset = RegionModel.objects.all()
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException(REGION_NOT_FOUND, status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Admin', sub_module='Admin')


# API Header
# API end Point: api/v1/region
# API verb: POST
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Region Post
# Usage: API will POST region into database
# Tables used: Region
# Author: Chinmay
# Created on: 09/11/2020
class Region(GenericAPIView):

    @is_token_validate
    @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def post(self, request):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            serializer = RegionSerializer(data=request.data)
            if serializer.is_valid(raise_exception=False):
                region_obj = serializer.create(serializer.validated_data, user)
                view_serializer = RegionViewSerializer(instance=region_obj, context={'request': request})
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
# API end Point: api/v1/:id_string/region
# API verb: GET,PUT
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: regions corresponding to the id
# Usage: API will fetch and update region for a given id
# Tables used: Region
# Author: Chinmay
# Created on: 09/11/2020


class RegionDetail(GenericAPIView):

    @is_token_validate
    @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def get(self, request, id_string):
        try:
            region = get_region_by_id_string(id_string)
            if region:
                serializer = RegionViewSerializer(instance=region, context={'request': request})
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
            region_obj = get_region_by_id_string(id_string)
            if "name" not in request.data:
                request.data['name'] = region_obj.name
            if region_obj:
                serializer = RegionSerializer(data=request.data)
                if serializer.is_valid(raise_exception=False):
                    region_obj = serializer.update(region_obj, serializer.validated_data, user)
                    view_serializer = RegionViewSerializer(instance=region_obj,
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

