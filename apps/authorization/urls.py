from django.urls import path

from apps.authorization import views
from rest_framework_simplejwt import views as jwt_views

from customjwt.tokens import CustomTokenObtainPairView

urlpatterns = [
    path("registration/", views.RegistrationViewSet.as_view({"post": "create"})),
    path("profile/", views.ProfileViewSet.as_view({"get": "receive", "patch": "update", "delete": "destroy"})),
    path("activate/<uuid:uuid_param>/<str:code>", views.ProfileViewSet.as_view({"get": "activate_email"})),
    path("activate/", views.ProfileViewSet.as_view({"get": "send_email"})),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path("social/", views.SocialViewSet.as_view({"post": "listen", "get": "get"})),
    path("settings/", views.SettingsViewSet.as_view({"get": "get_settings", "post": "update_settings"})),
    path("settings/check/", views.SettingsViewSet.as_view({"get": "check_possibility_update"}))
]
