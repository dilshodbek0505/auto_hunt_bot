from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from apps.common.models import BaseModel

User = get_user_model()


class Notification(BaseModel):
    title = models.CharField(max_length=255, help_text=_("Title of notification"))
    message = models.TextField(help_text=_("Message of notification"))
    is_for_everyone = models.BooleanField(default=False)
    users = models.ManyToManyField(User, verbose_name=_("Users"), blank=True)

    class Meta:
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")

    def __str__(self):
        return self.title


class NotificationUser(BaseModel):
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE)
    is_sent = models.BooleanField(default=False, help_text=_("Is this notification user sent?"))
    is_read = models.BooleanField(default=False, help_text=_("Is this notification user readable?"))
    sent_time = models.DateTimeField(verbose_name=_("Sent time"), null=True, blank=True)
    notification = models.ForeignKey(Notification, on_delete=models.PROTECT, related_name='notification_users', verbose_name=_("Notification"))

    class Meta:
        verbose_name = _("Notification user")
        verbose_name_plural = _("Notification users")

    def __str__(self):
        return f"{self.user.username} - {self.is_read}"


class UserFCMToken(BaseModel):
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE, related_name='fcm_token')
    token = models.CharField(max_length=255, verbose_name=_("Token"), unique=True)

    class Meta:
        verbose_name = _("User FCM Token")
        verbose_name_plural = _("User FCM Tokens")

    def __str__(self):
        return f"{self.created_at.timestamp()}"





