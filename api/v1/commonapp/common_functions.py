import os
import jwt  # jwt token library
from rest_framework import status, serializers
from master.models import get_user_by_id_string, check_user_id_string_exists,get_user_by_id
from v1.commonapp.models.module import get_module_by_id_string
from v1.commonapp.models.sub_module import get_sub_module_by_id_string
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.commonapp.views.logger import logger
from v1.userapp.models.user_privilege import check_user_privilege_exists
from v1.userapp.models.user_token import check_token_exists, check_token_exists_for_user
from v1.userapp.models.user_utility import check_user_utility_exists
from v1.utility.models.utility_master import get_utility_by_id_string
from v1.utility.models.utility_module import get_utility_module_by_id_string
from v1.utility.models.utility_sub_module import get_utility_submodule_by_id_string
from v1.utility.models.utility_payment_channel import get_utility_payment_channel_by_id_string
from v1.tenant.models.tenant_master import get_tenant_by_id_string
from v1.commonapp.models.products import get_product_by_id_string
from v1.commonapp.models.region import get_region_by_id_string
from v1.commonapp.models.country import get_country_by_id_string
from v1.commonapp.models.state import get_state_by_id_string
from v1.commonapp.models.city import get_city_by_id_string
from v1.commonapp.models.zone import get_zone_by_id_string
from v1.commonapp.models.area import get_area_by_id_string
from v1.commonapp.models.sub_area import get_sub_area_by_id_string
from v1.commonapp.models.work_order_type import get_work_order_type_by_id_string
from v1.commonapp.models.work_order_sub_type import get_work_order_sub_type_by_id_string
from v1.utility.models.utility_work_order_type import get_utility_work_order_type_by_id_string
from v1.utility.models.utility_region import get_utility_region_by_id_string

from v1.commonapp.models.channel import get_channel_by_id_string
from v1.commonapp.models.department import get_department_by_id_string
from v1.commonapp.models.department_subtype import get_department_subtype_by_id_string
from v1.campaign.models.campaign_type import get_campaign_type_by_id_string
from v1.commonapp.models.division import get_division_by_id_string
from v1.commonapp.models.document_type import get_document_type_by_id_string
from v1.utility.models.utility_document_type import get_utility_document_type_by_id_string
from v1.consumer.models.consumer_category import get_consumer_category_by_id_string
from v1.commonapp.models.global_lookup import get_global_lookup_by_id_string
from v1.commonapp.models.notification_type import get_notification_type_by_id_string
from v1.commonapp.models.integration_type import get_integration_type_by_id_string
from v1.commonapp.models.integration_subtype import get_integration_sub_type_by_id_string
from v1.utility.models.utility_product import get_utility_product_by_id_string
from v1.consumer.models.consumer_token import get_consumer_token_by_token,check_token_exists_for_consumer
from v1.consumer.models.consumer_master import get_consumer_by_id_string
from v1.consumer.models.consumer_master import get_consumer_by_id_string
from v1.commonapp.views.settings_reader import SettingReader

from v1.commonapp.models.transition_configuration import TransitionConfiguration, TRANSITION_CHANNEL_DICT, \
    is_transition_configuration_exists
from v1.commonapp.views.logger import logger
from v1.commonapp.views.notifications import OutboundHandler, EmailHandler, SMSHandler
from v1.commonapp.models.notification_template import get_notification_template_by_id
from v1.commonapp.models.transition_configuration import get_transition_configuration_by_id
from v1.commonapp.views.secret_reader import SecretReader
from master import models
from v1.consumer.models.consumer_service_contract_details import get_consumer_service_contract_detail_by_id
from v1.consumer.models.consumer_master import get_consumer_by_consumer_no
from v1.work_order import models as work_orderMdl


setting_reader = SettingReader()
secret_reader = SecretReader()

def get_payload(token):
    try:
        return jwt.decode(token, secret_reader.get_secret(), algorithms='HS256')
    except:
        return False


def get_user_from_token(token):
    decoded_token = get_payload(token)
    return decoded_token['user_id_string']


# def is_token_valid(token):
#     try:
#         decoded_token = get_payload(token)
#         user_obj = get_user_by_id_string(decoded_token['user_id_string'])
#         if check_token_exists_for_user(token, user_obj.id):
#             return True, user_obj.id_string
#         else:
#             return False
#     except Exception as e:
#         logger().log(e, 'ERROR', user='test', name='test')
#         return False


def is_token_valid(token):
    try:
        decoded_token = get_payload(token)
        print("DEOCED",decoded_token)
        if decoded_token:
            if decoded_token['type'] == setting_reader.get_user():
                user_obj = get_user_by_id_string(decoded_token['user_id_string'])
                if check_token_exists_for_user(token, user_obj.id):
                    return True, user_obj.id_string
                else:
                    return False
            elif decoded_token['type'] == setting_reader.get_consumer_user():
                consumer_obj = get_consumer_by_id_string(decoded_token['user_id_string'])
                if check_token_exists_for_consumer(token, consumer_obj.id):
                    return True, consumer_obj.id_string
                else:
                    return False
        else:
            return Response({
                STATE: ERROR,
                RESULTS: INVALID_TOKEN,
            }, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        logger().log(e, 'ERROR', user='test', name='test')
        return False

def is_authorized(module_id, sub_module_id, privilege_id, user_id):
    return True
    try:
        if check_user_privilege_exists(user_obj.id, module_id, sub_module_id, privilege_id):
            return True
        else:
            return False
    except Exception as e:
        logger().log(e, 'ERROR', user='test', name='test')
        return False





def is_utility(utility_id, user_obj):
    try:
        if check_user_utility_exists(user_obj.id, utility_id):
            return True
        else:
            return False

    except Exception as e:
        logger().log(e, 'ERROR', user='test', name='test')
        return False

def set_note_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            print(utility)
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException("Utility not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "module_id" in validated_data:
        module = get_utility_module_by_id_string(validated_data["module_id"])
        if module:
            validated_data["module_id"] = module.id
        else:
            raise CustomAPIException("Module not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "sub_module_id" in validated_data:
        sub_module = get_utility_submodule_by_id_string(validated_data["sub_module_id"])
        if sub_module:
            validated_data["sub_module_id"] = sub_module.id
        else:
            raise CustomAPIException("Sub module not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_region_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException("Utility not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "tenant_id" in validated_data:
        tenant = get_tenant_by_id_string(validated_data["tenant_id"])
        if tenant:
            validated_data["tenant_id"] = tenant.id
        else:
            raise CustomAPIException("Tenant not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "region_id" in validated_data:
        region = get_region_by_id_string(validated_data["region_id"])
        if region:
            validated_data["region_id"] = region.id
        else:
            raise CustomAPIException("Region not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_document_type_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException("Utility not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "tenant_id" in validated_data:
        tenant = get_tenant_by_id_string(validated_data["tenant_id"])
        if tenant:
            validated_data["tenant_id"] = tenant.id
        else:
            raise CustomAPIException("Tenant not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "document_type_id" in validated_data:
        document_type = get_document_type_by_id_string(validated_data["document_type_id"])
        if document_type:
            validated_data["document_type_id"] = document_type.id
        else:
            raise CustomAPIException("Document Type Not Found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_document_subtype_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException("Utility not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "tenant_id" in validated_data:
        tenant = get_tenant_by_id_string(validated_data["tenant_id"])
        if tenant:
            validated_data["tenant_id"] = tenant.id
        else:
            raise CustomAPIException("Tenant not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "document_type_id" in validated_data:
        document_type = get_utility_document_type_by_id_string(validated_data["document_type_id"])
        if document_type:
            validated_data["document_type_id"] = document_type.id
        else:
            raise CustomAPIException("Document Type Not Found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_document_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException("Utility not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "tenant_id" in validated_data:
        tenant = get_tenant_by_id_string(validated_data["tenant_id"])
        if tenant:
            validated_data["tenant_id"] = tenant.id
        else:
            raise CustomAPIException("Tenant not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "document_type_id" in validated_data:
        document_type = get_utility_document_type_by_id_string(validated_data["document_type_id"])
        if document_type:
            validated_data["document_type_id"] = document_type.id
        else:
            raise CustomAPIException("Document Type Not Found.", status_code=status.HTTP_404_NOT_FOUND)

    if "sub_module_id_string" in validated_data:
        sub_module = get_sub_module_by_id_string(validated_data["sub_module_id_string"])
        if sub_module:
            validated_data["sub_module_id_string"] = sub_module.id
        else:
            raise CustomAPIException("sub_module not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "module_id_string" in validated_data:
        module = get_module_by_id_string(validated_data["module_id_string"])
        if module:
            validated_data["module_id_string"] = module.id
        else:
            raise CustomAPIException("module not found.", status_code=status.HTTP_404_NOT_FOUND)

    return validated_data


def set_country_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException("Utility not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "tenant_id" in validated_data:
        tenant = get_tenant_by_id_string(validated_data["tenant_id"])
        if tenant:
            validated_data["tenant_id"] = tenant.id
        else:
            raise CustomAPIException("Tenant not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "region_id" in validated_data:
        region = get_utility_region_by_id_string(validated_data["region_id"])
        if region:
            validated_data["region_id"] = region.id
        else:
            raise CustomAPIException("Region not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_state_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException("Utility not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "tenant_id" in validated_data:
        tenant = get_tenant_by_id_string(validated_data["tenant_id"])
        if tenant:
            validated_data["tenant_id"] = tenant.id
        else:
            raise CustomAPIException("Tenant not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "country_id" in validated_data:
        country_name = get_country_by_id_string(validated_data["country_id"])
        if country_name:
            validated_data["country_id"] = country_name.id
        else:
            raise CustomAPIException("Country not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_city_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException("Utility not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "tenant_id" in validated_data:
        tenant = get_tenant_by_id_string(validated_data["tenant_id"])
        if tenant:
            validated_data["tenant_id"] = tenant.id
        else:
            raise CustomAPIException("Tenant not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "state_id" in validated_data:
        state = get_state_by_id_string(validated_data["state_id"])
        if state:
            validated_data["state_id"] = state.id
        else:
            raise CustomAPIException("State not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_zone_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException("Utility not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "tenant_id" in validated_data:
        tenant = get_tenant_by_id_string(validated_data["tenant_id"])
        if tenant:
            validated_data["tenant_id"] = tenant.id
        else:
            raise CustomAPIException("Tenant not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "city_id" in validated_data:
        city = get_city_by_id_string(validated_data["city_id"])
        if city:
            validated_data["city_id"] = city.id
        else:
            raise CustomAPIException("City not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_division_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException("Utility not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "tenant_id" in validated_data:
        tenant = get_tenant_by_id_string(validated_data["tenant_id"])
        if tenant:
            validated_data["tenant_id"] = tenant.id
        else:
            raise CustomAPIException("Tenant not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "zone_id" in validated_data:
        zone = get_zone_by_id_string(validated_data["zone_id"])
        if zone:
            validated_data["zone_id"] = zone.id
        else:
            raise CustomAPIException("Zone not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_area_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException("Utility not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "tenant_id" in validated_data:
        tenant = get_tenant_by_id_string(validated_data["tenant_id"])
        if tenant:
            validated_data["tenant_id"] = tenant.id
        else:
            raise CustomAPIException("Tenant not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "division_id" in validated_data:
        division = get_division_by_id_string(validated_data["division_id"])
        if division:
            validated_data["division_id"] = division.id
        else:
            raise CustomAPIException("Division not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_subarea_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException("Utility not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "tenant_id" in validated_data:
        tenant = get_tenant_by_id_string(validated_data["tenant_id"])
        if tenant:
            validated_data["tenant_id"] = tenant.id
        else:
            raise CustomAPIException("Tenant not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "area_id" in validated_data:
        area = get_area_by_id_string(validated_data["area_id"])
        if area:
            validated_data["area_id"] = area.id
        else:
            raise CustomAPIException("Area not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_premise_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException("Utility not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "tenant_id" in validated_data:
        tenant = get_tenant_by_id_string(validated_data["tenant_id"])
        if tenant:
            validated_data["tenant_id"] = tenant.id
        else:
            raise CustomAPIException("Tenant not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "category_id" in validated_data:
        category = get_consumer_category_by_id_string(validated_data["category_id"])
        if category:
            validated_data["category_id"] = category.id
        else:
            raise CustomAPIException("Consumer Category not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "meter_id" in validated_data:
        meter = get_global_lookup_by_id_string(validated_data["meter_id"])
        if meter:
            validated_data["meter_id"] = meter.id
        else:
            raise CustomAPIException("Meter Not Found", status_code=status.HTTP_404_NOT_FOUND)
    if "subarea_id" in validated_data:
        subarea = get_sub_area_by_id_string(validated_data["subarea_id"])
        if subarea:
            validated_data["subarea_id"] = subarea.id
        else:
            raise CustomAPIException("SubArea not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_skill_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException("Utility not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "tenant_id" in validated_data:
        tenant = get_tenant_by_id_string(validated_data["tenant_id"])
        if tenant:
            validated_data["tenant_id"] = tenant.id
        else:
            raise CustomAPIException("Tenant not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_frequency_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException("Utility not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "tenant_id" in validated_data:
        tenant = get_tenant_by_id_string(validated_data["tenant_id"])
        if tenant:
            validated_data["tenant_id"] = tenant.id
        else:
            raise CustomAPIException("Tenant not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "campaign_type_id" in validated_data:
        campaign_type = get_campaign_type_by_id_string(validated_data["campaign_type_id"])
        if campaign_type:
            validated_data["campaign_type_id"] = campaign_type.id
        else:
            raise CustomAPIException("Campaign Type not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "channel_type_id" in validated_data:
        channel_type = get_utility_payment_channel_by_id_string(validated_data["channel_type_id"])
        if channel_type:
            validated_data["channel_type_id"] = channel_type.id
        else:
            raise CustomAPIException("Channel Type not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_channel_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException("Utility not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "tenant_id" in validated_data:
        tenant = get_tenant_by_id_string(validated_data["tenant_id"])
        if tenant:
            validated_data["tenant_id"] = tenant.id
        else:
            raise CustomAPIException("Tenant not found.", status_code=status.HTTP_404_NOT_FOUND)

    # if "channel_id" in validated_data:
    #     channel = get_channel_by_id_string(validated_data["channel_id"])
    #     if channel:
    #         validated_data["channel_id"] = channel.id
    #     else:
    #         raise CustomAPIException("Channel not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_service_type_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException("Utility not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "tenant_id" in validated_data:
        tenant = get_tenant_by_id_string(validated_data["tenant_id"])
        if tenant:
            validated_data["tenant_id"] = tenant.id
        else:
            raise CustomAPIException("Tenant not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_service_subtype_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException("Utility not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "tenant_id" in validated_data:
        tenant = get_tenant_by_id_string(validated_data["tenant_id"])
        if tenant:
            validated_data["tenant_id"] = tenant.id
        else:
            raise CustomAPIException("Tenant not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_product_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException("Utility not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "tenant_id" in validated_data:
        tenant = get_tenant_by_id_string(validated_data["tenant_id"])
        if tenant:
            validated_data["tenant_id"] = tenant.id
        else:
            raise CustomAPIException("Tenant not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "product_id" in validated_data:
        product = get_product_by_id_string(validated_data["product_id"])
        if product:
            validated_data["product_id"] = product.id
        else:
            raise CustomAPIException("Product not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


class ChoiceField(serializers.ChoiceField):

    def to_representation(self, obj):
        return self._choices[obj]


def set_department_type_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException("Utility not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "tenant_id" in validated_data:
        tenant = get_tenant_by_id_string(validated_data["tenant_id"])
        if tenant:
            validated_data["tenant_id"] = tenant.id
        else:
            raise CustomAPIException("Tenant not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "department_type_id" in validated_data:
        department_type = get_department_by_id_string(validated_data["department_type_id"])
        if department_type:
            validated_data["department_type_id"] = department_type.id
        else:
            raise CustomAPIException("Department Type not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_department_subtype_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException("Utility not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "tenant_id" in validated_data:
        tenant = get_tenant_by_id_string(validated_data["tenant_id"])
        if tenant:
            validated_data["tenant_id"] = tenant.id
        else:
            raise CustomAPIException("Tenant not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "department_subtype_id" in validated_data:
        department_subtype = get_department_subtype_by_id_string(validated_data["department_subtype_id"])
        if department_subtype:
            validated_data["department_subtype_id"] = department_subtype.id
        else:
            raise CustomAPIException("Department SubType not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_notification_type_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException("Utility not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "tenant_id" in validated_data:
        tenant = get_tenant_by_id_string(validated_data["tenant_id"])
        if tenant:
            validated_data["tenant_id"] = tenant.id
        else:
            raise CustomAPIException("Tenant not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_notification_subtype_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException("Utility not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "tenant_id" in validated_data:
        tenant = get_tenant_by_id_string(validated_data["tenant_id"])
        if tenant:
            validated_data["tenant_id"] = tenant.id
        else:
            raise CustomAPIException("Tenant not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "notification_type_id" in validated_data:
        notification_type = get_notification_type_by_id_string(validated_data["notification_type_id"])
        if notification_type:
            validated_data["notification_type_id"] = notification_type.id
        else:
            raise CustomAPIException("Notification Type not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_integration_master_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException("Utility not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "tenant_id" in validated_data:
        tenant = get_tenant_by_id_string(validated_data["tenant_id"])
        if tenant:
            validated_data["tenant_id"] = tenant.id
        else:
            raise CustomAPIException("Tenant not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "integration_type_id" in validated_data:
        integration_type = get_integration_type_by_id_string(validated_data["integration_type_id"])
        if integration_type:
            validated_data["integration_type_id"] = integration_type.id
        else:
            raise CustomAPIException("Integration Type not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "integration_sub_type_id" in validated_data:
        integration_sub_type = get_integration_sub_type_by_id_string(validated_data["integration_sub_type_id"])
        if integration_sub_type:
            validated_data["integration_sub_type_id"] = integration_sub_type.id
        else:
            raise CustomAPIException("Integration Sub Type not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "module_id" in validated_data:
        module = get_utility_module_by_id_string(validated_data["module_id"])
        if module:
            validated_data["module_id"] = module.id
        else:
            raise CustomAPIException("Module not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_work_order_type_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException("Utility not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "tenant_id" in validated_data:
        tenant = get_tenant_by_id_string(validated_data["tenant_id"])
        if tenant:
            validated_data["tenant_id"] = tenant.id
        else:
            raise CustomAPIException("Tenant not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "work_order_type_id" in validated_data:
        work_order_type = get_work_order_type_by_id_string(validated_data["work_order_type_id"])
        if work_order_type:
            validated_data["work_order_type_id"] = work_order_type.id
        else:
            raise CustomAPIException("Work Order Type not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_work_order_sub_type_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException("Utility not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "tenant_id" in validated_data:
        tenant = get_tenant_by_id_string(validated_data["tenant_id"])
        if tenant:
            validated_data["tenant_id"] = tenant.id
        else:
            raise CustomAPIException("Tenant not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "work_order_sub_type_id" in validated_data:
        work_order_sub_type = get_work_order_sub_type_by_id_string(validated_data["work_order_sub_type_id"])
        if work_order_sub_type:
            validated_data["work_order_sub_type_id"] = work_order_sub_type.id
        else:
            raise CustomAPIException("Work Order Type not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "utility_work_order_type_id" in validated_data:
        utility_work_order_type = get_utility_work_order_type_by_id_string(validated_data["utility_work_order_type_id"])
        if utility_work_order_type:
            validated_data["utility_work_order_type_id"] = utility_work_order_type.id
        else:
            raise CustomAPIException("Utility Work Order Type not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_notification_template_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException("Utility not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "tenant_id" in validated_data:
        tenant = get_tenant_by_id_string(validated_data["tenant_id"])
        if tenant:
            validated_data["tenant_id"] = tenant.id
        else:
            raise CustomAPIException("Tenant not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def validate_user_data(validated_data):
    if "user_id_string" in validated_data:
        user_obj = get_user_by_id_string(validated_data["user_id_string"])

        if user_obj:
            validated_data["object_id"] = user_obj.id
        else:
            raise CustomAPIException("user_obj not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def check_user(token):
    print("this is token==",token)
    decoded_token = get_payload(token)
    print("decoded token==",decoded_token['user_id_string'])
    if decoded_token:
        if decoded_token['type'] == setting_reader.get_user():
            print("inside U")
            user_id_string = get_user_from_token(token)
            user = get_user_by_id_string(user_id_string)
        elif decoded_token['type'] == setting_reader.get_consumer_user():
            print("Inside C")
            user_token = get_consumer_token_by_token(token)
            user_id_string = decoded_token['user_id_string']
            print("---------",user_id_string)
            user = get_consumer_by_id_string(user_id_string)
            print("======",user)
        else:
            user=False
    return user



def perform_events(next_state, obj, transition_object):
    try:
        print('=====',next_state, obj, transition_object)
        if TransitionConfiguration.objects.filter(transition_object=transition_object, transition_state=next_state,
                                                  tenant=obj.tenant, is_active=True).exists():

            transition_objs = TransitionConfiguration.objects.filter(transition_object=transition_object,
                                                                     transition_state=next_state,
                                                                     tenant=obj.tenant, is_active=True)
            print('...........',transition_objs)
            for transition_obj in transition_objs:
                if transition_obj.channel == TRANSITION_CHANNEL_DICT['EMAIL']:
                    transition_obj = get_transition_configuration_by_id(transition_obj.id)
                    print('....transition_obj...',transition_obj)
                    # Call to the first function

                    e1 = EmailHandler(transition_obj.transition_object, obj)
                    print('------e1000-----',e1)

                    array = e1.handle_communications()
                    print('--------array-----',array)

                    html = get_notification_template_by_id(transition_obj.template_id)
                    print('=======html=======',html)

                    email_body = e1.html_handler(html.template, array)

                    print('--------',transition_obj.transition_object)

                    if transition_obj.transition_object == 5:
                        consumer_contract = get_consumer_service_contract_detail_by_id(obj.consumer_service_contract_detail_id)
                        consumer = get_consumer_by_consumer_no(consumer_contract.consumer_no) 
                        print(',,,,,,,,,,,',obj.get_state_display())
                        if obj.get_state_display() == 'NOT ASSIGNED':                            
                            e1.send_email('Appointment Created SuccessFully', SecretReader.get_from_email(),
                                          [consumer.email], None, None, email_body)
                            
                        elif obj.get_state_display() == 'ASSIGNED':
                            user_obj = get_user_by_id(obj.user_id)
                            print('=====user_obj====',user_obj.email)
                            e1.send_email('Appointment Assigned SuccessFully', SecretReader.get_from_email(),
                                      [consumer.email,user_obj.email], None, None, email_body)
                    else:
                        e1.send_email('Utility Created SuccessFully', SecretReader.get_from_email(),
                                      [obj.email_id], None, None, email_body)

                if transition_obj.channel == TRANSITION_CHANNEL_DICT['SMS']:
                    # Call to the first function
                    e1 = SMSHandler(transition_obj.transition_object, obj)

                    array = e1.handle_communications()

                    transition_obj = get_transition_configuration_by_id(transition_obj.id)

                    html = get_notification_template_by_id(transition_obj.template_id)

                    sms_body = e1.html_handler(html.template, array)
                    print("SMS Body", obj.phone_no)
                    e1.send_sms(sms_body, SecretReader.get_from_number(),
                                obj.phone_no)
        else:
            pass
    except Exception as e:
        logger().log(e, 'LOW', module='Admin', sub_module='Utility Configuration')
        pass
