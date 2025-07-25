# chats/middleware.py

import logging
from datetime import datetime, timedelta
from django.http import HttpResponseForbidden

# 1. Logging User Requests
class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        logging.basicConfig(
            filename='requests.log',
            level=logging.INFO,
            format='%(message)s'
        )

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        logging.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
        return self.get_response(request)


# 2. Restrict Chat Access by Time (6PM to 9PM only)
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.now().time()
        if not (18 <= now.hour < 21):
            return HttpResponseForbidden("Access to chat is allowed only between 6PM and 9PM.")
        return self.get_response(request)


# 3. Offensive Language / Rate Limiting Middleware (5 messages/minute)
class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_log = {}

    def __call__(self, request):
        if request.method == 'POST' and request.path.startswith('/chats/'):
            ip = request.META.get('REMOTE_ADDR')
            now = datetime.now()
            messages = self.message_log.get(ip, [])

            # Keep only messages within the last minute
            messages = [msg for msg in messages if now - msg < timedelta(minutes=1)]

            if len(messages) >= 5:
                return HttpResponseForbidden("Message rate limit exceeded. Try again later.")

            messages.append(now)
            self.message_log[ip] = messages

        return self.get_response(request)


# 4. Role-Based Access Control Middleware
class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        protected_paths = ['/chats/delete/', '/chats/manage/']  # adjust to real paths as needed

        if any(request.path.startswith(path) for path in protected_paths):
            if not user.is_authenticated or not hasattr(user, 'role') or user.role not in ['admin', 'moderator']:
                return HttpResponseForbidden("You do not have permission to access this resource.")

        return self.get_response(request)
