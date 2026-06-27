from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('auth/register/', views.register_view, name='register'),
    path('auth/login/', views.login_view, name='login'),
    path('auth/logout/', views.logout_view, name='logout'),
]