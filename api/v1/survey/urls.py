from django.urls import path
from v1.survey.views.survey import SurveyList,SurveyDetail,Survey
from v1.survey.views.consumers import ConsumerDetail,ConsumerList,Consumers
from v1.survey.views.survey_type import SurveyTypeList,SurveyTypeDetail
from v1.survey.views.survey_status import SurveyStatusList,SurveyStatusDetail
from v1.survey.views.survey_objective import SurveyObjectiveList,SurveyObjectiveDetail

urlpatterns = [
    path('list', SurveyList.as_view(),name="survey_list"),
    path('', Survey.as_view(), name="Survey"),
    path('<uuid:id_string>', SurveyDetail.as_view(),name="survey_detail"),

    path('<uuid:id_string>/consumers-list', ConsumerList.as_view(), name="survey_consumer_list"),
    path('<uuid:id_string>/consumers', Consumers.as_view(), name="Consumers"),
    path('consumer/<uuid:id_string>', ConsumerDetail.as_view(),name="survey_consumer_detail"),

    path('type/list', SurveyTypeList.as_view(),name="survey_type_list"),
    path('type/<uuid:id_string>/', SurveyTypeDetail.as_view(),name="survey_type_detail"),
    path('status/list', SurveyStatusList.as_view(),name="survey_status_list"),
    path('status/<uuid:id_string>/', SurveyStatusDetail.as_view(),name="survey_status_detail"),
    path('objective/list', SurveyObjectiveList.as_view(),name="survey_objective_list"),
    path('objective/<uuid:id_string>/', SurveyObjectiveDetail.as_view(),name="survey_objective_detail"),
]