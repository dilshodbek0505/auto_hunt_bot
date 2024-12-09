from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from apps.notification.models import Notification, NotificationUser
from apps.notification.tasks import send_notification

User = get_user_model()


@receiver(post_save, sender=Notification)
def create_notification(sender, instance, created, **kwargs):
    if created:
        if instance.is_for_everyone:
            instance.users.clear()
            user_notifications = [NotificationUser(user=user, notification=instance) for user in User.objects.all()]
            user_notifications_objs = NotificationUser.objects.bulk_create(user_notifications)
            user_notifications_ids = [notification_obj.id for notification_obj in user_notifications_objs]
            send_notification.delay(user_notifications_ids, instance.id)


@receiver(m2m_changed, sender=Notification.users.through)
def create_user_notification(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':
        user_notifications = [NotificationUser(user=user, notification=instance) for user in
                              User.objects.filter(pk__in=pk_set)]
        user_notifications_objs = NotificationUser.objects.bulk_create(user_notifications)
        user_notifications_ids = [notification_obj.id for notification_obj in user_notifications_objs]
        send_notification.delay(user_notifications_ids, instance.id)

