from django.contrib import admin

from apps.notification.models import Notification, NotificationUser, UserFCMToken


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    pass


@admin.register(NotificationUser)
class NotificationUserAdmin(admin.ModelAdmin):
    pass


@admin.register(UserFCMToken)
class UserFCMTokenAdmin(admin.ModelAdmin):
    pass