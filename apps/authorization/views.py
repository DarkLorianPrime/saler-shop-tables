from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK
from rest_framework.viewsets import ModelViewSet, ViewSet

from apps.authorization.serializers import UserSerializer, ProfileSerializer


class RegistrationViewSet(ModelViewSet):
    serializer_class = UserSerializer

    def create(self, request, subdomain: str = "", *args, **kwargs):
        serializer = self.serializer_class(data=request.POST, context={"subdomain": subdomain})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        return Response(ProfileSerializer(instance).data, status=HTTP_201_CREATED)


class ProfileViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = ProfileSerializer

    def list(self, request, subdomain: str = "", *args, **kwargs):
        print(subdomain)
        serializer = self.serializer_class(request.user)
        return Response({"response": serializer.data}, status=HTTP_200_OK)
