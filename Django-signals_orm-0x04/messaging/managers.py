from django.db import models


class UnreadMessagesManager(models.Manager):
    """Custom manager for unread messages."""
    
    def unread_for_user(self, user):
        """Get unread messages for a specific user."""
        return self.filter(
            receiver=user,
            read=False
        ).select_related('sender', 'receiver').only(
            'id', 'content', 'timestamp', 'sender__username', 'receiver__username'
        ) 