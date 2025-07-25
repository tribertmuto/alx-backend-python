from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import logging

logger = logging.getLogger(__name__)

def chat_view(request):
    """Simple chat view to test middleware."""
    try:
        return HttpResponse("Chat view - Middleware is working!")
    except Exception as e:
        logger.error(f"Error in chat_view: {str(e)}")
        return HttpResponse("Error occurred", status=500)

@csrf_exempt
@require_http_methods(["POST"])
def send_message(request):
    """Send a message endpoint to test middleware."""
    try:
        data = json.loads(request.body)
        message = data.get('message', '')
        return JsonResponse({
            'status': 'success',
            'message': f'Message received: {message}'
        })
    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid JSON'
        }, status=400)
    except Exception as e:
        logger.error(f"Error in send_message: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': 'Internal server error'
        }, status=500) 