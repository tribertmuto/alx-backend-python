from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from .managers import UnreadMessagesManager


class Message(models.Model):
    """Message model for storing user messages."""
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    edited = models.BooleanField(default=False)
    parent_message = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='replies'
    )

    # Custom managers
    objects = models.Manager()
    unread = UnreadMessagesManager()

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.sender.username} to {self.receiver.username}: {self.content[:50]}"

    def get_thread(self):
        """Get all messages in the same thread."""
        if self.parent_message:
            # This is a reply, get the original message and all its replies
            return Message.objects.filter(
                models.Q(id=self.parent_message.id) |
                models.Q(parent_message=self.parent_message) |
                models.Q(parent_message__parent_message=self.parent_message)
            ).select_related('sender', 'receiver').prefetch_related('replies').only(
                'id', 'content', 'timestamp', 'read', 'edited', 'parent_message',
                'sender__username', 'receiver__username'
            )
        else:
            # This is an original message, get it and all its replies
            return Message.objects.filter(
                models.Q(id=self.id) |
                models.Q(parent_message=self) |
                models.Q(parent_message__parent_message=self)
            ).select_related('sender', 'receiver').prefetch_related('replies').only(
                'id', 'content', 'timestamp', 'read', 'edited', 'parent_message',
                'sender__username', 'receiver__username'
            )


class Notification(models.Model):
    """Notification model for user notifications."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='notifications')
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message.content[:50]}"


class MessageHistory(models.Model):
    """Model to store message edit history."""
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-edited_at']
        verbose_name_plural = 'Message histories'

    def __str__(self):
        return f"History for message {self.message.id} edited at {self.edited_at}" 