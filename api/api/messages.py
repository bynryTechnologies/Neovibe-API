__author__ = 'aki'

# *********** KEY CONSTANTS **************
RESULTS = 'results'
RESULT = 'result'
MESSAGE = 'message'
RESPONSE_DATA = 'response_data'
Token = 'token'
STATE = 'state'
DATA = 'data'
ERROR = 'error'
DUPLICATE = 'duplicate',
ID_STRING = 'id_string'

# *********** VALUE CONSTANTS **************
UNAUTHORIZED_USER = "User is not authorised"
UNAUTHORIZED_UTILITY = "User not authorised for utility"
INVALID_TOKEN = "User token is not valid"
TOKEN_EXPIRED = "This token is expired. please log in again to continue"
SUCCESSFUL_LOGIN = "User logged in successfully"
SUCCESSFUL_LOGOUT = "User logged out successfully"
SUCCESSFULLY_DATA_SAVE = 'Data has been saved successfully.'
SUCCESSFULLY_DATA_DELETED = 'Data has been deleted successfully.'
SUCCESSFULLY_DATA_RETRIEVE = 'Data has been retrieved successfully.'
SUCCESSFULLY_DATA_UPDATED = 'Data has been updated successfully.'
DATA_ALREADY_DELETE = 'Data already deleted.'
DATA_ALREADY_EXISTS = 'Data already exists.'
DATA_NOT_EXISTS = 'Data not exists.'
AUTODISCOVER_STARTED_SUCCESSFULLY = 'Autodiscover started successfully'
INVALID_DATA = 'Invalid data provided, data could not save.'
FAIL = 'fail'
EXIST = 'exist'
USER_ALREADY_EXIST = 'User all ready exit with this name.'
SERVER_ERROR = 'Server error occurred {0}'
INVALID_CREDENTIALS = 'Provided credentials are wrong.'
SUCCESS = 'success'
EXCEPTION = 'exception'
UNAUTHORIZED = 'Unauthorized'

# *********** USER CUSTOM CONSTANTS **************
BANK_ALREADY_EXISTS = 'Bank detail already exists for specified user'
BANK_NOT_FOUND = 'Bank detail not found for specified user.'
ROLE_PRIVILEGE_NOT_FOUND = 'No Privileges attached to role.'
USER_PRIVILEGE_NOT_FOUND = 'No Privileges assigned to user.'
PRIVILEGE_NOT_FOUND = 'No Privileges found.'
USER_NOT_FOUND = 'User not found.'
ID_STRING_NOT_FOUND = 'Id string not found.'
ROLES_NOT_FOUND = 'No roles found.'
PRIVILEGE_DELETED = 'Privileges deleted successfully.'
ROLES_DELETED = 'User Roles deleted successfully.'
ROLES_NOT_ASSIGNED = 'No roles assigned to user.'
AREA_NOT_ASSIGNED = 'No areas assigned to user.'
SKILL_NOT_ASSIGNED = 'No skills assigned to user.'
UTILITY_NOT_ASSIGNED = 'No utilities assigned to user.'
NO_NOTES_NOT_FOUND = 'No notes found for user.'
NOTES_NOT_FOUND = 'Note not found.'
NO_DOCUMENT_NOT_FOUND = 'No Documents found for user.'
DOCUMENT_NOT_FOUND = 'Document not found.'
UTILITY_NOT_FOUND="Utility not found"
TENANT_NOT_FOUND="Tenant not found."
DOCUMENT_TYPE_NOT_FOUND="No record found for user document type"
SERVICE_TYPE_NOT_FOUND="No record found for user service type"
UTILITY_NOT_FOUND = "Utility not found"
DOCUMENT_TYPE_NOT_FOUND = "No record found for user document type"
SERVICE_TYPE_NOT_FOUND = "No record found for user service type"
MOBILE_ALREADY_EXISTS = "Mobile number already exists!"
CONTRACT_ALREADY_EXISTS = "Contract already exists"


# *********** NOT FOUND CONSTANTS **************
COUNTRY_NOT_FOUND = "Country Not Found"
STATE_NOT_FOUND = "State Not Found"
CITY_NOT_FOUND = "City Not Found"
STATUS_NOT_FOUND = "Status Not Found"
MODULE_NOT_FOUND = "Module Not Found"
SUBMODULE_NOT_FOUND = "SubModule Not Found"
SUBSCRIPTION_NOT_FOUND = "Subscription Not Found"
SUBSCRIPTION_PLAN_NOT_FOUND = "Subscription Plan Not Found"
SUBSCRIPTION_RATE_NOT_FOUND = "Subscription Rate Not Found"
BANK_NOT_FOUND_FOR_USER = "Bank Detail Not Found For User"
INVOICE_NOT_FOUND = "Invoice Not Found"
REGISTRATION_NOT_FOUND = "Registration not found"
PAYMENT_NOT_FOUND = "Payment not found"
BILL_NOT_FOUND = "Bill not found"
CONSUMER_NOT_FOUND = "Consumer not found"
COMPLAINT_NOT_FOUND = "Complaint not found"
SCHEME_NOT_FOUND = "Scheme not found"
CONTRACT_TYPE_NOT_FOUND = "Contract Type not found"
CONTRACT_PERIOD_NOT_FOUND = "Contract Period not found"
CONTRACT_SUBTYPE_NOT_FOUND = "Contract SubType not found"
TERMS_AND_CONDITION_NOT_FOUND = "Terms and condition not found"
SUPPLIER_TYPE_NOT_FOUND = "Contract Type not found"
SUPPLIER_SUBTYPE_NOT_FOUND = "Contract SubType not found"
PRODUCT_CATEGORY_NOT_FOUND = "Product Category not found"
PRODUCT_SUBCATEGORY_NOT_FOUND = "Product SubCategory not found"
CONTRACT_NOT_FOUND = "Contract not found"
STORE_TYPE_NOT_FOUND = "Store type not found"
STORE_LOCATION_NOT_FOUND = "Store location not found"
UTILITY_SERVICE_CONTRACT_NOT_FOUND = "Utility service contract not found"

# *********** ALREADY EXIST CONSTANTS **************
NAME_ALREADY_EXIST = "Name Already Exist"
ACCOUNT_NO_ALREADY_EXIST = "Account Number Already Exist"
INVOICE_ALREADY_EXIST = "Invoice Already Exist"
MODULE_ALREADY_EXIST = "Module Already Exist"
SUBMODULE_ALREADY_EXIST = "SubModule Already Exist"
SUBSCRIPTION_ALREADY_EXIST = "Subscription Already Exist"
TERMS_AND_CONDITION_ALREADY_EXIST = "Terms and Condition Already Exist"
REGION_ALREADY_EXIST = 'Region already exist'
COUNTRY_ALREADY_EXIST = "Country Already Exist"
STATE_ALREADY_EXIST = "State Already Exist"
CITY_ALREADY_EXIST = "City Already Exist"
AREA_ALREADY_EXIST = "Area Already Exist"
SUBAREA_ALREADY_EXIST = "SubArea Already Exist"
PREMISE_ALREADY_EXIST = "Premise Already Exist"
SKILL_ALREADY_EXIST = "Skill Already Exist"
CAMPAIGNSUBTYPE_ALREADY_EXIST = "Campaign Subtype Already Exist"
CAMPAIGN_TYPE_ALREADY_EXIST = "Campaign Type Already Exist"
NUMFORMAT_ALREADY_EXIST = "NumFormat with selected Sub Module Already Exist"
ADVERTISEMENT_TYPE_ALREADY_EXIST = "Advertisement with given type already exist"
ADVERTISEMENT_SUBTYPE_ALREADY_EXIST = "Advertisement with given type and subtype already exist"
SURVEY_TYPE_ALREADY_EXIST = "Survey Type already exist"
SURVEY_SUBTYPE_ALREADY_EXIST = "Survey Subtype already exist"
SURVEY_OBJECTIVE_ALREADY_EXIST = "Survey Objective already exist"
REGISTRATION_TYPE_ALREADY_EXIST = "Registration Type Already Exist"
REGISTRATION_SUBTYPE_ALREADY_EXIST = "Registration Subtype Already Exist"
CHANNEL_ALREADY_EXIST = "Channel Already Exist"
COSUMER_CATEGORY_ALREADY_EXIST = "Consumer Category Already Exist"
COSUMER_SUBCATEGORY_ALREADY_EXIST = "Consumer SubCategory Already Exist"
COSUMER_OWNERSHIP_ALREADY_EXIST = "Consumer OwnerShip Already Exist"
COSUMER_CONSENT_ALREADY_EXIST = "Consumer Consent Already Exist"
COSUMER_SUPPORT_ALREADY_EXIST = "Consumer Support Already Exist"
CONSUMER_FAQ_ALREADY_EXIST = "Consumer FAQ Already Exist"
PAYMENT_TYPE_ALREADY_EXIST = "Payment Type Alreday Exist"
PAYMENT_SUBTYPE_ALREADY_EXIST = "Payment SubType Alreday Exist"
PAYMENT_MODE_ALREADY_EXIST = "Payment Mode Already Exist"
COMPLAINT_TYPE_ALREADY_EXIST = "Complaint Type Already Exist"
COMPLAINT_SUBTYPE_ALREADY_EXIST = "Complaint Subtype Already Exist"
SERVICE_TYPE_ALREADY_EXIST = "Service Type Already Exist"
SERVICE_SUBTYPE_ALREADY_EXIST = "Service Subtype Already Exist"
ZONE_ALREADY_EXIST = "Zone Already Exist"



