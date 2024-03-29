from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
...

schema_view = get_schema_view(
   openapi.Info(
      title="Little lemon API",
      default_version='v1',
      description="Little lemon project using django rest framework",
    #   terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="akinolasamson1234@gmail.com"),
    #   license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('djoser.urls.authtoken')),
    path('auth/', include('authentication.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('api/', include('littleLemonAPI.urls')),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += staticfiles_urlpatterns()