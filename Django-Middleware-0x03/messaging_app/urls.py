"""
URL configuration for messaging_app package.
"""

from django.urls import path, include

urlpatterns = [
    path('api/', include('chats.urls')),
]