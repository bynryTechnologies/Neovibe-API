import traceback
import logging
from rest_framework.exceptions import APIException

from master.models import User
from v1.commonapp.views.custom_exception import InvalidTokenException, InvalidAuthorizationException
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import generics, status
from v1.commonapp.views.logger import logger
from v1.campaign.models.campaign import get_campaign_by_id_string,Campaign as Campaigntbl
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.campaign.models.campaign import Campaign as CampaignTbl
from v1.campaign.serializers.campaign import CampaignViewSerializer,CampaignListSerializer,CampaignSerializer
from v1.commonapp.common_functions import is_token_valid, get_payload, is_authorized
from v1.campaign.views.common_functions import is_data_verified,set_validated_data
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, DATA, RESULTS,DUPLICATE,DATA_ALREADY_EXISTS

# API Header
# API end Point: api/v1/campaign/list
# API verb: GET
# Package: Basic
# Modules: S&M
# Sub Module: Campaign
# Interaction: Campaign List
# Usage: API will fetch required data for Campaign list
# Tables used: 2.3.6 Campaign Master
# Author: Priyanka Kachare
# Created on: 22/04/2020

# Api for getting campaign  filter

class CampaignList(generics.ListAPIView):
    try:
        serializer_class = CampaignListSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('name', 'tenant__id_string','start_date',)
        ordering_fields = ('name',)
        ordering = ('created_date',)  # always give by default alphabetical order
        search_fields = ('name',)

        def get_queryset(self):
            if is_token_valid(0):
                if is_authorized():
                    queryset = CampaignTbl.objects.filter(is_active=True)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException

    except Exception as ex:
        logger().log(ex, 'ERROR')
        raise APIException


# API Header
# API end Point: api/v1/campaign
# API verb: POST
# Package: Basic
# Modules: S&M
# Sub Module: Campaign
# Interaction: Add Campaign
# Usage: Add
# Tables used:  2.3.6 Campaign Master
# Auther: Priyanka
# Created on: 15/05/2020

class Campaign(GenericAPIView):

    def post(self, request):
        try:
            if is_token_valid(1):
                if is_authorized():
                    user = User.objects.get(id=5)
                    if is_data_verified(request):
                        serializer = CampaignSerializer(data=request.data)
                        if serializer.is_valid():
                            campaign_obj = serializer.create(serializer.validated_data, user)
                            if campaign_obj:
                                view_serializer = CampaignViewSerializer(instance=campaign_obj,context={'request': request})
                                return Response({
                                    STATE: SUCCESS,
                                    RESULTS: view_serializer.data,
                                }, status=status.HTTP_201_CREATED)
                            else:
                                return Response({
                                    STATE: DUPLICATE,
                                    RESULTS: DATA_ALREADY_EXISTS,
                                }, status=status.HTTP_409_CONFLICT)
                        else:
                            return Response({
                                STATE: ERROR,
                                RESULTS: serializer.errors,
                            }, status=status.HTTP_400_BAD_REQUEST)
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


# API Header
# API end Point: api/v1/campaign/:id_string
# API verb: GET,PUT
# Package: Basic
# Modules: S&M
# Sub Module: Campaign
# Interaction: View  and Update Campaign
# Usage: View,Update
# Tables used:  2.3.6 Campaign Master
# Auther: Priyanka
# Created on: 23/04/2020

# API for add, edit, view campaign details
class CampaignDetail(GenericAPIView):

    def get(self, request, id_string):
        try:
            if is_token_valid(1):
                if is_authorized():
                    campaign = get_campaign_by_id_string(id_string)
                    if campaign:
                        serializer = CampaignViewSerializer(instance=campaign, context={'request': request})
                        return Response({
                            STATE: SUCCESS,
                            DATA: serializer.data,
                        }, status=status.HTTP_200_OK)
                    else:
                        return Response({
                            STATE: EXCEPTION,
                            DATA: '',
                        }, status=status.HTTP_204_NO_CONTENT)
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
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def put(self, request, id_string):
        try:
            if is_token_valid(1):
                if is_authorized():
                    user = User.objects.get(id=2)
                    campaign_obj = get_campaign_by_id_string(id_string)
                    if campaign_obj:
                        serializer = CampaignSerializer(data=request.data)
                        if serializer.is_valid():
                            campaign_obj = serializer.update(campaign_obj, serializer.validated_data, user)
                            view_serializer = CampaignViewSerializer(instance=campaign_obj,context={'request': request})
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
                        }, status=status.HTTP_204_NO_CONTENT)
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



