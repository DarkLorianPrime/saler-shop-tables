from django.http import HttpResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

from apps.authorization.models import User, EmailConfirmation
from apps.authorization.responses import Messages
from apps.authorization.serializers import UserSerializer, ProfileSerializer, SocialSerializer, NotificationsSerializer
from apps.authorization.utils import send_letter
from core import settings
from lib.methods_handler import TgMethods, VkMethods


class RegistrationViewSet(ModelViewSet):
    serializer_class = UserSerializer

    def create(self, request, subdomain: str = "", *args, **kwargs):
        serializer = self.serializer_class(data=request.POST, context={"subdomain": subdomain})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        return Response(ProfileSerializer(instance).data, status=status.HTTP_201_CREATED)


class ProfileViewSet(ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = User.objects.all()
    ALLOWED_METHODS = ["activate_email"]

    def get_permissions(self):
        return [AllowAny()] if self.action in self.ALLOWED_METHODS else [IsAuthenticated()]

    def receive(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def activate_email(self, request, *args, **kwargs):
        instance = EmailConfirmation.objects.filter(uuid_url=kwargs["uuid_param"], check_token=kwargs["code"])
        if instance.exists():
            instance.delete()
            return Response({"response": "ok"})

        return Response({"response": Messages.NOT_CODE}, status=status.HTTP_404_NOT_FOUND)

    def send_email(self, request, *args, **kwargs):
        instance = request.user
        if instance.email_confirmation is not None:
            code = instance.email_confirmation.check_token
            uuid = instance.email_confirmation.uuid_url
            send_letter("Окончание регистрации", f"{settings.DOMAIN}activate/{uuid}/{code}", [instance.email])
            return Response({"response": Messages.CHECK_EMAIL})

        return Response({"response": Messages.ALREADY_CONFIRMATION})


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
                VkMethods().messages.send(peer_id=user, message=Messages.NOT_TOKEN)
                return HttpResponse('ok')

            instance = user_instance.first()
            instance.vk_account.need_confirmation = False
            instance.vk_account.vk_id = user

            VkMethods().messages.send(peer_id=user, message=Messages.TOKEN_FOUND_USERNAME.format(instance.username))

        if data.get("message"):
            text = data["message"]["text"]
            user = data["message"]["from"]["id"]
            user_instance = User.objects.filter(tg_account__check_token=text)

            if not user_instance.exists():
                TgMethods().sendMessage(chat_id=user, text=Messages.NOT_TOKEN)
                return HttpResponse('ok')

            instance = user_instance.first()
            instance.tg_account.need_confirmation = False
            instance.tg_account.telegram_id = user

            TgMethods().sendMessage(chat_id=user, text=Messages.TOKEN_FOUND_USERNAME.format(instance.username))

        return HttpResponse('ok')


class SettingsViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def get_settings(self, request, *args, **kwargs):
        query = request.query_params
        user = request.user

        match query.get("action", "global"):
            case "notifications":
                serializer = NotificationsSerializer(user.notifications_settings)
                return Response(serializer.data)

        return Response({"error": Messages.NOT_FOUND_SETTINGS}, status=status.HTTP_400_BAD_REQUEST)

    def update_settings(self, request, *args, **kwargs):
        query = request.query_params
        user = request.user

        match query.get("action", "global"):
            case "notifications":
                serializer = NotificationsSerializer(user.notifications_settings, data=request.data,
                                                     context={"user": user})
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)

        return Response({"error": Messages.NOT_FOUND_SETTINGS}, status=status.HTTP_400_BAD_REQUEST)

    def check_possibility_update(self, request, *args, **kwargs):
        query = request.query_params
        user = request.user

        match query.get("action", "global"):
            case "notifications":
                perm = not (user.need_email and user.vk_account.need_confirmation and user.tg_account.need_confirmation)
                return Response({"response": perm})
