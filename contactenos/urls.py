from django.urls import path
from .views import contactenos_view

urlpatterns = [
    path('', contactenos_view, name='contactenos'),
]
