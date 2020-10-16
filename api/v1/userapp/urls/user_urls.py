from django.urls import path
from v1.userapp.views.document import UserDocument
from v1.userapp.views.login import LoginApiView, LogoutApiView
from v1.userapp.views.notes import UserNote
from v1.userapp.views.user import User, UserList, UserDetail
from v1.userapp.views.user_area import UserArea
from v1.userapp.views.user_bank import UserBankDetail
from v1.userapp.views.user_privilege import UserPrivilegeDetail
from v1.userapp.views.user_role import UserRole
from v1.userapp.views.user_skill import UserSkill
from v1.userapp.views.user_utility import UserUtility

urlpatterns = [
    path('', User.as_view(), name='create-user'),
    path('<uuid:id_string>', UserDetail.as_view()),
    path('list/', UserList.as_view()),

    path('<uuid:id_string>/bank/', UserBankDetail.as_view()),

    path('<uuid:id_string>/role/', UserRole.as_view()),

    path('<uuid:id_string>/privilege/', UserPrivilegeDetail.as_view()),

    path('<uuid:id_string>/note/', UserNote.as_view()),

    path('<uuid:id_string>/document/', UserDocument.as_view()),

    path('<uuid:id_string>/utility/', UserUtility.as_view()),

    path('<uuid:id_string>/area/', UserArea.as_view()),

    path('<uuid:id_string>/skill/', UserSkill.as_view()),

    path('login/', LoginApiView.as_view(), name='log-in'),

    path('logout/', LogoutApiView.as_view()),
]