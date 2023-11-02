from django.contrib import admin
from django.urls import path,include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.views import serve

# Endpoint for swagger
schema_view = get_schema_view(
   openapi.Info(
      title="Documentacion Swagger para Django-Tasker",
      default_version='v1',
      description="Documentacion de Backend para Django-Tasker de Mario Gonzalez",
      license=openapi.License(name="BSD License"),
   ),
   public=True,
#    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
   
   # Path de Admin en Django
   path('admin/', admin.site.urls),
   
   # Paths del Core
   path('core/',include('apps.core.urls')),
   
   # Paths de Catalogos
   path('api/v1/',include('apps.tasks.urls')),
   
   # Paths de User
   path('api/v1/',include('apps.users.urls')),

   # Paths de Swagger
   path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),  # Registra el nombre de espacio 'rest_framework'

   # Path de favicon
   path('favicon.ico', serve, {'path': 'img/favicon.ico'}),

   # Path de API de Swagger
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('swagger/api/v1/user/login/', schema_view.with_ui('swagger', cache_timeout=0), name='rest_framework_login'),
   path('swagger/api/v1/user/logout/', schema_view.with_ui('swagger', cache_timeout=0), name='rest_framework_logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)