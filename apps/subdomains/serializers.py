from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from apps.subdomains.models import Site, PremiumSettings
from apps.subdomains.responses import Messages


class SubdomainsSerializer(ModelSerializer):
    class Meta:
        model = Site
        fields = ("subdomain", "description", "public")

    def validate(self, attrs):
        if Site.objects.filter(subdomain=attrs["subdomain"]):
            raise ValidationError({"error": Messages.SUBDOMAIN_EXISTS})

        attrs["owner_id"] = self.context["user"].id
        return attrs

    def create(self, validated_data):
        validated_data["premium"] = PremiumSettings.objects.create()
        return Site.objects.create(**validated_data)


class SiteInformationSerializer(ModelSerializer):
    class Meta:
        model = Site
        fields = ("id", "owner", "subdomain", "description", "template_name", "public", "premium")


class PremiumSettingsSerializer(ModelSerializer):
    class Meta:
        model = PremiumSettings
        fields = "__all__"
