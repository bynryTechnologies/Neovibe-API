__author__ = "aki"

import traceback
from rest_framework.exceptions import APIException
from rest_framework.generics import GenericAPIView
from rest_framework import generics, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, DUPLICATE, RESULT, DATA_ALREADY_EXISTS
from master.models import User
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.views.custom_exception import InvalidAuthorizationException, InvalidTokenException, \
    ObjectNotFoundException
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.contract.models.contract import get_contract_by_id_string
from v1.contract.serializers.contract_demand import ContractDemandViewSerializer, ContractDemandSerializer
from v1.contract.models.contract_demand import ContractDemand as ContractDemandTbl, get_contract_demand_by_id_string


# API Header
# API end Point: api/v1/contract/id_string/demand/list
# API verb: GET
# Package: Basic
# Modules: Contract
# Sub Module: Demand
# Interaction: Get contract demand list
# Usage: API will fetch required data for contract demand list.
# Tables used: Contract Demand
# Author: Akshay
# Created on: 29/05/2020


class ContractDemandList(generics.ListAPIView):
    try:
        serializer_class = ContractDemandViewSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('tenant__id_string', 'utility__id_string')
        ordering_fields = ('tenant__name', 'utility__name')
        ordering = ('tenant__name',)  # always give by default alphabetical order
        search_fields = ('tenant__name', 'utility__name',)

        def get_queryset(self):
            if is_token_valid(self.request.headers['token']):
                if is_authorized():
                    contract_obj = get_contract_by_id_string(self.kwargs['id_string'])
                    if contract_obj:
                        queryset = ContractDemandTbl.objects.filter(contract=contract_obj.id, is_active=True)
                        return queryset
                    else:
                        raise ObjectNotFoundException
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'ERROR')
        raise APIException


# API Header
# API end Point: api/v1/contract/id_string/demand
# API verb: POST
# Package: Basic
# Modules: Contract
# Sub Module: Demand
# Interaction: Create contract demand
# Usage: API will create contract demand object based on valid data
# Tables used: Contract Demand
# Author: Akshay
# Created on: 29/05/2020

class ContractDemand(GenericAPIView):
    serializer_class = ContractDemandSerializer

    def post(self, request, id_string):
        try:
            # Checking authentication start
            if is_token_valid(request.headers['token']):
                # payload = get_payload(request.headers['token'])
                # user = get_user(payload['id_string'])
                # Checking authentication end

                # Checking authorization start
                if is_authorized():
                # Checking authorization end
                    # Todo fetch user from request start
                    user = User.objects.get(id=2)
                    # Todo fetch user from request end
                    contract_obj = get_contract_by_id_string(id_string)
                    if contract_obj:
                        serializer = ContractDemandSerializer(data=request.data)
                        if serializer.is_valid():
                            contract_demand_obj = serializer.create(serializer.validated_data, contract_obj, user)
                            if contract_demand_obj:
                                serializer = ContractDemandViewSerializer(contract_demand_obj, context={'request': request})
                                return Response({
                                    STATE: SUCCESS,
                                    RESULT: serializer.data,
                                }, status=status.HTTP_201_CREATED)
                            else:
                                return Response({
                                    STATE: DUPLICATE,
                                    RESULT: DATA_ALREADY_EXISTS,
                                }, status=status.HTTP_409_CONFLICT)
                        else:
                            return Response({
                                STATE: ERROR,
                                RESULT: serializer.errors,
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
        except Exception as ex:
            logger().log(ex, 'ERROR', user=request.user, name=request.user.username)
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(ex))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# API Header
# API end Point: api/v1/contract/demand/id_string
# API verb: GET, PUT
# Package: Basic
# Modules: Contract
# Sub Module: Demand
# Interaction: For edit and get single contract demand
# Usage: API will edit and get contract demand
# Tables used: Contract Demand
# Author: Akshay
# Created on: 29/05/2020

class ContractDemandDetail(GenericAPIView):
    serializer_class = ContractDemandSerializer

    def get(self, request, id_string):
        try:
            # Checking authentication start
            if is_token_valid(request.headers['token']):
                # payload = get_payload(request.headers['token'])
                # user = get_user(payload['id_string'])
                # Checking authentication end

                # Checking authorization start
                if is_authorized():
                # Checking authorization end

                    contract_demand_obj = get_contract_demand_by_id_string(id_string)
                    if contract_demand_obj:
                        serializer = ContractDemandViewSerializer(contract_demand_obj, context={'request': request})
                        return Response({
                            STATE: SUCCESS,
                            RESULT: serializer.data,
                        }, status=status.HTTP_200_OK)
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
        except Exception as ex:
            logger().log(ex, 'ERROR', user=request.user, name=request.user.username)
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(ex))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, id_string):
        try:
            # Checking authentication start
            if is_token_valid(request.headers['token']):
                # payload = get_payload(request.headers['token'])
                # user = get_user(payload['id_string'])
                # Checking authentication end

                # Checking authorization start
                if is_authorized():
                # Checking authorization end
                    # Todo fetch user from request start
                    user = User.objects.get(id=2)
                    # Todo fetch user from request end

                    contract_demand_obj = get_contract_demand_by_id_string(id_string)
                    if contract_demand_obj:
                        serializer = ContractDemandSerializer(data=request.data)
                        if serializer.is_valid():
                            contract_demand_obj = serializer.update(contract_demand_obj, serializer.validated_data, user)
                            serializer = ContractDemandViewSerializer(contract_demand_obj, context={'request': request})
                            return Response({
                                STATE: SUCCESS,
                                RESULT: serializer.data,
                            }, status=status.HTTP_200_OK)
                        else:
                            return Response({
                                STATE: ERROR,
                                RESULT: serializer.errors,
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
        except Exception as ex:
            logger().log(ex, 'ERROR', user=request.user, name=request.user.username)
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(ex))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)