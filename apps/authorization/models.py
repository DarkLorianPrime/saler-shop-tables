from django.contrib.auth.models import AbstractUser
from django.db import models


class ProfileSettings(models.Model):
    email_news = models.BooleanField(default=False)
    email_important = models.BooleanField(default=True)


class Roles(models.Model):
    name = models.CharField(max_length=255)
    permission = models.IntegerField()


class TGConnect(models.Model):
    telegram_id = models.CharField(max_length=255, blank=True)
    need_confirmation = models.BooleanField(default=True)
    check_token = models.CharField(max_length=255)


class VKConnect(models.Model):
    vk_id = models.CharField(max_length=255, blank=True)
    need_confirmation = models.BooleanField(default=True)
    check_token = models.CharField(max_length=255)


class User(AbstractUser):
    subdomain = models.CharField(max_length=255, blank=True)
    username = models.CharField(max_length=255)
    profile_settings = models.ForeignKey(to=ProfileSettings, on_delete=models.CASCADE, related_name="user_settings", blank=True)
    role = models.ManyToManyField(Roles)
    need_email = models.BooleanField(default=True)
    balance = models.DecimalField(max_digits=19, decimal_places=4, default=0.0)
    tg_account = models.ForeignKey(TGConnect, on_delete=models.CASCADE)
    vk_account = models.ForeignKey(VKConnect, on_delete=models.CASCADE)

    USERNAME_FIELD = 'username'

    class Meta:
        unique_together = ("subdomain", "username")
