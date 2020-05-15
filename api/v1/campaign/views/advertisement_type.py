from rest_framework import generics, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from api.messages import SUCCESS, STATE, DATA, EXCEPTION
from v1.campaign.serializers.advertisement_type import AdvertisementListSerializer,AdvertisementViewSerializer
from v1.campaign.models.advertisement_type import AdvertisementType,get_advert_type_by_id_string
from v1.commonapp.views.pagination import StandardResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from v1.commonapp.views.logger import logger

# 'advert-type/list'
class AdvertisementTypeList(generics.ListAPIView):
    serializer_class = AdvertisementListSerializer
    pagination_class = StandardResultsSetPagination

    queryset = AdvertisementType.objects.filter(tenant=1, utility=1)
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_fields = ('name', 'tenant__id_string',)
    ordering_fields = ('name', 'tenant',)
    ordering = ('name',)  # always give by default alphabetical order
    search_fields = ('name', 'tenant__name',)



class AdvertisementTypeDetail(GenericAPIView):
    def get(self,request,id_string):
        try:
            advet_type = get_advert_type_by_id_string(id_string)
            if advet_type:
                serializer = AdvertisementViewSerializer(instance=advet_type,context={"request":request})
                return Response({
                    STATE: SUCCESS,
                    DATA: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: EXCEPTION,
                    DATA: '',
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            logger().log(e, 'ERROR', user='test', name='test')
            return Response({
                STATE: EXCEPTION,
                DATA: '',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)