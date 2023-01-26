from rest_framework_simplejwt.views import TokenObtainPairView

from customjwt.token_serializers import CustomObtainSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    _serializer_class = "customjwt.token_serializers.CustomTokenObtainPairSerializer"


class CustomTokenRefreshView(TokenObtainPairView):
    _serializer_class = "customjwt.token_serializers.CustomTokenObtainPairSerializer"
