#!/usr/bin/env python
"""
Test script to verify middleware configuration
"""
import os
import sys
import django
from django.test import RequestFactory
from django.contrib.auth import get_user_model
from django.http import HttpResponse

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'messaging_app.settings')
django.setup()

from chats.middleware import (
    RequestLoggingMiddleware, 
    RestrictAccessByTimeMiddleware, 
    RateLimitMiddleware, 
    RolepermissionMiddleware
)

def test_middleware_configuration():
    """Test that all middleware classes can be instantiated and called."""
    print("Testing middleware configuration...")
    
    # Create a simple get_response function
    def get_response(request):
        return HttpResponse("OK")
    
    # Test each middleware
    middlewares = [
        RequestLoggingMiddleware,
        RestrictAccessByTimeMiddleware,
        RateLimitMiddleware,
        RolepermissionMiddleware
    ]
    
    factory = RequestFactory()
    
    for middleware_class in middlewares:
        try:
            middleware = middleware_class(get_response)
            request = factory.get('/api/')
            response = middleware(request)
            print(f"✓ {middleware_class.__name__} - OK")
        except Exception as e:
            print(f"✗ {middleware_class.__name__} - ERROR: {str(e)}")
    
    print("\nMiddleware configuration test completed!")

def test_settings_import():
    """Test that settings can be imported and middleware is configured."""
    print("\nTesting settings import...")
    
    try:
        from django.conf import settings
        print(f"✓ Settings imported successfully")
        print(f"✓ MIDDLEWARE configured with {len(settings.MIDDLEWARE)} items")
        
        # Check if our custom middleware is in the list
        custom_middleware = [
            'chats.middleware.RequestLoggingMiddleware',
            'chats.middleware.RestrictAccessByTimeMiddleware',
            'chats.middleware.RateLimitMiddleware',
            'chats.middleware.RolepermissionMiddleware',
        ]
        
        for middleware in custom_middleware:
            if middleware in settings.MIDDLEWARE:
                print(f"✓ {middleware} - Found in settings")
            else:
                print(f"✗ {middleware} - NOT found in settings")
                
    except Exception as e:
        print(f"✗ Settings import failed: {str(e)}")

if __name__ == '__main__':
    test_settings_import()
    test_middleware_configuration() 