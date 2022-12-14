from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from customjwt.jwthandler import CustomJWTAuthentication


class AuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        try:
            user = CustomJWTAuthentication().authenticate(request)
        except AuthenticationFailed:
            return HttpResponse("Unauthorized", status=401)

        if user is None:
            return

        ACCESS_LIST = ["registration"]
        if (user[0].email and user[0].email_confirmation is None) or request.path.split("/")[-2] in ACCESS_LIST:
            request.user = user[0]
            return

        raise PermissionDenied(detail="You have no mail or it is not confirmed.", code=403)

