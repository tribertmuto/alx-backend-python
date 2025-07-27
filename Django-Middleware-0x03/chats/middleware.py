from datetime import datetime, timedelta
import logging
from django.http import HttpResponseForbidden, HttpResponseServerError
from django.conf import settings
import os

# Configure logging with proper file path
log_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'requests.log')
logging.basicConfig(
    filename=log_file, 
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            user = request.user if request.user.is_authenticated else 'Anonymous'
            logging.info(f"User: {user} - Path: {request.path} - Method: {request.method}")
            response = self.get_response(request)
            return response
        except Exception as e:
            logging.error(f"Error in RequestLoggingMiddleware: {str(e)}")
            return HttpResponseServerError("Internal server error")

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            now = datetime.now().time()
            # Allow access between 6 PM and 9 PM (18:00 - 21:00)
            if not (18 <= now.hour < 21):
                return HttpResponseForbidden("Access to chat is allowed only between 6PM and 9PM.")
            return self.get_response(request)
        except Exception as e:
            logging.error(f"Error in RestrictAccessByTimeMiddleware: {str(e)}")
            return HttpResponseServerError("Internal server error")

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_log = {}

    def __call__(self, request):
        try:
            if request.method == 'POST' and request.path.startswith('/api/'):
                ip = request.META.get('REMOTE_ADDR', 'unknown')
                now = datetime.now()
                messages = self.message_log.get(ip, [])
                # Clean old messages (older than 1 minute)
                messages = [msg for msg in messages if now - msg < timedelta(minutes=1)]

                if len(messages) >= 5:
                    return HttpResponseForbidden("Message rate limit exceeded. Try again later.")
                messages.append(now)
                self.message_log[ip] = messages
            return self.get_response(request)
        except Exception as e:
            logging.error(f"Error in RateLimitMiddleware: {str(e)}")
            return HttpResponseServerError("Internal server error")

class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            protected_paths = ['/api/delete/', '/api/manage/']
            user = request.user
            
            if any(request.path.startswith(path) for path in protected_paths):
                if not user.is_authenticated:
                    return HttpResponseForbidden("Authentication required.")
                
                if not hasattr(user, 'role') or user.role not in ['admin', 'moderator']:
                    return HttpResponseForbidden("You do not have permission to access this resource.")
            
            return self.get_response(request)
        except Exception as e:
            logging.error(f"Error in RolepermissionMiddleware: {str(e)}")
            return HttpResponseServerError("Internal server error")
