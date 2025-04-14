from django.urls import path
from . import views

urlpatterns = [
    path('servicios/', views.ServicioListView.as_view(), name='servicio-list'),
    path('servicios/<int:pk>/', views.ServicioDetailView.as_view(), name='servicio-detail'),
    path('detalles-servicio/', views.DetalleServicioListView.as_view(), name='detalle-servicio-list'),
    path('detalles-servicio/<int:pk>/', views.DetalleServicioDetailView.as_view(), name='detalle-servicio-detail'),
]
