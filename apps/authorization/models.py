from django.contrib.auth.models import AbstractUser
from django.db import models


class NotificationsSettings(models.Model):
    need_notifications = models.BooleanField(default=False)
    vk_need_notifications = models.BooleanField(default=False)
    tg_need_notifications = models.BooleanField(default=False)
    # Подробные настройки уведомлений
    buy_notifications = models.BooleanField(default=False)  # Уведомления о покупках
    add_card_notifications = models.BooleanField(default=False)  # Уведомления о добавлениях в корзину
    add_favorites_notifications = models.BooleanField(default=False)  # Уведомления о добавлениях в избранное
    service_news_notifications = models.BooleanField(default=False)  # Уведомления об изменениях в сервисе
    new_product_notifications = models.BooleanField(default=False)  # Уведомления о добавлении нового товара на сайты
    about_account_notifications = models.BooleanField(default=False)  # Уведомления об изменениях в аккаунте
    recommendations_notifications = models.BooleanField(default=False)  # Рекоммендации по настройке аккаунта


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


class EmailConfirmation(models.Model):
    check_token = models.CharField(max_length=255)
    uuid_url = models.UUIDField()


class User(AbstractUser):
    subdomain = models.CharField(max_length=255, blank=True)
    username = models.CharField(max_length=255)
    roles = models.ManyToManyField(Roles)

    email_confirmation = models.ForeignKey(to=EmailConfirmation, on_delete=models.SET_NULL, blank=True, null=True)
    notifications_settings = models.ForeignKey(to=NotificationsSettings, on_delete=models.CASCADE, blank=True)

    balance = models.DecimalField(max_digits=19, decimal_places=4, default=0.0)
    tg_account = models.ForeignKey(TGConnect, on_delete=models.CASCADE)
    vk_account = models.ForeignKey(VKConnect, on_delete=models.CASCADE)

    USERNAME_FIELD = 'username'

    class Meta:
        unique_together = ("subdomain", "username")
