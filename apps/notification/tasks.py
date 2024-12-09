from apps.notification.utils import send_push_notification
from core.celery import app
from apps.notification.models import NotificationUser, UserFCMToken, Notification


@app.task
def send_notification(user_notification_ids: list, notification_id: int) -> str:
    notification = Notification.objects.get(id=notification_id)
    NotificationUser.objects.filter(id__in=user_notification_ids).values_list('user', flat=True)
    user_tokens = UserFCMToken.objects.filter(user_id__in=user_notification_ids)
    for user_token in user_tokens:
        send_push_notification(token=user_token.token, title=notification.title, message=notification.message)

    return 'success'
