from django.conf.global_settings import DEFAULT_FROM_EMAIL
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from djoser import email, utils
from djoser.conf import settings

from apps.users.models import Client, User


def create_client(request, serializer):
    client = Client.objects.create_user(
        email=serializer.data['email'],
        name=serializer.data['name'],
        phone=serializer.data['phone'],
        is_active=False
    )
    client.set_password(request.data['password'])
    client.save()


class ActivationEmail(email.ActivationEmail):
    template_name = 'users/activation.html'

    def get_context_data(self):
        context = super().get_context_data()
        user = context.get("user")
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.ACTIVATION_URL.format(**context)
        return context