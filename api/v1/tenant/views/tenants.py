import traceback
from pyatspi import state
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.v1.smart360_API.commonapp.models.state import get_state_by_id_string
from api.v1.smart360_API.smart360_API.messages import STATE, SUCCESS, ERROR, EXCEPTION, DATA
from api.v1.smart360_API.smart360_API.settings import DISPLAY_DATE_FORMAT
from api.v1.smart360_API.commonapp.common_functions import get_payload, get_user, is_authorized, is_token_valid
from api.v1.smart360_API.tenant.models.tenant_master import get_tenant,get_tenant_subscription_by_tenant_id_string,get_tenant_subscription_plan_by_tenant_id_string,get_tenant_invoices_by_tenant_id_string,get_tenant_subscription_rate_by_tenant_id_string,get_tenant_payment_by_tenant_id_string,get_tenant_bank_details_by_tenant_id_string,get_tenant_summary_by_tenant_id_string,get_tenant_sub_modules_by_tenant_id_string,get_tenant_documents_by_tenant_id_string
from api.v1.smart360_API.userapp.models.privilege import get_privilege_by_id
from api.v1.smart360_API.commonapp.models.sub_module import get_sub_module_by_id
from api.v1.smart360_API.commonapp.models.country import get_country_by_id_string, get_country_by_id
from api.v1.smart360_API.commonapp.models.city import get_city_by_id_string, get_city_by_id
from v1.commonapp.common_functions import is_token_valid, get_payload, get_user, is_authorized
from v1.commonapp.common_functions import is_token_valid, get_payload, get_user, is_authorized
from v1.commonapp.models.area import get_areas_by_tenant_id_string, get_area_by_id
from v1.commonapp.models.city import get_city_by_id
from v1.commonapp.models.country import get_country_by_id
from v1.commonapp.models.state import get_state_by_id
from v1.tenant.views.common_functions import get_tenant, is_data_verified, save_basic_tenant_details, save_payment_details,save_basic_subscription_details,save_basic_subscription_plan_details,save_basic_subscription_rate_details,save_basic_tenant_bank_details,save_basic_tenant_invoices_details,save_basic_tenant_document_details,save_basic_tenant_sub_modules_details,save_basic_tenant_payments_details

# API Header
# API end Point: api/v1/tenant/list
# API verb: GET
# Package: Basic
# Modules: Tenant
# Sub Module:
# Interaction: Tenant List
# Usage: API will fetch required data for Tenant list
# Tables used: 1.1 Tenant
# Author: Gauri
# Created on: 28/04/2020
class TenantApiView(APIView):
    def get(self, request, format=None):
        try:
            # Initializing output list start
            tenant_list = []
            # Initializing output list end
            # Checking authentication start
            if is_token_valid(request.data['token']):
                payload = get_payload(request.data['token'])
                user = get_user(payload['id_string'])
                # Checking authentication end
                # Checking authorization start
                privilege = get_privilege_by_id(1)
                sub_module = get_sub_module_by_id(1)
                if is_authorized(user, privilege, sub_module):
                    # Checking authorization end
                    # Code for filtering Tenant start
                    tenants, total_pages, page_no = get_tenant(user, request)
                    # Code for filtering tenant end
                    # Code for lookups start
                    statuses = Status.objects.all()
                    countries = get_country_by_id_string(user.tenant.id_string)
                    state = get_state_by_id_string(user.tenant.id_string)
                    # Code for lookups end
                    # Code for sending tenant in response start
                    for tenant in tenants:
                        tenant_list.append({
                            'first_name': tenant.first_name,
                            'phone_no': tenant.phone_no,
                            'email_id': tenant.email_id,
                            'status': statuses.objects.get(id_string=tenant.status_id).status_name,
                            'country_id': countries.objects.get(id_string=tenant.country_id).country_name,
                            'state_id': state.objects.get(id_string=tenant.state_id).state_name,
                            'total_pages': total_pages,
                            'page_no': page_no
                        })
                    return Response({
                        STATE: SUCCESS,
                        'data': tenant_list,
                    }, status=status.HTTP_200_OK)
                    # Code for sending tenant in response end
                else:
                    return Response({
                        STATE: ERROR,
                        'data': '',
                    }, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    STATE: ERROR,
                    'data': '',
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # API Header
        # API end Point: api/v1/tenant/
        # API verb: GET, POST, PUT
        # Package: Basic
        # Modules: All
        # Sub Module: Tenant
        # Interaction: View Tenant, Add Tenant, Edit Tenants
        # Usage: View, Add, Edit Tenants
        # Tables used: 1.1 Tenant
        # Auther: Gauri
        # Created on: 29/04/2020
class TenantApiView(APIView)
    def get(self, request, format=None):
        try:
        # Checking authentication start
            if is_token_valid(request.data['token']):
                payload = get_payload(request.data['token'])
                user = get_user(payload['id_string'])
                # Checking authentication end
                # Checking authorization start
                privilege = get_privilege_by_id(1)
                if is_authorized(user, privilege):
                    # Checking authorization end
                    # Code for lookups start
                    tenant = get_tenant(request.data['id_string'])
                    country = get_country_by_id(tenant.country_id)
                    state = get_state_by_id(tenant.state_id)
                    city = get_city_by_id(tenant.city_id)
                    area = get_area_by_id(tenant.area_id)
                    # Code for lookups end
                    # Code for sending registrations in response start
                    data = {
                        'tenant_id_string': tenant.id_string,
                        'first_name': tenant.name,
                        'email_id': tenant.email_id,
                        'mobile_no': tenant.phone_mobile,
                        'country_id_string': country.id_string,
                        'state_id_string': state.id_string,
                        'city_id_string': city.id_string,
                        'area_id_string': area.id_string,
                        'is_active': tenant.is_active,
                    }
                    return Response({
                    STATE: SUCCESS,
                    DATA: data,
                }, status=status.HTTP_200_OK)
                # Code for sending registrations in response end
                else:
                    return Response({
                        STATE: ERROR,
                        DATA: '',
                    }, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                STATE: ERROR,
                DATA: '',
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({
            STATE: EXCEPTION,
            DATA: '',
            ERROR: str(traceback.print_exc(e))
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 def post(self, request, format=None):
        try:
            # Checking authentication start
            if is_token_valid(request.data['token']):
                payload = get_payload(request.data['token'])
                user = get_user(payload['id_string'])
                # Checking authentication end
                # Checking authorization start
                privilege = get_privilege_by_id(1)
                if is_authorized(user, privilege):
                    # Checking authorization end
                    # Request data verification start
                    if is_data_verified(request):
                        # Request data verification end
                        # Save basic and payment details start
                        tenant, result, error = save_basic_tenant_details(request, user)
                        if result == False:
                            return Response({
                                STATE: EXCEPTION,
                                ERROR: error
                            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                        payment = save_payment_details(request, user, tenant)
                        # Save basic and payment details start
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
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def put(self, request, format=None):
        try:
            # Checking authentication start
            if is_token_valid(request.data['token']):
                payload = get_payload(request.data['token'])
                user = get_user(payload['id_string'])
                # Checking authentication end
                # Checking authorization start
                privilege = get_privilege_by_id(1)
                if is_authorized(user, privilege):
                    # Checking authorization end
                    # Request data verification start
                    if is_data_verified(request):
                        # Request data verification end
                        # Save basic details start
                        tenant, result, error = save_basic_tenant_details(request, user)
                        if result == False:
                            return Response({
                                STATE: EXCEPTION,
                                ERROR: error
                            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                        # Save basic details start
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
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # API Header
        # API end Point: api/v1/tenant/subscription
        # API verb: GET, POST, PUT
        # Package: Basic
        # Modules: All
        # Sub Module: Tenant Subscription
        # Interaction: View Tenant Subscription, Add Tenant Subscription, Edit Tenants Subscription
        # Usage: View, Add, Edit Tenants Subscription
        # Tables used: 1.2 Tenant Subscription
        # Auther: Gauri
        # Created on: 04/05/2020

class TenantSubscriptionApiView(APIView):

    def get(self, request, format=None):
        try:
            tenant_subscription_list = []
            # Checking authentication start
            if is_token_valid(request.data['token']):
                payload = get_payload(request.data['token'])
                user = get_user(payload['id_string'])
            # Checking authentication end

                # Checking authorization start
                privilege = get_privilege_by_id(1)
                sub_module = get_sub_module_by_id(1)
                if is_authorized(user, privilege, sub_module):
                # Checking authorization end

                    # Get Tenant Subscription
                    tenant_subscription = get_tenant_subscription_by_tenant_id_string(request.data['tenant_id_string'])

                    for tenant_subscription in tenant_subscription:
                        tenant_subscription_list.append({
                            'id_string': tenant_subscription.id_string,
                            'name': tenant_subscription.tenant,
                            "subscription_plan_id": tenant_subscription.subscription_plan_id,
                            "subscription_frequency_id": tenant_subscription.subscription_frequency_id,
                            "start_date": tenant_subscription.start_date,
                            "end_date": tenant_subscription.end_date,
                            "validity_id" : tenant_subscription.validity_id
                        })
                    return Response({
                        STATE: SUCCESS,
                        'data': tenant_subscription_list,
                    }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                STATE: EXCEPTION,
                DATA: '',
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        try:
            # Checking authentication start
            if is_token_valid(request.data['token']):
                payload = get_payload(request.data['token'])
                user = get_user(payload['id_string'])
                # Checking authentication end
                # Checking authorization start
                privilege = get_privilege_by_id(1)
                if is_authorized(user, privilege):
                    # Checking authorization end
                    # Request data verification start
                    if is_data_verified(request):
                        # Request data verification end
                        # Save basic and payment details start
                        subscription, result, error = save_basic_subscription_details(request, user)
                        if result == False:
                            return Response({
                                STATE: EXCEPTION,
                                ERROR: error
                            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                        # Save subscription details start
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
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def put(self, request, format=None):
        try:
            # Checking authentication start
            if is_token_valid(request.data['token']):
                payload = get_payload(request.data['token'])
                user = get_user(payload['id_string'])
                # Checking authentication end
                # Checking authorization start
                privilege = get_privilege_by_id(1)
                if is_authorized(user, privilege):
                    # Checking authorization end
                    # Request data verification start
                    if is_data_verified(request):
                        # Request data verification end
                        # Save basic details start
                        tenant, result, error = save_basic_subscription_details(request, user)
                        if result == False:
                            return Response({
                                STATE: EXCEPTION,
                                ERROR: error
                            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                        # Save basic details start
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
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # API Header
            # API end Point: api/v1/tenant/subscription_plan
            # API verb: GET, POST, PUT
            # Package: Basic
            # Modules: All
            # Sub Module: Tenant Subscription Plan
            # Interaction: View Tenant Subscription Plan, Add Tenant Subscription Plan, Edit Tenants Subscription Plan
            # Usage: View, Add, Edit Tenants Subscription Plan
            # Tables used: 1.2 Tenant Subscription Plan
            # Auther: Gauri
            # Created on: 04/05/2020

            class TenantSubscriptionPlanApiView(APIView):

                def get(self, request, format=None):
                    try:
                        tenant_subscription_plan_list = []
                        # Checking authentication start
                        if is_token_valid(request.data['token']):
                            payload = get_payload(request.data['token'])
                            user = get_user(payload['id_string'])
                            # Checking authentication end

                            # Checking authorization start
                            privilege = get_privilege_by_id(1)
                            sub_module = get_sub_module_by_id(1)
                            if is_authorized(user, privilege, sub_module):
                                # Checking authorization end

                                # Get Tenant Subscription Plan
                                tenant_subscription_plan = get_tenant_subscription_plan_by_tenant_id_string(
                                    request.data['tenant_id_string'])

                                for tenant_subscription_plan in tenant_subscription_plan:
                                    tenant_subscription_plan_list.append
                                    ({
                                        'id_string': tenant_subscription_plan.id_string,
                                        'subscription_id': tenant_subscription_plan.subscription_id,
                                        'short_name' : tenant_subscription_plan.short_name,
                                        'subscription_type' : tenant_subscription_plan.subscription_type,
                                        'description': tenant_subscription_plan.description,
                                        'max_utility' : tenant_subscription_plan.description,
                                        'max_user' : tenant_subscription_plan.max_user,
                                        'max_consumer' : tenant_subscription_plan.max_consumer,
                                        'max_storage': tenant_subscription_plan.max_storage,
                                        'is_active': tenant_subscription_plan.is_active
                                    })
                                return Response({
                                    STATE: SUCCESS,
                                    'data': tenant_subscription_plan_list,
                                }, status=status.HTTP_200_OK)
                    except Exception as e:
                        return Response({
                            STATE: EXCEPTION,
                            DATA: '',
                            ERROR: str(traceback.print_exc(e))
                        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                def post(self, request, format=None):
                    try:
                        # Checking authentication start
                        if is_token_valid(request.data['token']):
                            payload = get_payload(request.data['token'])
                            user = get_user(payload['id_string'])
                            # Checking authentication end
                            # Checking authorization start
                            privilege = get_privilege_by_id(1)
                            if is_authorized(user, privilege):
                                # Checking authorization end
                                # Request data verification start
                                if is_data_verified(request):
                                    # Request data verification end
                                    # Save basic and payment details start
                                    subscription_plan, result, error = save_basic_subscription_plan_details(request, user)
                                    if result == False:
                                        return Response({
                                            STATE: EXCEPTION,
                                            ERROR: error
                                        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                                    # Save subscription details start
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
                        return Response({
                            STATE: EXCEPTION,
                            ERROR: str(traceback.print_exc(e))
                        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                def put(self, request, format=None):
                    try:
                        # Checking authentication start
                        if is_token_valid(request.data['token']):
                            payload = get_payload(request.data['token'])
                            user = get_user(payload['id_string'])
                            # Checking authentication end
                            # Checking authorization start
                            privilege = get_privilege_by_id(1)
                            if is_authorized(user, privilege):
                                # Checking authorization end
                                # Request data verification start
                                if is_data_verified(request):
                                    # Request data verification end
                                    # Save basic details start
                                    subscription_plan, result, error = save_basic_subscription_plan_details(request, user)
                                    if result == False:
                                        return Response({
                                            STATE: EXCEPTION,
                                            ERROR: error
                                        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                                    # Save basic details start
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
                        return Response({
                            STATE: EXCEPTION,
                            ERROR: str(traceback.print_exc(e))
                        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # API Header
        # API end Point: api/v1/tenant/status
        # API verb: GET, POST, PUT
        # Package: Basic
        # Modules: All
        # Sub Module: Tenant
        # Interaction: View Tenant Status, Add Tenant Status, Edit Tenants Status
        # Usage: View, Add, Edit Tenants Status
        # Tables used: 1.1 Tenant
        # Auther: Gauri
        # Created on: 03/05/2020

class TenantStatusApiView(APIView):

    def get(self, request, format=None):
        try:
            tenant_status_list = []
            # Checking authentication start
            if is_token_valid(request.data['token']):
                payload = get_payload(request.data['token'])
                user = get_user(payload['id_string'])
            # Checking authentication end

                # Checking authorization start
                privilege = get_privilege_by_id(1)
                sub_module = get_sub_module_by_id(1)
                if is_authorized(user, privilege, sub_module):
                # Checking authorization end

                    # Get registration statuses
                    tenant_statuses = get_tenant_statuses_by_tenant_id_string(request.data['tenant_id_string'])

                    for tenant_status in tenant_statuses:
                        tenant_status_list.append({
                            'id_string': tenant_status.id_string,
                            'name': tenant_status.name
                        })
                    return Response({
                        STATE: SUCCESS,
                        'data': tenant_status_list,
                    }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                STATE: EXCEPTION,
                DATA: '',
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        try:
            pass
        except Exception as e:
            pass

    def put(self, request, format=None):
        try:
            pass
        except Exception as e:
            pass



        # API Header
        # API end Point: api/v1/tenant/subscription_rate
        # API verb: GET, POST, PUT
        # Package: Basic
        # Modules: All
        # Sub Module: Tenant Subscription Rate
        # Interaction: View Tenant Subscription Rate, Add Tenant Subscription Rate, Edit Tenants Subscription Rate
        # Usage: View, Add, Edit Tenants Subscription Rate
        # Tables used: 1.2 Tenant Subscription Rate
        # Auther: Gauri
        # Created on: 04/05/2020
    class TenantSubscriptionRateApiView(APIView):

        def get(self, request, format=None):
            try:
                tenant_subscription_rate_list = []
                # Checking authentication start
                if is_token_valid(request.data['token']):
                    payload = get_payload(request.data['token'])
                    user = get_user(payload['id_string'])
                    # Checking authentication end

                    # Checking authorization start
                    privilege = get_privilege_by_id(1)
                    sub_module = get_sub_module_by_id(1)
                    if is_authorized(user, privilege, sub_module):
                        # Checking authorization end

                        # Get Tenant Subscription Rate
                        tenant_subscription_rate = get_tenant_subscription_rate_by_tenant_id_string(
                            request.data['tenant_id_string'])

                        for tenant_subscription_rate in tenant_subscription_rate:
                            tenant_subscription_rate_list.append
                            ({
                                'id_string': tenant_subscription_rate.id_string,
                                'tenant_subscription_plan_id': tenant_subscription_rate.tenant_subscription_plan_id,
                                'base_rate': tenant_subscription_rate.base_rate,
                                'currency': tenant_subscription_rate.currency,
                                'region': tenant_subscription_rate.region,
                                'country': tenant_subscription_rate.country,
                                'is_taxable': tenant_subscription_rate.is_taxable,
                                'tax': tenant_subscription_rate.tax,
                                'effective_date': tenant_subscription_rate.effective_date
                            })
                        return Response({
                            STATE: SUCCESS,
                            'data': tenant_subscription_rate_list,
                        }, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({
                    STATE: EXCEPTION,
                    DATA: '',
                    ERROR: str(traceback.print_exc(e))
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        def post(self, request, format=None):
            try:
                # Checking authentication start
                if is_token_valid(request.data['token']):
                    payload = get_payload(request.data['token'])
                    user = get_user(payload['id_string'])
                    # Checking authentication end
                    # Checking authorization start
                    privilege = get_privilege_by_id(1)
                    if is_authorized(user, privilege):
                        # Checking authorization end
                        # Request data verification start
                        if is_data_verified(request):
                            # Request data verification end
                            # Save basic and payment details start
                            subscription_rate, result, error = save_basic_subscription_rate_details(request, user)
                            if result == False:
                                return Response({
                                    STATE: EXCEPTION,
                                    ERROR: error
                                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                            # Save subscription details start
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
                return Response({
                    STATE: EXCEPTION,
                    ERROR: str(traceback.print_exc(e))
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        def put(self, request, format=None):
            try:
                # Checking authentication start
                if is_token_valid(request.data['token']):
                    payload = get_payload(request.data['token'])
                    user = get_user(payload['id_string'])
                    # Checking authentication end
                    # Checking authorization start
                    privilege = get_privilege_by_id(1)
                    if is_authorized(user, privilege):
                        # Checking authorization end
                        # Request data verification start
                        if is_data_verified(request):
                            # Request data verification end
                            # Save basic details start
                            subscription_rate, result, error = save_basic_subscription_rate_details(request, user)
                            if result == False:
                                return Response({
                                    STATE: EXCEPTION,
                                    ERROR: error
                                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                            # Save basic details start
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
                return Response({
                    STATE: EXCEPTION,
                    ERROR: str(traceback.print_exc(e))
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # API Header
            # API end Point: api/v1/tenant/invoices
            # API verb: GET, POST, PUT
            # Package: Basic
            # Modules: All
            # Sub Module: Tenant Invoices
            # Interaction: View Tenant Invoices, Add Tenant Invoices, Edit Tenants Invoices
            # Usage: View, Add, Edit Tenants Invoices
            # Tables used: 1.2 Tenant Invoices
            # Auther: Gauri
            # Created on: 04/05/2020

            class TenantInvoicesApiView(APIView):

                def get(self, request, format=None):
                    try:
                        tenant_invoice_list = []
                        # Checking authentication start
                        if is_token_valid(request.data['token']):
                            payload = get_payload(request.data['token'])
                            user = get_user(payload['id_string'])
                            # Checking authentication end

                            # Checking authorization start
                            privilege = get_privilege_by_id(1)
                            sub_module = get_sub_module_by_id(1)
                            if is_authorized(user, privilege, sub_module):
                                # Checking authorization end

                                # Get Tenant Invoices
                                tenant_invoices = get_tenant_invoices_by_tenant_id_string(
                                    request.data['tenant_id_string'])

                                for tenant_invoices in tenant_invoices:
                                    tenant_invoice_list.append
                                    ({
                                        'id_string': tenant_invoices.id_string,
                                        'subscription_id': tenant_invoices.subscription_id,
                                        'tenant_bank_details_id': tenant_invoices.tenant_bank_details_id,
                                        'invoice_number' : tenant_invoices.invoice_number,
                                        'invoice_date': tenant_invoices.invoice_date,
                                        'invoice_amt': tenant_invoices.invoice_amt,
                                        'invoice_tax': tenant_invoices.invoice_tax,
                                        'invoice_url': tenant_invoices.invoice_url,
                                        'due_date': tenant_invoices.due_date,
                                        'contact_name': tenant_invoices.contact_name,
                                        'contact_no': tenant_invoices.contact_no,
                                        'email_id': tenant_invoices.email_id,
                                        'month': tenant_invoices.month,
                                        'billing_address': tenant_invoices.billing_address,
                                        'address' : tenant_invoices.address,
                                        'is_active' : tenant_invoices.is_active,
                                        'created_by': tenant_invoices.created_by,
                                        'updated_by' : tenant_invoices.updated_by,
                                        'created_date' : tenant_invoices.created_date,
                                        'updated_date': tenant_invoices.updated_date
                                    })
                                return Response({
                                    STATE: SUCCESS,
                                    'data': tenant_invoice_list,
                                }, status=status.HTTP_200_OK)
                    except Exception as e:
                        return Response({
                            STATE: EXCEPTION,
                            DATA: '',
                            ERROR: str(traceback.print_exc(e))
                        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                def post(self, request, format=None):
                    try:
                        # Checking authentication start
                        if is_token_valid(request.data['token']):
                            payload = get_payload(request.data['token'])
                            user = get_user(payload['id_string'])
                            # Checking authentication end
                            # Checking authorization start
                            privilege = get_privilege_by_id(1)
                            if is_authorized(user, privilege):
                                # Checking authorization end
                                # Request data verification start
                                if is_data_verified(request):
                                    # Request data verification end
                                    # Save basic and payment details start
                                    tenant_invoices , result, error = save_basic_tenant_invoices_details(request,user)
                                    if result == False:
                                        return Response({
                                            STATE: EXCEPTION,
                                            ERROR: error
                                        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                                    # Save subscription details start
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
                        return Response({
                            STATE: EXCEPTION,
                            ERROR: str(traceback.print_exc(e))
                        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                def put(self, request, format=None):
                    try:
                        # Checking authentication start
                        if is_token_valid(request.data['token']):
                            payload = get_payload(request.data['token'])
                            user = get_user(payload['id_string'])
                            # Checking authentication end
                            # Checking authorization start
                            privilege = get_privilege_by_id(1)
                            if is_authorized(user, privilege):
                                # Checking authorization end
                                # Request data verification start
                                if is_data_verified(request):
                                    # Request data verification end
                                    # Save basic details start
                                    tenant_invoices, result, error = save_basic_tenant_invoices_details(request,
                                                                                                            user)
                                    if result == False:
                                        return Response({
                                            STATE: EXCEPTION,
                                            ERROR: error
                                        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                                    # Save basic details start
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
                        return Response({
                            STATE: EXCEPTION,
                            ERROR: str(traceback.print_exc(e))
                        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                    # API Header
                    # API end Point: api/v1/tenant/payment
                    # API verb: GET, POST, PUT
                    # Package: Basic
                    # Modules: All
                    # Sub Module: Tenant payment
                    # Interaction: View Tenant Payment, Add Tenant Payment, Edit Tenants Payment
                    # Usage: View, Add, Edit Tenants Payment
                    # Tables used: 1.2 Tenant Payment
                    # Auther: Gauri
                    # Created on: 04/05/2020

                    class TenantPaymentApiView(APIView):

                        def get(self, request, format=None):
                            try:
                                tenant_payment_list = []
                                # Checking authentication start
                                if is_token_valid(request.data['token']):
                                    payload = get_payload(request.data['token'])
                                    user = get_user(payload['id_string'])
                                    # Checking authentication end

                                    # Checking authorization start
                                    privilege = get_privilege_by_id(1)
                                    sub_module = get_sub_module_by_id(1)
                                    if is_authorized(user, privilege, sub_module):
                                        # Checking authorization end

                                        # Get Tenant Payment
                                        tenant_payment = get_tenant_payment_by_tenant_id_string(
                                            request.data['tenant_id_string'])

                                        for tenant_payment in tenant_payment:
                                            tenant_payment_list.append
                                            ({
                                                'id_string': tenant_payment.id_string,
                                                'invoice_number': tenant_payment.invoice_number,
                                                'payment_method': tenant_payment.payment_method,
                                                'payment_channel': tenant_payment.payment_channel,
                                                'transaction_no': tenant_payment.id_string,
                                                'transaction_date': tenant_payment.id_string,
                                                'amount': tenant_payment.id_string,
                                                'tax_amount': tenant_payment.id_string,
                                                'currency': tenant_payment.id_string,
                                                'is_active': tenant_payment.id_string,
                                                'created_by': tenant_payment.id_string,
                                                'updated_by': tenant_payment.id_string,
                                                'created_date': tenant_payment.id_string,
                                                'updated_date': tenant_payment.id_string
                                            })
                                        return Response({
                                            STATE: SUCCESS,
                                            'data': tenant_payment_list,
                                        }, status=status.HTTP_200_OK)
                            except Exception as e:
                                return Response({
                                    STATE: EXCEPTION,
                                    DATA: '',
                                    ERROR: str(traceback.print_exc(e))
                                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                    def post(self, request, format=None):
                        try:
                            # Checking authentication start
                            if is_token_valid(request.data['token']):
                                payload = get_payload(request.data['token'])
                                user = get_user(payload['id_string'])
                                # Checking authentication end
                                # Checking authorization start
                                privilege = get_privilege_by_id(1)
                                if is_authorized(user, privilege):
                                    # Checking authorization end
                                    # Request data verification start
                                    if is_data_verified(request):
                                        # Request data verification end
                                        # Save basic and payment details start
                                        tenant_payment, result, error = save_basic_tenant_payments_details(request,
                                                                                                            user)
                                        if result == False:
                                            return Response({
                                                STATE: EXCEPTION,
                                                ERROR: error
                                            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                                        # Save subscription details start
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
                            return Response({
                                STATE: EXCEPTION,
                                ERROR: str(traceback.print_exc(e))
                            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                    def put(self, request, format=None):
                        try:
                            # Checking authentication start
                            if is_token_valid(request.data['token']):
                                payload = get_payload(request.data['token'])
                                user = get_user(payload['id_string'])
                                # Checking authentication end
                                # Checking authorization start
                                privilege = get_privilege_by_id(1)
                                if is_authorized(user, privilege):
                                    # Checking authorization end
                                    # Request data verification start
                                    if is_data_verified(request):
                                        # Request data verification end
                                        # Save basic details start
                                        tenant_payment, result, error = save_basic_tenant_payments_details(request,
                                                                                                            user)
                                        if result == False:
                                            return Response({
                                                STATE: EXCEPTION,
                                                ERROR: error
                                            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                                        # Save basic details start
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
                            return Response({
                                STATE: EXCEPTION,
                                ERROR: str(traceback.print_exc(e))
                            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                    # API Header
                    # API end Point: api/v1/tenant/bank
                    # API verb: GET, POST, PUT
                    # Package: Basic
                    # Modules: All
                    # Sub Module: Tenant Bank Details
                    # Interaction: View Tenant Bank, Add Tenant Bank, Edit Tenants Bank
                    # Usage: View, Add, Edit Tenants Bank
                    # Tables used: 1.3 Tenant Bank Details
                    # Auther: Gauri
                    # Created on: 04/05/2020

                    class TenantBankDetailsApiView(APIView):

                        def get(self, request, format=None):
                            try:
                                tenant_bank_list = []
                                # Checking authentication start
                                if is_token_valid(request.data['token']):
                                    payload = get_payload(request.data['token'])
                                    user = get_user(payload['id_string'])
                                    # Checking authentication end

                                    # Checking authorization start
                                    privilege = get_privilege_by_id(1)
                                    sub_module = get_sub_module_by_id(1)
                                    if is_authorized(user, privilege, sub_module):
                                        # Checking authorization end

                                        # Get Tenant Bank Details
                                        tenant_bank_details = get_tenant_bank_details_by_tenant_id_string(
                                            request.data['tenant_id_string'])

                                        for tenant_bank in tenant_bank_details:
                                            tenant_bank_list.append
                                            ({
                                                'id_string': tenant_bank.id_string,
                                                'bank_name': tenant_bank.bank_name,
                                                'branch_name': tenant_bank.branch_name,
                                                'branch_city': tenant_bank.branch_city,
                                                'account_number': tenant_bank.account_number,
                                                'account_type': tenant_bank.account_type,
                                                'account_name': tenant_bank.account_name,
                                                'ifsc_no': tenant_bank.ifsc_no,
                                                'pan_no': tenant_bank.pan_no,
                                                'gst_no': tenant_bank.gst_no,
                                                'tax_id_no': tenant_bank.tax_id_no,
                                                'is_active': tenant_bank.is_active,
                                                'created_by': tenant_bank.created_by,
                                                'updated_by': tenant_bank.updated_by,
                                                'created_date': tenant_bank.created_date,
                                                'updated_date': tenant_bank.updated_date,
                                            })
                                        return Response({
                                            STATE: SUCCESS,
                                            'data': tenant_bank_list,
                                        }, status=status.HTTP_200_OK)
                            except Exception as e:
                                return Response({
                                    STATE: EXCEPTION,
                                    DATA: '',
                                    ERROR: str(traceback.print_exc(e))
                                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                        def post(self, request, format=None):
                            try:
                                # Checking authentication start
                                if is_token_valid(request.data['token']):
                                    payload = get_payload(request.data['token'])
                                    user = get_user(payload['id_string'])
                                    # Checking authentication end
                                    # Checking authorization start
                                    privilege = get_privilege_by_id(1)
                                    if is_authorized(user, privilege):
                                        # Checking authorization end
                                        # Request data verification start
                                        if is_data_verified(request):
                                            # Request data verification end
                                            # Save basic and payment details start
                                            tenant_bank, result, error = save_basic_tenant_bank_details(request, user)
                                            if result == False:
                                                return Response({
                                                    STATE: EXCEPTION,
                                                    ERROR: error
                                                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                                            # Save subscription details start
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
                                return Response({
                                    STATE: EXCEPTION,
                                    ERROR: str(traceback.print_exc(e))
                                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                        def put(self, request, format=None):
                            try:
                                # Checking authentication start
                                if is_token_valid(request.data['token']):
                                    payload = get_payload(request.data['token'])
                                    user = get_user(payload['id_string'])
                                    # Checking authentication end
                                    # Checking authorization start
                                    privilege = get_privilege_by_id(1)
                                    if is_authorized(user, privilege):
                                        # Checking authorization end
                                        # Request data verification start
                                        if is_data_verified(request):
                                            # Request data verification end
                                            # Save basic details start
                                            tenant_bank, result, error = save_basic_tenant_bank_details(request,user)
                                            if result == False:
                                                return Response({
                                                    STATE: EXCEPTION,
                                                    ERROR: error
                                                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                                            # Save basic details start
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
                                return Response({
                                    STATE: EXCEPTION,
                                    ERROR: str(traceback.print_exc(e))
                                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


                    # API Header
                    # API end Point: api/v1/tenant/summary
                    # API verb: GET, POST, PUT
                    # Package: Basic
                    # Modules: All
                    # Sub Module: Tenant Monthly Summary
                    # Interaction: View Tenant Monthly Summary, Add Tenant Monthly Summary, Edit Tenants Monthly Summary
                    # Usage: View, Add, Edit Tenants Monthly Summary
                    # Tables used: 1.8 Tenant Summary on monthly basis
                    # Auther: Gauri
                    # Created on: 04/05/2020

                    class TenantMonthlySummaryApiView(APIView):

                        def get(self, request, format=None):
                            try:
                                tenant_summary_list = []
                                # Checking authentication start
                                if is_token_valid(request.data['token']):
                                    payload = get_payload(request.data['token'])
                                    user = get_user(payload['id_string'])
                                    # Checking authentication end

                                    # Checking authorization start
                                    privilege = get_privilege_by_id(1)
                                    sub_module = get_sub_module_by_id(1)
                                    if is_authorized(user, privilege, sub_module):
                                        # Checking authorization end

                                        # Get Tenant Summary
                                        tenant_summary = get_tenant_summary_by_tenant_id_string(
                                            request.data['tenant_id_string'])

                                        for tenant_summary in tenant_summary:
                                            tenant_summary_list.append
                                            ({
                                                'id_string': tenant_summary.id_string,
                                                'no_of_utilities': tenant_summary.no_of_utilities,
                                                'no_of_users': tenant_summary.no_of_users,
                                                'no_of_consumers': tenant_summary.no_of_consumers,
                                                'total_no_of_transaction': tenant_summary.total_no_of_transaction,
                                                'no_of_cities': tenant_summary.no_of_cities,
                                                'no_of_documents': tenant_summary.no_of_documents,
                                                'total_storage_in_use': tenant_summary.total_storage_in_use,
                                                'month': tenant_summary.month,
                                                'is_active': tenant_summary.is_active,
                                                'created_by': tenant_summary.created_by,
                                                'updated_by': tenant_summary.updated_by,
                                                'created_date': tenant_summary.created_date,
                                                'updated_date': tenant_summary.updated_date,
                                            })
                                        return Response({
                                            STATE: SUCCESS,
                                            'data': tenant_summary_list,
                                        }, status=status.HTTP_200_OK)
                            except Exception as e:
                                return Response({
                                    STATE: EXCEPTION,
                                    DATA: '',
                                    ERROR: str(traceback.print_exc(e))
                                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                            def post(self, request, format=None):
                                try:
                                    pass
                                except Exception as e:
                                    pass

                            def put(self, request, format=None):
                                try:
                                    pass
                                except Exception as e:
                                    pass



                    # API Header
                    # API end Point: api/v1/tenant/submodules
                    # API verb: GET, POST, PUT
                    # Package: Basic
                    # Modules: All
                    # Sub Module: Tenant System Sub Modules
                    # Interaction: View Tenant System Sub Modules, Add Tenant System Sub Modules, Edit Tenants System Sub Modules
                    # Usage: View, Add, Edit Tenants System Sub Modules
                    # Tables used: 1.7 Tenant System Sub Modules
                    # Auther: Gauri
                    # Created on: 04/05/2020

                    class TenantSubModulesApiView(APIView):

                        def get(self, request, format=None):
                            try:
                                tenant_sub_modules_list = []
                                # Checking authentication start
                                if is_token_valid(request.data['token']):
                                    payload = get_payload(request.data['token'])
                                    user = get_user(payload['id_string'])
                                    # Checking authentication end

                                    # Checking authorization start
                                    privilege = get_privilege_by_id(1)
                                    sub_module = get_sub_module_by_id(1)
                                    if is_authorized(user, privilege, sub_module):
                                        # Checking authorization end

                                        # Get Tenant Modules
                                        tenant_sub_modules = get_tenant_sub_modules_by_tenant_id_string(
                                            request.data['tenant_id_string'])

                                        for tenant_sub_modules in tenant_sub_modules:
                                            tenant_sub_modules_list.append
                                            ({
                                                'id_string': tenant_sub_modules.id_string,
                                                'subscription_id': tenant_sub_modules.subscription_id,
                                                'module_id': tenant_sub_modules.module_id,
                                                'sub_module_id': tenant_sub_modules.sub_module_id,
                                                'sub_module_name': tenant_sub_modules.sub_module_name,
                                                'is_active': tenant_sub_modules.is_active,
                                                'created_by': tenant_sub_modules.created_by,
                                                'updated_by': tenant_sub_modules.updated_by,
                                                'created_date': tenant_sub_modules.created_date,
                                                'updated_date': tenant_sub_modules.updated_date,
                                            })
                                        return Response({
                                            STATE: SUCCESS,
                                            'data': tenant_sub_modules_list,
                                        }, status=status.HTTP_200_OK)
                            except Exception as e:
                                return Response({
                                    STATE: EXCEPTION,
                                    DATA: '',
                                    ERROR: str(traceback.print_exc(e))
                                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                        def post(self, request, format=None):
                            try:
                                # Checking authentication start
                                if is_token_valid(request.data['token']):
                                    payload = get_payload(request.data['token'])
                                    user = get_user(payload['id_string'])
                                    # Checking authentication end
                                    # Checking authorization start
                                    privilege = get_privilege_by_id(1)
                                    if is_authorized(user, privilege):
                                        # Checking authorization end
                                        # Request data verification start
                                        if is_data_verified(request):
                                            # Request data verification end
                                            # Save basic and payment details start
                                            tenant_sub_modules, result, error = save_basic_tenant_sub_modules_details(request, user)
                                            if result == False:
                                                return Response({
                                                    STATE: EXCEPTION,
                                                    ERROR: error
                                                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                                            # Save subscription details start
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
                                return Response({
                                    STATE: EXCEPTION,
                                    ERROR: str(traceback.print_exc(e))
                                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                        def put(self, request, format=None):
                            try:
                                # Checking authentication start
                                if is_token_valid(request.data['token']):
                                    payload = get_payload(request.data['token'])
                                    user = get_user(payload['id_string'])
                                    # Checking authentication end
                                    # Checking authorization start
                                    privilege = get_privilege_by_id(1)
                                    if is_authorized(user, privilege):
                                        # Checking authorization end
                                        # Request data verification start
                                        if is_data_verified(request):
                                            # Request data verification end
                                            # Save basic details start
                                            tenant_sub_modules, result, error = save_basic_tenant_sub_modules_details(request, user)
                                            if result == False:
                                                return Response({
                                                    STATE: EXCEPTION,
                                                    ERROR: error
                                                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                                            # Save basic details start
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
                                return Response({
                                    STATE: EXCEPTION,
                                    ERROR: str(traceback.print_exc(e))
                                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                            def post(self, request, format=None):
                            try:
                                # Checking authentication start
                                if is_token_valid(request.data['token']):
                                    payload = get_payload(request.data['token'])
                                    user = get_user(payload['id_string'])
                                    # Checking authentication end
                                    # Checking authorization start
                                    privilege = get_privilege_by_id(1)
                                    if is_authorized(user, privilege):
                                        # Checking authorization end
                                        # Request data verification start
                                        if is_data_verified(request):
                                            # Request data verification end
                                            # Save basic and payment details start
                                            tenant_sub_modules, result, error = save_basic_tenant_sub_modules_details(request, user)
                                            if result == False:
                                                return Response({
                                                    STATE: EXCEPTION,
                                                    ERROR: error
                                                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                                            # Save subscription details start
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
                                return Response({
                                    STATE: EXCEPTION,
                                    ERROR: str(traceback.print_exc(e))
                                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                        def put(self, request, format=None):
                            try:
                                # Checking authentication start
                                if is_token_valid(request.data['token']):
                                    payload = get_payload(request.data['token'])
                                    user = get_user(payload['id_string'])
                                    # Checking authentication end
                                    # Checking authorization start
                                    privilege = get_privilege_by_id(1)
                                    if is_authorized(user, privilege):
                                        # Checking authorization end
                                        # Request data verification start
                                        if is_data_verified(request):
                                            # Request data verification end
                                            # Save basic details start
                                            tenant_sub_modules, result, error = save_basic_tenant_sub_modules_details(request, user)
                                            if result == False:
                                                return Response({
                                                    STATE: EXCEPTION,
                                                    ERROR: error
                                                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                                            # Save basic details start
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
                                return Response({
                                    STATE: EXCEPTION,
                                    ERROR: str(traceback.print_exc(e))
                                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                            # API Header
                            # API end Point: api/v1/tenant/documents
                            # API verb: GET, POST, PUT
                            # Package: Basic
                            # Modules: All
                            # Sub Module: Tenant Documents
                            # Interaction: View Tenant Documents, Add Tenant Documents , Edit Tenants System Sub Modules
                            # Usage: View, Add, Edit Tenants Documents
                            # Tables used: 1.7 Tenant Documents
                            # Auther: Gauri
                            # Created on: 04/05/2020

                            class TenantDocumentsApiView(APIView):

                                def get(self, request, format=None):
                                    try:
                                        tenant_document_list = []
                                        # Checking authentication start
                                        if is_token_valid(request.data['token']):
                                            payload = get_payload(request.data['token'])
                                            user = get_user(payload['id_string'])
                                            # Checking authentication end

                                            # Checking authorization start
                                            privilege = get_privilege_by_id(1)
                                            sub_module = get_sub_module_by_id(1)
                                            if is_authorized(user, privilege, sub_module):
                                                # Checking authorization end

                                                # Get Tenant Documents
                                                tenant_document = get_tenant_documents_by_tenant_id_string(
                                                    request.data['tenant_id_string'])

                                                for tenant_document in tenant_document:
                                                    tenant_document.append
                                                    ({
                                                        'id_string': tenant_document.id_string,
                                                        'document_name':tenant_document.document_name,
                                                        'document_type':tenant_document.document_type,
                                                        'sub_module_id':tenant_document.sub_module_id,
                                                        'document_extension':tenant_document.document_extension,
                                                        'document_link':tenant_document.document_link,
                                                        'is_active': tenant_document.is_active,
                                                        'created_by': tenant_document.created_by,
                                                        'updated_by': tenant_document.updated_by,
                                                        'created_date': tenant_document.created_date,
                                                        'updated_date': tenant_document.updated_date,

                                                    })
                                                return Response({
                                                    STATE: SUCCESS,
                                                    'data': tenant_document_list,
                                                }, status=status.HTTP_200_OK)
                                    except Exception as e:
                                        return Response({
                                            STATE: EXCEPTION,
                                            DATA: '',
                                            ERROR: str(traceback.print_exc(e))
                                        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                                def post(self, request, format=None):
                                    try:
                                        # Checking authentication start
                                        if is_token_valid(request.data['token']):
                                            payload = get_payload(request.data['token'])
                                            user = get_user(payload['id_string'])
                                            # Checking authentication end
                                            # Checking authorization start
                                            privilege = get_privilege_by_id(1)
                                            if is_authorized(user, privilege):
                                                # Checking authorization end
                                                # Request data verification start
                                                if is_data_verified(request):
                                                    # Request data verification end
                                                    # Save basic and payment details start
                                                    tenant_document, result, error = save_basic_tenant_document_details(request,
                                                                                                                user)
                                                    if result == False:
                                                        return Response({
                                                            STATE: EXCEPTION,
                                                            ERROR: error
                                                        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                                                    # Save subscription details start
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
                                        return Response({
                                            STATE: EXCEPTION,
                                            ERROR: str(traceback.print_exc(e))
                                        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                                def put(self, request, format=None):
                                    try:
                                        # Checking authentication start
                                        if is_token_valid(request.data['token']):
                                            payload = get_payload(request.data['token'])
                                            user = get_user(payload['id_string'])
                                            # Checking authentication end
                                            # Checking authorization start
                                            privilege = get_privilege_by_id(1)
                                            if is_authorized(user, privilege):
                                                # Checking authorization end
                                                # Request data verification start
                                                if is_data_verified(request):
                                                    # Request data verification end
                                                    # Save basic details start
                                                    tenant_document, result, error = save_basic_tenant_document_details(request,
                                                                                                                user)
                                                    if result == False:
                                                        return Response({
                                                            STATE: EXCEPTION,
                                                            ERROR: error
                                                        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                                                    # Save basic details start
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
                                        return Response({
                                            STATE: EXCEPTION,
                                            ERROR: str(traceback.print_exc(e))
                                        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                                        # API Header
                                        # API end Point: api/v1/countries
                                        # API verb: GET
                                        # Package: Basic
                                        # Modules: All
                                        # Sub Module: Get Countries
                                        # Interaction: All
                                        # Usage: View
                                        # Tables used: All
                                        # Auther: Gauri
                                        # Created on: 08/05/2020

                                        class getCountries(APIView):

                                            def get(self, request, format=None):
                                                try:
                                                    country_list = []
                                                    # Checking authentication start
                                                    if is_token_valid(request.data['token']):
                                                        payload = get_payload(request.data['token'])
                                                        user = get_user(payload['id_string'])
                                                        # Checking authentication end

                                                        # Checking authorization start
                                                        privilege = get_privilege_by_id(1)
                                                        sub_module = get_sub_module_by_id(1)
                                                        if is_authorized(user, privilege, sub_module):
                                                            # Checking authorization end

                                                            # Get Tenant Modules
                                                            tenant_sub_modules = get_tenant_sub_modules_by_tenant_id_string(
                                                                request.data['tenant_id_string'])

                                                            for tenant_sub_modules in tenant_sub_modules:
                                                                tenant_sub_modules_list.append
                                                                ({
                                                                    'id_string': tenant_sub_modules.id_string,
                                                                    'subscription_id': tenant_sub_modules.subscription_id,
                                                                    'module_id': tenant_sub_modules.module_id,
                                                                    'sub_module_id': tenant_sub_modules.sub_module_id,
                                                                    'sub_module_name': tenant_sub_modules.sub_module_name,
                                                                    'is_active': tenant_sub_modules.is_active,
                                                                    'created_by': tenant_sub_modules.created_by,
                                                                    'updated_by': tenant_sub_modules.updated_by,
                                                                    'created_date': tenant_sub_modules.created_date,
                                                                    'updated_date': tenant_sub_modules.updated_date,
                                                                })
                                                            return Response({
                                                                STATE: SUCCESS,
                                                                'data': tenant_sub_modules_list,
                                                            }, status=status.HTTP_200_OK)
                                                except Exception as e:
                                                    return Response({
                                                        STATE: EXCEPTION,
                                                        DATA: '',
                                                        ERROR: str(traceback.print_exc(e))
                                                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                                            def post(self, request, format=None):
                                                try:
                                                    pass
                                                except Exception as e:
                                                    pass

                                            def put(self, request, format=None):
                                                try:
                                                    pass
                                                except Exception as e:
                                                    pass