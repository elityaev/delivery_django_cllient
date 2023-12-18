import uuid

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        primary_key=True,
        editable=False
    )
    username = None
    email = models.EmailField(_("email address"),
                              blank=True,
                              unique=True
                              )
    USERNAME_FIELD = 'email'
    objects = CustomUserManager()

    REQUIRED_FIELDS = ['first_name']


class Client(User):
    name = models.CharField(verbose_name='Имя',
                            max_length=40,
                            )
    phone = models.CharField(verbose_name='Телефон',
                             default=None,
                             null=True,
                             max_length=12)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'