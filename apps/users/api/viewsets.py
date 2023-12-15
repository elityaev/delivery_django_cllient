from djoser import signals
from djoser.compat import get_user_email
from djoser.conf import settings
from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


from apps.users.api.serializers import ClientCreateSerializer
from apps.users.models import User
from apps.users.utils import create_client


class CustomUserViewSet(UserViewSet, viewsets.ModelViewSet):
    """
    Использует класс djoser действий с объектами пользователя,
    в т.ч. для регистрации, авторизации и аутентификации.

    При регистрации создается токен пользователя.
    """

    serializer_class = ClientCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        create_client(request, serializer)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer, *args, **kwargs):
        user = User.objects.get(email__iexact=serializer.data['email'])
        Token.objects.get_or_create(user=user)
        signals.user_registered.send(
            sender=self.__class__, user=user, request=self.request
        )

        context = {"user": user}
        to = [get_user_email(user)]
        if settings.SEND_ACTIVATION_EMAIL:
            settings.EMAIL.activation(self.request, context).send(to)
        elif settings.SEND_CONFIRMATION_EMAIL:
            settings.EMAIL.confirmation(self.request, context).send(to)
