from datetime import datetime
from django.http import HttpResponseForbidden

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.now().time()
        if not (now.hour >= 18 and now.hour < 21):  # 6PM to 9PM
            return HttpResponseForbidden("Access to chat is allowed only between 6PM and 9PM.")
        return self.get_response(request)
