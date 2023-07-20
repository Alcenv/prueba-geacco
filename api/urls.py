from django.urls import path, include
from .views import GenerarDocumentoView, ConfigurarTareaView, CreateUserView, SecuenciaTareaViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'secuencias', SecuenciaTareaViewSet)

urlpatterns = [
    path('generar-documento/', GenerarDocumentoView.as_view(), name='generar-documento'),
    path('configurar-tarea/', ConfigurarTareaView.as_view(), name='configurar-tarea'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('create-user/', CreateUserView.as_view(), name='create-user'),
    path('', include(router.urls)),  # Incluye todas las rutas generadas automáticamente por el router
]
