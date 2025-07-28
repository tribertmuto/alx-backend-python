from django.contrib import admin
from .models import Message, Notification, MessageHistory


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'content', 'timestamp', 'read', 'edited')
    list_filter = ('read', 'edited', 'timestamp')
    search_fields = ('sender__username', 'receiver__username', 'content')
    readonly_fields = ('timestamp',)
    date_hierarchy = 'timestamp'


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'timestamp', 'read')
    list_filter = ('read', 'timestamp')
    search_fields = ('user__username', 'message__content')
    readonly_fields = ('timestamp',)
    date_hierarchy = 'timestamp'


@admin.register(MessageHistory)
class MessageHistoryAdmin(admin.ModelAdmin):
    list_display = ('message', 'edited_by', 'edited_at')
    list_filter = ('edited_at',)
    search_fields = ('message__content', 'old_content', 'edited_by__username')
    readonly_fields = ('edited_at',)
    date_hierarchy = 'edited_at' 