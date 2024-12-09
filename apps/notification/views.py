from rest_framework.generics import CreateAPIView, RetrieveAPIView, get_object_or_404, ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.notification.models import UserFCMToken, NotificationUser
from apps.notification.serializers import FCMTokenSerializer, NotificationUserSerializer
from apps.notification.permissions import IsOwner

from django.views import View
from django.conf import settings
from django.http import JsonResponse



class RegisterFcmToken(CreateAPIView):
    serializer_class = FCMTokenSerializer
    permission_classes = (IsAuthenticated,)
    queryset = UserFCMToken.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class NotificationUserList(ListAPIView):
    serializer_class = NotificationUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return NotificationUser.objects.filter(user=self.request.user)


class NotificationUserDetail(RetrieveAPIView):
    queryset = NotificationUser.objects.all()
    serializer_class = NotificationUserSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_object(self):

        queryset = self.filter_queryset(self.get_queryset())

        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
                'Expected view %s to be called with a URL keyword argument '
                'named "%s". Fix your URL conf, or set the `.lookup_field` '
                'attribute on the view correctly.' %
                (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        self.check_object_permissions(self.request, obj)

        obj.is_read = True
        obj.save(update_fields=['is_read'])

        return obj


class UserNotificationExist(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        notification_count = NotificationUser.objects.filter(user=request.user, is_read=False).count()
        return Response(
            {'notification_exist': notification_count != 0,
             'notification_count': notification_count})



# view

class FirebaseConfigView(View):
    def get(self, request, *args, **kwargs):
        firebase_config = {
            "apiKey": settings.API_KEY,
            "authDomain": settings.AUTH_DOMAIN,
            "projectId": settings.PROJECT_ID,
            "storageBucket": settings.STORAGE_BUCKET,
            "messagingSenderId": settings.MESSAGING_SENDER_ID,
            "appId": settings.APP_ID,
            "measurementId": settings.MEASUREMENT_ID
        }

        return JsonResponse(firebase_config)
