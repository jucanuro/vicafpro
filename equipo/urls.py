from django.urls import path
from .views import (
    MiembroEquipoListCreateView,
    MiembroEquipoRetrieveUpdateDestroyView,
)

urlpatterns = [
    path('equipo/', MiembroEquipoListCreateView.as_view(), name='miembroequipo-list-create'),
    path('equipo/<int:pk>/', MiembroEquipoRetrieveUpdateDestroyView.as_view(), name='miembroequipo-detail'),
]
