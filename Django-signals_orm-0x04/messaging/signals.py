from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory


@receiver(post_save, sender=Message)
def create_notification_for_new_message(sender, instance, created, **kwargs):
    """Create a notification when a new message is created."""
    if created:
        # Don't create notification if sender is the same as receiver
        if instance.sender != instance.receiver:
            Notification.objects.create(
                user=instance.receiver,
                message=instance
            )


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """Log the old content before a message is edited."""
    if instance.pk:  # Only for existing messages
        try:
            old_instance = Message.objects.get(pk=instance.pk)
            if old_instance.content != instance.content:
                # Content has changed, log the old content
                MessageHistory.objects.create(
                    message=instance,
                    old_content=old_instance.content,
                    edited_by=instance.sender
                )
                instance.edited = True
        except Message.DoesNotExist:
            pass


@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    """Clean up all user-related data when a user is deleted."""
    # This signal will automatically handle CASCADE deletions
    # but we can add custom cleanup logic here if needed
    pass 