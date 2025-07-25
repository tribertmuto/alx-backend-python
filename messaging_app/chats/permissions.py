from rest_framework import permissions

class IsAuthenticated(permissions.BasePermission):
    """
    Custom permission to only allow authenticated users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to access messages.
    """
    def has_permission(self, request, view):
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return False
        
        # For POST requests, check if user is participant of the conversation
        if request.method == 'POST':
            conversation_id = request.data.get('conversation')
            if conversation_id:
                try:
                    from .models import Conversation
                    conversation = Conversation.objects.get(conversation_id=conversation_id)
                    return request.user in conversation.participants.all()
                except Conversation.DoesNotExist:
                    return False
        return True

    def has_object_permission(self, request, view, obj):
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return False
        
        # For PUT, PATCH, DELETE methods, check if user is participant
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return request.user in obj.conversation.participants.all()
        
        # For GET requests, check if user is participant
        return request.user in obj.conversation.participants.all()
