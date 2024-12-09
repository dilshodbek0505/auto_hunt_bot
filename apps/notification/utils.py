from firebase_admin import messaging


def send_push_notification(token, title, message):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=message,
        ),
        token=token
    )

    messaging.send(message)
