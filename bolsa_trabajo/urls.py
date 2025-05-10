from django.urls import path
from . import views

app_name = 'bolsa_trabajo'

urlpatterns = [
    path('', views.lista_oportunidades, name='listar'),
   path('postular/<int:oportunidad_id>/', views.postular, name='postular')
]
