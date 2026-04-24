"""
URL configuration for abc_core project.

This module defines the root URL patterns for the application.

URL Configuration:
    The `urlpatterns` list routes URLs to views. Each path maps a URL pattern 
    to its corresponding view or includes sub-URL patterns from other apps.

    For more information:
    - https://docs.djangoproject.com/en/6.0/topics/http/urls/
    - https://docs.djangoproject.com/en/6.0/ref/urls/
"""

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.http import JsonResponse
from vn_docs.views import dashboard


def redirect_home(request):
    """Redirect root URL based on user authentication status.
    
    - Authenticated users: redirect to dashboard
    - Unauthenticated users: redirect to login page
    
    Args:
        request: HTTP request object
        
    Returns:
        HttpResponseRedirect: Redirect response
    """
    if not request.user.is_authenticated:
        return redirect('/auth/login/')
    return redirect('/auth/dashboard/staff/')


def health_check(request):
    """Health check endpoint for Docker/Kubernetes.
    
    Returns a simple JSON response to indicate the service is alive.
    
    Args:
        request: HTTP request object
        
    Returns:
        JsonResponse: JSON response with status OK
    """
    return JsonResponse({'status': 'ok'}, status=200)


urlpatterns = [
    # Health check for Docker/Kubernetes
    path('health/', health_check, name='health'),
    
    # Root URL - redirects based on auth status
    path('', redirect_home, name='home'),
    
    # Django admin interface
    path('admin/', admin.site.urls),
    
    # Dashboard view
    path('dashboard/', dashboard, name='dashboard'),
    
    # User authentication URLs (login, logout, password reset, etc.)
    path('auth/', include('vn_users.urls')),
]

