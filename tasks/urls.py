from django.urls import path
from django.contrib.auth import views as auth_views # Import built-in auth views
from . import views

urlpatterns = [
    # Frontend HTML Routes
    path('', views.task_list, name='task_list'),
    
    # Auth Routes
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'), # <--- FIXED LINE
    path('reset-password/', views.reset_password, name='reset_password'),

    # Task CRUD Routes
    path('create/', views.task_create, name='task_create'),
    path('update/<int:pk>/', views.task_update, name='task_update'),
    path('delete/<int:pk>/', views.task_delete, name='task_delete'),
]