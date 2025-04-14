from django.urls import path
from . import views

urlpatterns = [
    path('carrusel/', views.CarruselInicioListCreateView.as_view(), name='carrusel-list-create'),
    path('carrusel/<int:pk>/', views.CarruselInicioRetrieveUpdateDestroyView.as_view(), name='carrusel-detail'),
]
