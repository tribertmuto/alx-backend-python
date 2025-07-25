from django.shortcuts import render
from django.http import HttpResponse

def chat_view(request):
    """Simple chat view to test middleware."""
    return HttpResponse("Chat view - Middleware is working!") 