from django.urls import path
from djoser.views import TokenCreateView, TokenDestroyView

from apps.users.api import viewsets


urlpatterns = [
    path('registration/', viewsets.CustomUserViewSet.as_view({'post':'create'}), name='user-create'),
    path('auth/activation/', viewsets.CustomUserViewSet.as_view({'post':'activation'}), name='user-activation'),
    path('auth/login/', TokenCreateView.as_view(), name='login'),
    path('auth/logout/', TokenDestroyView.as_view(), name='logout'),
]