from django.contrib import admin
from django.urls import path, include, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from delivery_client import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.users.urls'))
]


if settings.ENV_NAME not in ['production', 'production_testing']:
    urlpatterns.append(
        path('schema/', SpectacularAPIView.as_view(), name='schema'),
    )
    urlpatterns.append(
        path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger')
    )

