from rest_framework import serializers

from apps.notification.models import UserFCMToken, Notification, NotificationUser


class FCMTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFCMToken
        fields = ('token', 'user')
        extra_kwargs = {'user': {'required': False}}


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('title', 'message')


class NotificationUserSerializer(serializers.ModelSerializer):
    notification = NotificationSerializer()

    class Meta:
        model = NotificationUser
        fields = ('id', 'is_read', 'created_at', 'sent_time', 'notification')