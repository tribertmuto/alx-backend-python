from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
from django.db.models import Q
from .models import Message, Notification, MessageHistory


@cache_page(60)  # Cache for 60 seconds
@login_required
def conversation_list(request):
    """Display list of conversations with caching."""
    # Get conversations where user is either sender or receiver
    conversations = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).select_related('sender', 'receiver').prefetch_related('replies').only(
        'id', 'content', 'timestamp', 'sender__username', 'receiver__username'
    ).distinct()
    
    # Group by conversation partner
    conversation_partners = {}
    for msg in conversations:
        partner = msg.sender if msg.receiver == request.user else msg.receiver
        if partner.id not in conversation_partners:
            conversation_partners[partner.id] = {
                'partner': partner,
                'last_message': msg,
                'unread_count': Message.unread.unread_for_user(request.user).filter(
                    sender=partner
                ).count()
            }
    
    context = {
        'conversations': conversation_partners.values(),
        'unread_count': Message.unread.unread_for_user(request.user).count()
    }
    return render(request, 'messaging/conversation_list.html', context)


@login_required
def conversation_detail(request, user_id):
    """Display detailed conversation with a specific user."""
    other_user = get_object_or_404(User, id=user_id)
    
    # Get all messages between the two users
    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(receiver=other_user)) |
        (Q(sender=other_user) & Q(receiver=request.user))
    ).select_related('sender', 'receiver').prefetch_related('replies').only(
        'id', 'content', 'timestamp', 'read', 'edited', 'parent_message',
        'sender__username', 'receiver__username'
    ).order_by('timestamp')
    
    # Mark messages as read
    unread_messages = messages.filter(receiver=request.user, read=False)
    unread_messages.update(read=True)
    
    context = {
        'other_user': other_user,
        'messages': messages,
    }
    return render(request, 'messaging/conversation_detail.html', context)


@login_required
def send_message(request, user_id):
    """Send a message to another user."""
    if request.method == 'POST':
        receiver = get_object_or_404(User, id=user_id)
        content = request.POST.get('content', '').strip()
        parent_message_id = request.POST.get('parent_message')
        
        if content:
            message = Message.objects.create(
                sender=request.user,
                receiver=receiver,
                content=content,
                parent_message_id=parent_message_id if parent_message_id else None
            )
            return JsonResponse({'success': True, 'message_id': message.id})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})


@login_required
def edit_message(request, message_id):
    """Edit a message."""
    message = get_object_or_404(Message, id=message_id, sender=request.user)
    
    if request.method == 'POST':
        new_content = request.POST.get('content', '').strip()
        if new_content and new_content != message.content:
            message.content = new_content
            message.save()
            return JsonResponse({'success': True})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})


@login_required
def message_history(request, message_id):
    """View edit history of a message."""
    message = get_object_or_404(Message, id=message_id)
    history = MessageHistory.objects.filter(message=message).select_related('edited_by').only(
        'id', 'old_content', 'edited_at', 'edited_by__username'
    ).order_by('-edited_at')
    
    context = {
        'message': message,
        'history': history,
    }
    return render(request, 'messaging/message_history.html', context)


@login_required
def notifications(request):
    """View user notifications."""
    notifications = Notification.objects.filter(user=request.user).select_related('message__sender').only(
        'id', 'timestamp', 'read', 'message__content', 'message__sender__username'
    )
    
    if request.method == 'POST':
        # Mark notifications as read
        notification_ids = request.POST.getlist('mark_read')
        if notification_ids:
            Notification.objects.filter(
                id__in=notification_ids,
                user=request.user
            ).update(read=True)
            return redirect('notifications')
    
    context = {
        'notifications': notifications,
    }
    return render(request, 'messaging/notifications.html', context)


@login_required
def unread_messages(request):
    """View unread messages using custom manager."""
    unread_messages = Message.unread.unread_for_user(request.user)
    
    context = {
        'unread_messages': unread_messages,
    }
    return render(request, 'messaging/unread_messages.html', context)


@login_required
def delete_user_account(request):
    """Delete user account and all related data."""
    if request.method == 'POST':
        # The post_delete signal will handle cleanup automatically
        # due to CASCADE relationships
        user = request.user
        user.delete()
        return redirect('login')
    
    return render(request, 'messaging/delete_account.html')


@login_required
def threaded_conversation(request, message_id):
    """View threaded conversation starting from a specific message."""
    root_message = get_object_or_404(Message, id=message_id)
    
    # Get the entire thread using the model method
    thread_messages = root_message.get_thread()
    
    context = {
        'root_message': root_message,
        'thread_messages': thread_messages,
    }
    return render(request, 'messaging/threaded_conversation.html', context) 