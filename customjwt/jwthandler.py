from rest_framework_jwt.settings import api_settings
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken
from django.utils.translation import gettext_lazy as _

from customjwt.utils import get_subdomain


class CustomJWTAuthentication(JWTAuthentication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subdomain = None

    def authenticate(self, request):
        auth_data = super().authenticate(request)

        if auth_data is None:
            return None

        if auth_data[0] is None:
            return None

        self.subdomain = get_subdomain(request)
        if auth_data[0].subdomain != self.subdomain:
            raise AuthenticationFailed(_("User not found"), code="user_not_found")

        return auth_data
