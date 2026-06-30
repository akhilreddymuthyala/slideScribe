from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('create/', views.create_presentation, name='create_presentation'),
    path('<int:pk>/', views.presentation_detail, name='presentation_detail'),
    path('<int:pk>/delete/', views.delete_presentation, name='delete_presentation'),
]