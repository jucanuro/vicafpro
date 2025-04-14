from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_postulaciones, name='lista_postulaciones'),
    path('crear/', views.crear_postulacion, name='crear_postulacion'),
    path('<int:id>/', views.detalle_postulacion, name='detalle_postulacion'),
     path('oportunidades/', views.lista_oportunidades, name='lista_oportunidades'),
    path('oportunidad/crear/', views.crear_oportunidad, name='crear_oportunidad'),
    path('oportunidad/<int:id>/', views.detalle_oportunidad, name='detalle_oportunidad'),
]
