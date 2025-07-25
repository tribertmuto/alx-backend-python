import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    phone_number = models.CharField(
        max_length=15, 
        null=True, 
        blank=True,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
        )]
    )
    ROLE_CHOICES = [
        ('guest', 'Guest'), 
        ('host', 'Host'), 
        ('admin', 'Admin')
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='guest')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
    # Override email to make it required
    email = models.EmailField(unique=True, blank=False, null=False)
    
    class Meta:
        db_table = 'users'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['username']),
        ]
    
    def __str__(self):
        return self.username
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username


class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        db_table = 'conversations'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        participant_names = ', '.join([p.username for p in self.participants.all()[:3]])
        if self.participants.count() > 3:
            participant_names += f' and {self.participants.count() - 3} others'
        return f"Conversation with {participant_names}"
    
    def get_other_participants(self, user):
        """Get all participants except the specified user"""
        return self.participants.exclude(user_id=user.user_id)


class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
    # Optional: Add read receipts
    read_by = models.ManyToManyField(User, related_name='read_messages', blank=True)
    
    class Meta:
        db_table = 'messages'
        ordering = ['-sent_at']
        indexes = [
            models.Index(fields=['conversation', 'sent_at']),
            models.Index(fields=['sender', 'sent_at']),
        ]
    
    def __str__(self):
        return f"{self.sender.username}: {self.message_body[:50]}..."
    
    def mark_as_read(self, user):
        """Mark this message as read by a user"""
        if user != self.sender:
            self.read_by.add(user)
    
    def is_read_by(self, user):
        """Check if this message has been read by a user"""
        return user in self.read_by.all()