from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_403_FORBIDDEN
from rest_framework.viewsets import ModelViewSet, ViewSet

from apps.authorization.models import User
from apps.authorization.serializers import UserSerializer, ProfileSerializer, SocialSerializer
from lib.methods_handler import TgMethods, VkMethods


class RegistrationViewSet(ModelViewSet):
    serializer_class = UserSerializer

    def create(self, request, subdomain: str = "", *args, **kwargs):
        serializer = self.serializer_class(data=request.POST, context={"subdomain": subdomain})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        return Response(ProfileSerializer(instance).data, status=HTTP_201_CREATED)


class ProfileViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    queryset = User.objects.all()

    def receive(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        if self.get_object().id == request.user.id:
            return super().update(request, *args, **kwargs)

        return Response({"detail": "You don`t have permission to change foreign profile."}, status=HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        if self.get_object().id == request.user.id:
            return super().destroy(request, *args, **kwargs)

        return Response({"detail": "You don`t have permission to delete foreign profile."}, status=HTTP_403_FORBIDDEN)


class SocialViewSet(ViewSet):
    ALLOWED_METHODS = ["listen"]

    def get_permissions(self):
        return [AllowAny()] if self.action in self.ALLOWED_METHODS else [IsAuthenticated()]

    def get(self, request, *args, **kwargs):
        user = request.user
        socials = SocialSerializer([user.tg_account, user.vk_account], many=True)
        return Response(socials.data)

    def listen(self, request, *args, **kwargs):
        data = request.data
        if data.get("object"):
            text = data["object"]['message']["text"]
            user = data["object"]["message"]["peer_id"]
            user_instance = User.objects.filter(vk_account__check_token=text)

            if not user_instance.exists():
                VkMethods().messages.send(peer_id=user, message="Token not found!\nTry again?")
                return HttpResponse('ok')

            instance = user_instance.first()
            instance.vk_account.need_confirmation = False
            instance.vk_account.vk_id = user

            VkMethods().messages.send(peer_id=user, message=f"Token found!\nConnected to user with username {instance.username}")

        if data.get("message"):
            text = data["message"]["text"]
            user = data["message"]["from"]["id"]
            user_instance = User.objects.filter(tg_account__check_token=text)

            if not user_instance.exists():
                TgMethods().sendMessage(chat_id=user, text="Token not found!\nTry again?")
                return HttpResponse('ok')

            instance = user_instance.first()
            instance.tg_account.need_confirmation = False
            instance.tg_account.telegram_id = user

            TgMethods().sendMessage(chat_id=user, text=f"Token found!\nConnected to user with username {instance.username}")

        return HttpResponse('ok')
