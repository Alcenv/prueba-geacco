from django.contrib import admin
from django.urls import path, include
from .views import index
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('api/', include('api.urls')),  # Todas las rutas de la API se manejarán en api/urls.py
]