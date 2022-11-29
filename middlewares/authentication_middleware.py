from django.contrib.auth.middleware import get_user
from django.utils.deprecation import MiddlewareMixin
from rest_framework.exceptions import PermissionDenied

from customjwt.authorization import CustomAuthorizationBackend, authenticate
from customjwt.jwthandler import CustomJWTAuthentication


class AuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user = CustomJWTAuthentication().authenticate(request)

        if user is None:
            return

        ACCESS_LIST = ["registration"]
        if (user[0].email and user[0].email_confirmation is None) or request.path.split("/")[-2] in ACCESS_LIST:
            request.user = user[0]
            return

        raise PermissionDenied(detail="You have no mail or it is not confirmed.", code=403)

