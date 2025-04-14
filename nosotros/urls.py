from django.urls import path
from . import views

urlpatterns = [
    path('nosotros/', views.NosotrosListView.as_view(), name='nosotros_list'),
    path('nosotros/create/', views.NosotrosCreateView.as_view(), name='nosotros_create'),
    path('nosotros/<int:pk>/update/', views.NosotrosUpdateView.as_view(), name='nosotros_update'),
    path('nosotros/<int:pk>/delete/', views.NosotrosDeleteView.as_view(), name='nosotros_delete'),
]

