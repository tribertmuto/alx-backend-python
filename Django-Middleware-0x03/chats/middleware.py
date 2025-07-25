from datetime import datetime, timedelta
import logging
from django.http import HttpResponseForbidden

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        logging.basicConfig(filename='requests.log', level=logging.INFO, format='%(message)s')

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        logging.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
        return self.get_response(request)

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.now().time()
        if not (18 <= now.hour < 21):
            return HttpResponseForbidden("Access to chat is allowed only between 6PM and 9PM.")
        return self.get_response(request)

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_log = {}

    def __call__(self, request):
        if request.method == 'POST' and request.path.startswith('/chats/'):
            ip = request.META.get('REMOTE_ADDR')
            now = datetime.now()
            messages = self.message_log.get(ip, [])
            messages = [msg for msg in messages if now - msg < timedelta(minutes=1)]

            if len(messages) >= 5:
                return HttpResponseForbidden("Message rate limit exceeded. Try again later.")
            messages.append(now)
            self.message_log[ip] = messages
        return self.get_response(request)

class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        protected_paths = ['/chats/delete/', '/chats/manage/']
        user = request.user
        if any(request.path.startswith(path) for path in protected_paths):
            if not user.is_authenticated or not hasattr(user, 'role') or user.role not in ['admin', 'moderator']:
                return HttpResponseForbidden("You do not have permission to access this resource.")
        return self.get_response(request)
