from django.urls import path
from .views import nosotros_view

urlpatterns = [
    path('', nosotros_view, name='nosotros'),
]


