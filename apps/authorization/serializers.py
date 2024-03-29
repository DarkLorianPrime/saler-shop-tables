import random
import string
import uuid

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, Serializer

from apps.authorization.models import User, TGConnect, VKConnect, NotificationsSettings, EmailConfirmation
from apps.authorization.responses import Messages
from apps.authorization.utils import send_letter
from core import settings


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("password", "username", "email", "first_name", "last_name")

    def create(self, validated_data):
        validated_data["subdomain"] = self.context["subdomain"]
        subdomain = validated_data["subdomain"]

        if User.objects.filter(subdomain=subdomain, username=validated_data["username"]).exists():
            raise ValidationError({"error": Messages.ACCOUNT_ALREADY_EXISTS})

        if email := validated_data.get("email"):
            if User.objects.filter(subdomain=subdomain, email=email).exists():
                raise ValidationError({"error": Messages.EMAIL_ALREADY_LINKED})

        chars = string.ascii_uppercase + string.digits
        token = ''.join(random.choice(chars) for _ in range(6))
        token_uuid = uuid.uuid4()
        validated_data["notifications_settings"] = NotificationsSettings.objects.create()
        validated_data["email_confirmation"] = EmailConfirmation.objects.create(check_token=token, uuid_url=token_uuid)
        validated_data["tg_account"] = TGConnect.objects.create(check_token=token)
        validated_data["vk_account"] = VKConnect.objects.create(check_token=token)

        return User.objects.create_user(**validated_data)


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "id", "email", "first_name", "last_name")
        extra_kwargs = {'username': {'required': False}}

    def update(self, instance, validated_data):
        if (email := validated_data.get("email")) is not None:
            if User.objects.filter(subdomain='', email=email).exists():
                raise ValidationError({"error": Messages.EMAIL_ALREADY_LINKED})

            code = instance.email_confirmation.check_token
            uuid = instance.email_confirmation.uuid_url
            send_letter("Окончание регистрации", f"{settings.DOMAIN}activate/{uuid}/{code}", [email])

        if validated_data.get("username") is not None:
            del validated_data["username"]

        return super().update(instance, validated_data)


class SocialSerializer(Serializer):
    telegram_id = serializers.CharField(max_length=255, required=False)
    vk_id = serializers.CharField(max_length=255, required=False)
    need_confirmation = serializers.BooleanField(default=True)
    check_token = serializers.CharField(max_length=255)


class NotificationsSerializer(ModelSerializer):
    class Meta:
        model = NotificationsSettings
        fields = "__all__"

    def update(self, instance, validated_data):
        user = self.context["user"]
        if user.need_email and user.vk_account.need_confirmation and user.tg_account.need_confirmation:
            return instance

        super().update(instance, validated_data)
