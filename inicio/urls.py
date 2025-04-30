from django.urls import path
from .views import inicio_view

urlpatterns = [
    path('', inicio_view, name='inicio'),
]
