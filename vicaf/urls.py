from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('inicio.urls')),
    path('', include('nosotros.urls')),
    path('trabajadores/', include('trabajadores.urls', namespace='trabajadores')),
    path('servicios/', include('servicios.urls', namespace='servicios')),
    path('clientes/', include('clientes.urls', namespace='clientes')),
    path('', include('contactenos.urls')),
    path('proyectos/', include('proyectos.urls',namespace='proyectos')),
    path('bolsa-trabajo/', include('bolsa_trabajo.urls')), 
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
