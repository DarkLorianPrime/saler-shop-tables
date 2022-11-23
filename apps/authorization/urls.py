from django.urls import path

from apps.authorization import views
from rest_framework_simplejwt import views as jwt_views

from customjwt.tokens import CustomTokenObtainPairView

urlpatterns = [
    path("registration/", views.RegistrationViewSet.as_view({"post": "create"})),
    path("profile/", views.ProfileViewSet.as_view({"get": "list"})),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
