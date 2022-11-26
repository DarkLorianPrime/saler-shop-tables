import random
import string

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, Serializer

from apps.authorization.models import User, ProfileSettings, TGConnect, VKConnect


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("password", "username", "email", "first_name", "last_name")

    def create(self, validated_data):
        validated_data["subdomain"] = self.context["subdomain"]
        subdomain = validated_data["subdomain"]
        if User.objects.filter(subdomain=subdomain, username=validated_data["username"]).exists():
            raise ValidationError({"error": "This account already exists."})

        if validated_data.get("email"):
            if User.objects.filter(subdomain=subdomain, email=validated_data["email"]).exists():
                raise ValidationError({"error": "This email already linked to other account."})

        validated_data["profile_settings"] = ProfileSettings.objects.create()
        chars = string.ascii_uppercase + string.digits
        confirm_token = ''.join(random.choice(chars) for _ in range(6))
        validated_data["tg_account"] = TGConnect.objects.create(check_token=confirm_token)
        validated_data["vk_account"] = VKConnect.objects.create(check_token=confirm_token)
        instance = User.objects.create_user(**validated_data)
        return instance


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "id", "email", "first_name", "last_name")


class SettingsSerializer(ModelSerializer):
    class Meta:
        model = ProfileSettings
        field = "__all__"


class SocialSerializer(Serializer):
    telegram_id = serializers.CharField(max_length=255, required=False)
    vk_id = serializers.CharField(max_length=255, required=False)
    need_confirmation = serializers.BooleanField(default=True)
    check_token = serializers.CharField(max_length=255)

    class Meta:
        model = VKConnect
        field = "__all__"
