from rest_framework import status
from v1.commonapp.models.area import get_area_by_id_string
from v1.commonapp.models.city import get_city_by_id_string
from v1.commonapp.models.country import get_country_by_id_string
from v1.commonapp.models.state import get_state_by_id_string
from v1.commonapp.models.sub_area import get_sub_area_by_id_string
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.consumer.models.consumer_category import get_consumer_category_by_id_string
from v1.consumer.models.consumer_ownership import get_consumer_ownership_by_id_string
from v1.consumer.models.consumer_scheme_master import get_scheme_by_id_string
from v1.consumer.models.consumer_sub_category import get_consumer_sub_category_by_id_string
from v1.consumer.models.source_type import get_source_type_by_id_string
from v1.payment.models.consumer_payment import get_payment_by_id_string
from v1.registration.models.registration_status import get_registration_status_by_id_string
from v1.registration.models.registration_type import get_registration_type_by_id_string
from v1.utility.models.utility_master import get_utility_by_id_string


def is_data_verified(request):
    return True


def set_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException("Utility not found.",status_code=status.HTTP_404_NOT_FOUND)
    if "area_id" in validated_data:
        area = get_area_by_id_string(validated_data["area_id"])
        if area:
            validated_data["area_id"] = area.id
        else:
            raise CustomAPIException("Area not found.",status_code=status.HTTP_404_NOT_FOUND)
    if "status_id" in validated_data:
        registration_status = get_registration_status_by_id_string(validated_data["status_id"])
        if registration_status:
            validated_data["status_id"] = registration_status.id
        else:
            raise CustomAPIException("Status not found.", status.HTTP_404_NOT_FOUND)
    if "registration_type_id" in validated_data:
        registration_type = get_registration_type_by_id_string(validated_data["registration_type_id"])
        if registration_type:
            validated_data["registration_type_id"] = registration_type.id
        else:
            raise CustomAPIException("Registration type not found.", status.HTTP_404_NOT_FOUND)
    if "country_id" in validated_data:
        country = get_country_by_id_string(validated_data["country_id"])
        if country:
            validated_data["country_id"] = country.id
        else:
            raise CustomAPIException("Country not found.", status.HTTP_404_NOT_FOUND)
    if "state_id" in validated_data:
        state = get_state_by_id_string(validated_data["state_id"])
        if state:
            validated_data["state_id"] = state.id
        else:
            raise CustomAPIException("State not found.", status.HTTP_404_NOT_FOUND)
    if "city_id" in validated_data:
        city = get_city_by_id_string(validated_data["city_id"])
        if city:
            validated_data["city_id"] = city.id
        else:
            raise CustomAPIException("City not found.", status.HTTP_404_NOT_FOUND)
    if "scheme_id" in validated_data:
        scheme = get_scheme_by_id_string(validated_data["scheme_id"])
        if scheme:
            validated_data["scheme_id"] = scheme.id
        else:
            raise CustomAPIException("Scheme not found.", status.HTTP_404_NOT_FOUND)
    if "sub_area_id" in validated_data:
        sub_area = get_sub_area_by_id_string(validated_data["sub_area_id"])
        if sub_area:
            validated_data["sub_area_id"] = sub_area.id
        else:
            raise CustomAPIException("Sub area not found.", status.HTTP_404_NOT_FOUND)
    if "payment_id" in validated_data:
        payment = get_payment_by_id_string(validated_data["payment_id"])
        if payment:
            validated_data["payment_id"] = payment.id
        else:
            raise CustomAPIException("Payment not found.", status.HTTP_404_NOT_FOUND)
    if "ownership_id" in validated_data:
        ownership = get_consumer_ownership_by_id_string(validated_data["ownership_id"])
        if ownership:
            validated_data["ownership_id"] = ownership.id
        else:
            raise CustomAPIException("Ownership not found.", status.HTTP_404_NOT_FOUND)
    if "consumer_category_id" in validated_data:
        consumer_category = get_consumer_category_by_id_string(validated_data["consumer_category_id"])
        if consumer_category:
            validated_data["consumer_category_id"] = consumer_category.id
        else:
            raise CustomAPIException("Consumer category not found.", status.HTTP_404_NOT_FOUND)
    if "sub_category_id" in validated_data:
        sub_category = get_consumer_sub_category_by_id_string(validated_data["sub_category_id"])
        if sub_category:
            validated_data["sub_category_id"] = sub_category.id
        else:
            raise CustomAPIException("Consumer sub category not found.", status.HTTP_404_NOT_FOUND)
    if "source_id" in validated_data:
        source = get_source_type_by_id_string(validated_data["source_id"])
        if source:
            validated_data["source_id"] = source.id
        else:
            raise CustomAPIException("Source not found.", status.HTTP_404_NOT_FOUND)
    return validated_data