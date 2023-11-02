from django.urls import path,include
from .api.routers import router

app_name = 'tasks_app'

urlpatterns = [
    # Router de la API
    path('', include(router.urls)),
]
