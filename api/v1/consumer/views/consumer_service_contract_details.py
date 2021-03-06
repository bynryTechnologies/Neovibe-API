from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.exceptions import APIException
from rest_framework.filters import OrderingFilter, SearchFilter
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.views.custom_exception import CustomAPIException, InvalidAuthorizationException, InvalidTokenException
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.consumer.models.consumer_master import get_consumer_by_id_string
from v1.consumer.models.consumer_service_contract_details import ConsumerServiceContractDetail, get_consumer_service_contract_detail_by_id_string, CONSUMER_DICT
from v1.consumer.serializers.consumer_service_contract_details import ConsumerServiceContractDetailViewSerializer
from v1.meter_data_management.models.meter import get_meter_by_id_string
from v1.utility.models.utility_master import get_utility_by_id_string
from v1.commonapp.views.custom_filter_backend import CustomFilter
from v1.utility.models.utility_service_contract_master import get_utility_service_contract_master_by_id
from v1.utility.models.utility_product import get_utility_product_by_id
from v1.commonapp.models.work_order_type import get_work_order_type_by_key
from v1.commonapp.models.work_order_sub_type import get_work_order_sub_type_by_key
from v1.utility.models.utility_work_order_type import get_utility_work_order_type_by_id
from v1.utility.models.utility_work_order_sub_type import get_utility_work_order_sub_type_by_id
from v1.work_order.models.work_order_master import get_work_order_master_by_id, WorkOrderMaster
from v1.work_order.serializers.service_appointment import ServiceAppointmentSerializer
from v1.work_order.views.common_functions import generate_service_appointment_no
from v1.userapp.decorators import is_token_validate, role_required
from v1.commonapp.common_functions import is_authorized, is_token_valid, get_user_from_token
from rest_framework.generics import GenericAPIView
from api.constants import *
from api.messages import *
from master.models import get_user_by_id_string
from rest_framework.response import Response
from v1.utility.models.utility_work_order_type import UtilityWorkOrderType
from v1.utility.models.utility_work_order_sub_type import UtilityWorkOrderSubType
from django.db import transaction
from v1.meter_data_management.models.meter import get_meter_by_id_string

class ConsumerServiceContractDetailList(generics.ListAPIView):
    try:
        serializer_class = ConsumerServiceContractDetailViewSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('tenant__id_string',)
        ordering_fields = ('tenant',)
        search_fields = ('tenant__name',)

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    utility = get_utility_by_id_string(self.kwargs['id_string'])
                    queryset = ConsumerServiceContractDetail.objects.filter(utility=utility, is_active=True)
                    queryset = CustomFilter.get_filtered_queryset(queryset, self.request)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Consumer service contracts not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Consumer ops', sub_module='consumer')

# Note: rohan below is updated api for fetch service contract detail list you just delete above code give class name to below api and delete url


# API Header
# API end Point: api/v1/service-contract-detail/list
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: consumer service contract detail list
# Usage: API will fetch required data for consumer service contract detail list against filter and search
# Tables used: ConsumerServiceContractDetail
# Author: Akshay
# Created on: 19/02/2021

class ConsumerMeterList(generics.ListAPIView):
    try:
        serializer_class = ConsumerServiceContractDetailViewSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('utility__id_string', 'consumer_id', 'meter_id')
        ordering_fields = ('utility__id_string',)
        ordering = ('utility__id_string',)  # always give by default alphabetical order
        search_fields = ('utility__name',)

        def get_queryset(self):
            token, user_obj = is_token_valid(self.request.headers['Authorization'])
            if token:
                if is_authorized(1, 1, 1, user_obj):
                    self.request.query_params._mutable = True
                    if 'consumer_id' in self.request.query_params:
                        self.request.query_params['consumer_id'] = get_consumer_by_id_string\
                            (self.request.query_params['consumer_id']).id
                    if 'meter_id' in self.request.query_params:
                        self.request.query_params['meter_id'] = get_meter_by_id_string\
                            (self.request.query_params['meter_id']).id
                    self.request.query_params._mutable = False
                    queryset = ConsumerServiceContractDetail.objects.filter(is_active=True)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'LOW', module='CONSUMER OPS', sub_module='METER DATA')
        raise APIException


# API Header
# API end Point: api/v1/consumer/service-contract-detail
# API verb: POST
# Package: Basic
# Modules: S&M, Consumer Care, Consumer Ops
# Sub Module: Consumer
# Interaction: ConsumerServiceContractDetail
# Usage: ConsumerServiceContractDetail Approve
# Tables used: ConsumerServiceContractDetail
# Author: Gaurav
# Created on: 22-02-2021

# class ConsumerServiceContractDetailApprove(GenericAPIView):

#     @is_token_validate
#     # #role_required(CONSUMER_OPS, CONSUMER, EDIT)
#     def post(self, request):
#         try:
#             user_id_string = get_user_from_token(request.headers['Authorization'])
#             user = get_user_by_id_string(user_id_string)
#             print("=======request data===",request.data)
#             print("======yesorno=========",request.data['meter_status'])
#             consumer_service_contract_details_obj = get_consumer_service_contract_detail_by_id_string(request.data['consumer_service_contract_detail_id'])
#             if consumer_service_contract_details_obj:
#                 print("=====consumer id==",consumer_service_contract_details_obj.id)
#                 print("=====consumer contract id==",consumer_service_contract_details_obj.service_contract_id)
#                 service_contract_obj = get_utility_service_contract_master_by_id(consumer_service_contract_details_obj.service_contract_id)
#                 print("==============serv=======",service_contract_obj)
#                 if service_contract_obj:
#                     utility_product_obj=get_utility_product_by_id(service_contract_obj.utility_product_id)
#                     print("===========product========",utility_product_obj)

#                 work_order_type_obj = get_work_order_type_by_key('INSTALLATION')
#                 if work_order_type_obj:
#                     # utility_work_order_type_obj = get_utility_work_order_type_by_id(work_order_type_obj.id)
#                     utility_work_order_type_obj = UtilityWorkOrderType.objects.get(work_order_type_id=work_order_type_obj.id)
#                     print("========UWOT=======",utility_work_order_type_obj)

#                 work_order_sub_type_obj = get_work_order_sub_type_by_key('Meter Installation')
#                 if work_order_sub_type_obj:
#                     # utility_work_order_sub_type_obj = get_utility_work_order_sub_type_by_id(work_order_sub_type_obj.id)
#                     utility_work_order_sub_type_obj = UtilityWorkOrderSubType.objects.get(work_order_sub_type_id=work_order_sub_type_obj.id)
#                     print("========UWOST=======",utility_work_order_sub_type_obj)

#                 if utility_product_obj and utility_work_order_type_obj and utility_work_order_sub_type_obj:
#                     work_order_master_obj = WorkOrderMaster.objects.get(utility_work_order_sub_type_id=utility_work_order_sub_type_obj.id,utility_product_id=utility_product_obj.id)
#                     print("=====master======",work_order_master_obj)

#                     if work_order_master_obj:
#                         request.data['work_order_master_id']=str(work_order_master_obj.id_string)
#                         appointment_serializer = ServiceAppointmentSerializer(data=request.data)
#                         if appointment_serializer.is_valid(raise_exception=True):                           
#                             appointment_obj = appointment_serializer.create(appointment_serializer.validated_data, user)
#                             appointment_obj.utility = consumer_service_contract_details_obj.utility
#                             appointment_obj.consumer_service_contract_detail_id = consumer_service_contract_details_obj.id 
#                             appointment_obj.save()
#                             consumer_service_contract_details_obj.change_state(CONSUMER_DICT["APPROVED"])
#                             consumer_service_contract_details_obj.is_active = True
#                             consumer_service_contract_details_obj.save()                             
#                     view_serializer = ConsumerServiceContractDetailViewSerializer(instance=consumer_service_contract_details_obj, context={'request': request})
#                     return Response({
#                         STATE: SUCCESS,
#                         RESULT: view_serializer.data,
#                     }, status=status.HTTP_200_OK)
#         except Exception as e:
#             logger().log(e, 'HIGH', module='Consumer Ops', sub_module='Consumer')
#             res = self.handle_exception(e)
#             return Response({
#                 STATE: EXCEPTION,
#                 RESULT: str(e),
#             }, status=res.status_code)


class ConsumerServiceContractDetailApprove(GenericAPIView):
    
    @is_token_validate
    #role_required(WORK_ORDER, DISPATCHER, EDIT)
    def post(self, request):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            print("=======request data===",request.data)
            print("======yesorno=========",request.data['meter_status'])
            consumer_service_contract_details_obj = get_consumer_service_contract_detail_by_id_string(request.data['consumer_service_contract_detail_id'])
            appointment_serializer = ServiceAppointmentSerializer(data=request.data)
            if appointment_serializer.is_valid(raise_exception=False):
                with transaction.atomic():
                    if request.data['meter_status'] == "yes":
                        print("inside yesssssssss")
                        appointment_obj = appointment_serializer.create(appointment_serializer.validated_data, user)
                        appointment_obj.utility = consumer_service_contract_details_obj.utility
                        appointment_obj.consumer_service_contract_detail_id = consumer_service_contract_details_obj.id 
                        appointment_obj.save()
                        consumer_service_contract_details_obj.change_state(CONSUMER_DICT["APPROVED"])
                        consumer_service_contract_details_obj.is_active = True
                        consumer_service_contract_details_obj.save()
                        # # Timeline code start
                        # transaction.on_commit(
                        #     lambda: save_service_appointment_timeline.delay(appointment_obj, "Service Appointment", "Service Appointment Created", "NOT ASSIGNED",user))
                            # Timeline code end
                    elif request.data['meter_status'] == "no":
                        print("inside noooooooooo")
                        meter = get_meter_by_id_string(request.data['meter_id'])
                        print("========meter id string==========",meter)
                        print("======meteeerer id=======",meter.id)
                        appointment_obj = appointment_serializer.create(appointment_serializer.validated_data, user)
                        appointment_obj.utility = consumer_service_contract_details_obj.utility
                        appointment_obj.consumer_service_contract_detail_id = consumer_service_contract_details_obj.id 
                        appointment_obj.save()
                        consumer_service_contract_details_obj.change_state(CONSUMER_DICT["APPROVED"])
                        consumer_service_contract_details_obj.is_active = True
                        consumer_service_contract_details_obj.meter_id = meter.id
                        consumer_service_contract_details_obj.save()
                        # # Timeline code start
                        # transaction.on_commit(
                        #     lambda: save_service_appointment_timeline.delay(appointment_obj, "Service Appointment", "Service Appointment Created", "NOT ASSIGNED",user))
                            # Timeline code end

                    view_serializer = ConsumerServiceContractDetailViewSerializer(instance=consumer_service_contract_details_obj, context={'request': request})
                    return Response({
                        STATE: SUCCESS,
                        RESULTS: view_serializer.data,
                    }, status=status.HTTP_201_CREATED)                
            else:
                return Response({
                    STATE: ERROR,
                    RESULTS: list(appointment_serializer.errors.values())[0][0],
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("=======error=========",e)
            logger().log(e, 'HIGH', module = 'Admin', sub_module = 'User')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)


# API Header
# API end Point: api/v1/consumer/<uuid:id_string>/service-contract-detail
# API verb: POST
# Package: Basic
# Modules: S&M, Consumer Care, Consumer Ops
# Sub Module: Consumer
# Interaction: ConsumerServiceContractDetail
# Usage: ConsumerServiceContractDetail details
# Tables used: ConsumerServiceContractDetail
# Author: Gaurav
# Created on: 08-04-2021

class ConsumerServiceContractDetailDetails(GenericAPIView):

    @is_token_validate
    #role_required(CONSUMER_OPS, CONSUMER, VIEW)
    def get(self, request, id_string):
        try:
            consumer = get_consumer_service_contract_detail_by_id_string(id_string)
            if consumer:
                serializer = ConsumerServiceContractDetailViewSerializer(instance=consumer, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULT: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: CONSUMER_SERVICE_CONTRACT_DETAIL_NOT_FOUND,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'MEDIUM', module='Consumer Ops', Sub_module='Consumer')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)


# API Header
# API end Point: api/v1/consumer/<uuid:id_string>/service-contract-detail/reject
# API verb: POST
# Package: Basic
# Modules: S&M, Consumer Care, Consumer Ops
# Sub Module: Consumer
# Interaction: ConsumerServiceContractDetail
# Usage: ConsumerServiceContractDetail Reject
# Tables used: ConsumerServiceContractDetail
# Author: Gaurav
# Created on: 08-04-2021

class ConsumerServiceContractDetailReject(GenericAPIView):

    @is_token_validate
    #role_required(CONSUMER_OPS, COMPLAINT, EDIT)
    def put(self, request, id_string):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            consumer_contract = get_consumer_service_contract_detail_by_id_string(id_string)
            print("==========consumer========",consumer_contract)
            if consumer_contract:
                # serializer = ComplaintSerializer(data=request.data)
                # consumer_contract.change_state(CONSUMER_DICT["REJECTED"])
                # if serializer.is_valid(raise_exception=False):
                    # consumer_contract = serializer.update(consumer_contract, serializer.validated_data, user)
                    with transaction.atomic():
                        consumer_contract.change_state(CONSUMER_DICT["REJECTED"])
                        serializer = ConsumerServiceContractDetailViewSerializer(instance=consumer_contract, context={'request': request})
                        return Response({
                            STATE: SUCCESS,
                            RESULT: serializer.data,
                        }, status=status.HTTP_200_OK)
                # else:
                #     return Response({
                #         STATE: ERROR,
                #         RESULTS: list(serializer.errors.values())[0][0],
                #     }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: CONSUMER_SERVICE_CONTRACT_DETAIL_NOT_FOUND
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'HIGH', module='Consumer Ops', Sub_module='Consumer')
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=status.HTTP_412_PRECONDITION_FAILED)


# API Header
# API end Point: api/v1/consumer/<uuid:id_string>/service-contract-detail/hold
# API verb: POST
# Package: Basic
# Modules: S&M, Consumer Care, Consumer Ops
# Sub Module: Consumer
# Interaction: ConsumerServiceContractDetail
# Usage: ConsumerServiceContractDetail hold
# Tables used: ConsumerServiceContractDetail
# Author: Gaurav
# Created on: 08-04-2021

class ConsumerServiceContractDetailHold(GenericAPIView):

    @is_token_validate
    #role_required(CONSUMER_OPS, COMPLAINT, EDIT)
    def put(self, request, id_string):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            consumer_contract = get_consumer_service_contract_detail_by_id_string(id_string)
            print("==========consumer========",consumer_contract)
            if consumer_contract:
                # serializer = ComplaintSerializer(data=request.data)
                # consumer_contract.change_state(CONSUMER_DICT["REJECTED"])
                # if serializer.is_valid(raise_exception=False):
                    # consumer_contract = serializer.update(consumer_contract, serializer.validated_data, user)
                    with transaction.atomic():
                        consumer_contract.change_state(CONSUMER_DICT["HOLD"])
                        serializer = ConsumerServiceContractDetailViewSerializer(instance=consumer_contract, context={'request': request})
                        return Response({
                            STATE: SUCCESS,
                            RESULT: serializer.data,
                        }, status=status.HTTP_200_OK)
                # else:
                #     return Response({
                #         STATE: ERROR,
                #         RESULTS: list(serializer.errors.values())[0][0],
                #     }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: CONSUMER_SERVICE_CONTRACT_DETAIL_NOT_FOUND
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'HIGH', module='Consumer Ops', Sub_module='Consumer')
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=status.HTTP_412_PRECONDITION_FAILED)