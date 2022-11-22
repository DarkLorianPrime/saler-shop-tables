from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.viewsets import ModelViewSet, ViewSet

from apps.authorization.serializers import UserSerializer

class RegistrationViewSet(ModelViewSet):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.POST, context={"request": request})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        return Response({"response": instance.data}, status=HTTP_201_CREATED)


class ProfileViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response({"response": serializer.data})
