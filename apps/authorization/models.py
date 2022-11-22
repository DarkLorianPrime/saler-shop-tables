from django.contrib.auth.models import AbstractUser
from django.db import models


class ProfileSettings(models.Model):
    email_news = models.BooleanField(default=False)
    email_important = models.BooleanField(default=True)


class User(AbstractUser):
    Roles = (
        ("owner", "Subdomain owner"),
        ("admin", "Subdomain admin"),
        ("user", "Subdomain user"),
        ("not_domain_user", "User")
    )
    subdomain = models.CharField(max_length=255, blank=True)
    username = models.CharField(max_length=255)
    profile_settings = models.ForeignKey(to=ProfileSettings, on_delete=models.CASCADE, related_name="user_settings", blank=True)
    role = models.CharField(choices=Roles, max_length=15)
    USERNAME_FIELD = 'username'
    balance = models.DecimalField(max_digits=19, decimal_places=4, default=0.0)

    class Meta:
        unique_together = ("subdomain", "username")
