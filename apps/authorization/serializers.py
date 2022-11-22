from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from apps.authorization.models import User, ProfileSettings


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("password", "username", "email", "first_name", "last_name")

    def create(self, validated_data):
        validated_data["subdomain"] = self.context["request"].subdomain
        subdomain = validated_data["subdomain"]
        if User.objects.filter(subdomain=subdomain, username=validated_data["username"]).exists():
            raise ValidationError({"error": "This account already exists."})
        if validated_data.get("email"):
            if User.objects.filter(subdomain=subdomain, email=validated_data["email"]).exists():
                raise ValidationError({"error": "This email already linked to other account."})

        instance = User.objects.create_user(**validated_data)
        instance.ProfileSettings.objects.create()
        return


class ProfileSerializer(UserSerializer):
    class Meta:
        fields = ("username", "id", "email", "first_name", "last_name")


class SettingsSerializer(ModelSerializer):
    class Meta:
        model = ProfileSettings
        field = "__all__"

