from django.contrib import admin

from apps.users.models import User, Client

admin.site.register(User)
admin.site.register(Client)
