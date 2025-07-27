from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import ChatMessage, User
import json

def chat_view(request):
    """Simple chat view to test middleware."""
    return HttpResponse("Chat view - Middleware is working!")

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request):
    """Send a chat message."""
    try:
        data = json.loads(request.body)
        message_text = data.get('message', '')
        
        if not message_text:
            return Response({'error': 'Message cannot be empty'}, status=400)
        
        message = ChatMessage.objects.create(
            user=request.user,
            message=message_text
        )
        
        return Response({
            'id': message.id,
            'message': message.message,
            'timestamp': message.timestamp,
            'user': message.user.username
        }, status=201)
    except json.JSONDecodeError:
        return Response({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_message(request, message_id):
    """Delete a chat message (admin/moderator only)."""
    try:
        message = ChatMessage.objects.get(id=message_id)
        message.delete()
        return Response({'message': 'Message deleted successfully'}, status=200)
    except ChatMessage.DoesNotExist:
        return Response({'error': 'Message not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def manage_chat(request):
    """Manage chat (admin/moderator only)."""
    try:
        messages = ChatMessage.objects.all().order_by('-timestamp')[:50]
        data = [{
            'id': msg.id,
            'message': msg.message,
            'timestamp': msg.timestamp,
            'user': msg.user.username,
            'user_role': msg.user.role
        } for msg in messages]
        return Response(data, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500) 