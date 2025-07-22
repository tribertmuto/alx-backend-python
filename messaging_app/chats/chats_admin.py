from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Conversation, Message

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'role', 'phone_number', 'created_at', 'is_staff']
    list_filter = ['role', 'is_staff', 'is_superuser', 'created_at']
    search_fields = ['username', 'email', 'phone_number']
    ordering = ['-created_at']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {
            'fields': ('phone_number', 'role')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {
            'fields': ('phone_number', 'role')
        }),
    )

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['conversation_id', 'created_at', 'participant_count']
    list_filter = ['created_at']
    search_fields = ['conversation_id']
    ordering = ['-created_at']
    filter_horizontal = ['participants']
    
    def participant_count(self, obj):
        return obj.participants.count()
    participant_count.short_description = 'Participants'

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['message_id', 'sender', 'conversation', 'sent_at', 'message_preview']
    list_filter = ['sent_at', 'sender__role']
    search_fields = ['message_body', 'sender__username']
    ordering = ['-sent_at']
    raw_id_fields = ['sender', 'conversation']
    
    def message_preview(self, obj):
        return obj.message_body[:50] + '...' if len(obj.message_body) > 50 else obj.message_body
    message_preview.short_description = 'Message Preview'
    from django.contrib import admin
from .models import User, Conversation, Message

admin.site.register(User)
admin.site.register(Conversation)
admin.site.register(Message)
