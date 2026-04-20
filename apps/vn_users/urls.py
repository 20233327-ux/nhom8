from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('dashboard/staff/', views.dashboard_staff, name='dashboard_staff'),
    path('dashboard/manager/', views.dashboard_manager, name='dashboard_manager'),
    path('dashboard/admin/', views.dashboard_admin, name='dashboard_admin'),
]
