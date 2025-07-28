from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('', views.conversation_list, name='conversation_list'),
    path('conversation/<int:user_id>/', views.conversation_detail, name='conversation_detail'),
    path('send/<int:user_id>/', views.send_message, name='send_message'),
    path('edit/<int:message_id>/', views.edit_message, name='edit_message'),
    path('history/<int:message_id>/', views.message_history, name='message_history'),
    path('notifications/', views.notifications, name='notifications'),
    path('unread/', views.unread_messages, name='unread_messages'),
    path('delete-account/', views.delete_user_account, name='delete_account'),
    path('thread/<int:message_id>/', views.threaded_conversation, name='threaded_conversation'),
] 