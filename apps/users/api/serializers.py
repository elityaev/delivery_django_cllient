from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.settings import api_settings

from apps.users.models import Client, User


class ClientCreateSerializer(ModelSerializer):
    """Сериализатор клиента"""

    name = serializers.CharField(
        label='Имя',
        min_length=2,
        max_length=40
    )
    email = serializers.EmailField()
    password = serializers.CharField(
        label='Пароль',
        max_length=128,
        min_length=8,
        write_only=True
    )
    confirm_password = serializers.CharField(
        label='Подтверждение пароля',
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = Client
        fields = ['name', 'email', 'phone', 'password',
                  'confirm_password']
        extra_kwargs = {
            'email': {'required': True, 'allow_blank': False}
        }

    def to_internal_value(self, data):
        """Если пользователь зарегистрирован, но не верифицировал почту и пытается зарегистрироваться повторно,
         то он будет удален, входящие данные будут переданы для создания новой записи.
         """

        user = User.objects.filter(email=data['email']).first()
        if user:
            if user.is_active:
                raise serializers.ValidationError({'email': ['Пользователь с таким email уже зарегистрирован']})
            user.delete()
        return super(ClientCreateSerializer, self).to_internal_value(data)

    def validate(self, attrs):
        """Валидатор пароля"""

        confirm_password = attrs.pop('confirm_password')
        if attrs['password'] != confirm_password:
            raise serializers.ValidationError({'confirm_password': 'Пароли не совпадают'})

        client = Client(**attrs)
        password = attrs.get("password")

        try:
            validate_password(password, client)
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializer_error[api_settings.NON_FIELD_ERRORS_KEY]}
            )

        return attrs
