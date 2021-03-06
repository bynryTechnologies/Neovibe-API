
from rest_framework import status, generics
from api.messages import *
from v1.commonapp.common_functions import is_authorized, is_token_valid, get_user_from_token
from v1.commonapp.views.custom_exception import CustomAPIException, InvalidAuthorizationException, InvalidTokenException
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.userapp.decorators import is_token_validate, role_required
from v1.work_order.serializers.material_name import MaterialNameListSerializer
from v1.work_order.models.material_name import MaterialName as MaterialNameModel
from v1.utility.models.utility_master import get_utility_by_id_string
from v1.commonapp.models.channel import get_channel_by_id_string
from v1.commonapp.views.custom_filter_backend import CustomFilter
from api.messages import *
from api.constants import *


# API Header
# API end Point: api/v1/work_order/:id_string/material_name/list
# API verb: GET
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Material Name list
# Usage: API will fetch all Material Name list
# Tables used: MaterialName
# Author: Chinmay
# Created on: 24/12/2020

class MaterialNameList(generics.ListAPIView):
    try:
        serializer_class = MaterialNameListSerializer
        pagination_class = StandardResultsSetPagination

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    utility = get_utility_by_id_string(self.kwargs['id_string'])
                    queryset = MaterialNameModel.objects.filter(utility=utility, is_active=True)
                    queryset = CustomFilter.get_filtered_queryset(queryset, self.request)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Material Name not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Admin', sub_module='Work Order')
