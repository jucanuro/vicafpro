from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('', include('inicio.urls')),
    path('', include('nosotros.urls')),
    path('', include('servicios.urls')),
    path('', include('clientes.urls')),
    path('', include('contactenos.urls')),
    path('bolsa-trabajo/', include('bolsa_trabajo.urls')), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
