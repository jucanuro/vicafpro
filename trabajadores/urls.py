from django.urls import path
from .views import trabajadores_view

urlpatterns = [
    path('', trabajadores_view, name='trabajadores'),
]