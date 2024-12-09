from django.urls import path

from apps.notification.views import RegisterFcmToken, NotificationUserDetail, UserNotificationExist, \
    NotificationUserList, FirebaseConfigView

app_name = 'notification'


urlpatterns = [
    path('register-fcm-token/', RegisterFcmToken.as_view(), name='register-fcm-token'),
    path('user-notification/', NotificationUserList.as_view(), name='user-notification-list'),
    path('user-notification/<int:pk>/', NotificationUserDetail.as_view(), name='user-notification-detail'),
    path('user-notification-exist/', UserNotificationExist.as_view(), name='user-notification-exist'),

    path('firebase-config/', FirebaseConfigView.as_view(), name='firebase-config'),
]