from django.db import models


class PremiumSettings(models.Model):
    authentication = models.BooleanField(default=False)


class Site(models.Model):
    owner = models.ForeignKey("authorization.User", on_delete=models.CASCADE)
    subdomain = models.SlugField(allow_unicode=True)
    premium = models.ForeignKey("PremiumSettings", on_delete=models.CASCADE)
    description = models.TextField()
    template_name = models.CharField(max_length=255, default="default")
    public = models.BooleanField(default=True)

