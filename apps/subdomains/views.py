from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN
from rest_framework.viewsets import ModelViewSet

from apps.authorization.models import Roles
from apps.subdomains.models import Site
from apps.subdomains.serializers import SubdomainsSerializer, SiteInformationSerializer, PremiumSettingsSerializer
from apps.subdomains.responses import Messages


class SubdomainController(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Site.objects.all()

    def list(self, request, *args, **kwargs):
        sites = Site.objects.filter(owner=request.user)
        serialize = SiteInformationSerializer(sites, many=True).data
        return Response(serialize)

    def create(self, request, *args, **kwargs):
        serialize = SubdomainsSerializer(data=request.POST, context={"user": request.user})
        serialize.is_valid(raise_exception=True)
        instance = serialize.save()

        return Response(SiteInformationSerializer(instance).data, status=HTTP_201_CREATED)

    def check_exists(self, request, *args, **kwargs):
        query = request.query_params

        if not query.get("subdomain"):
            return Response({"error": Messages.NOT_SUBDOMAIN_IN_QUERY}, status=HTTP_400_BAD_REQUEST)

        if Site.objects.filter(subdomain=query["subdomain"]).exists():
            return Response({"error": Messages.SUBDOMAIN_EXISTS}, status=HTTP_400_BAD_REQUEST)

        return Response({"response": Messages.SUBDOMAIN_NOT_EXISTS})

    def get_premium_settings(self, request, *args, **kwargs):
        query = request.query_params

        if not query.get("subdomain"):
            return Response({"error": Messages.NOT_SUBDOMAIN_IN_QUERY}, status=HTTP_400_BAD_REQUEST)

        if not (site := Site.objects.filter(subdomain=query["subdomain"])).exists():
            return Response({"error": Messages.SUBDOMAIN_NOT_EXISTS}, status=HTTP_400_BAD_REQUEST)

        one_site = site.first()
        if not Roles.objects.filter(user=request.user, user__roles__permission__gte=3).exists():
            if one_site.owner.id != request.user.id:
                return Response({"error": Messages.NOT_ACCESS_TO_SUBDOMAIN}, status=HTTP_403_FORBIDDEN)

        return Response({"response": PremiumSettingsSerializer(one_site.premium).data})

    def delegate_subdomain(self, request, *args, **kwargs):
        print(self.get_object())

    def get_subdomain(self, request, *args, **kwargs):
        return Response(SiteInformationSerializer(self.get_object()).data)
