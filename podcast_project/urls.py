from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from accounts.views import CustomRegisterView
from dj_rest_auth.registration.views import VerifyEmailView

schema_view = get_schema_view(
        openapi.Info(
            title='Growth table Api',
            default_version='v1',
            description='Api documentation for the Growth table Podcast',
            contact=openapi.Contact(email='isaiahjuniorp@gmail.com'),),
            public=True,
            permission_classes=[permissions.AllowAny],
            )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('podcast.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/dj-rest-auth/', include('dj_rest_auth.urls')),
   # path('api/v1/dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
   path('api/v1/dj-rest-auth/registration/', CustomRegisterView.as_view(), name='rest_register'),
   path('api/v1/dj-rest-auth/account-confirm-email/', VerifyEmailView.as_view(), name='account_confirm_email'),
    path('swagger-docs/',schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
