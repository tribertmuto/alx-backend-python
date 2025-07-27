from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_view, name='chat_view'),
    path('send/', views.send_message, name='send_message'),
    path('delete/<int:message_id>/', views.delete_message, name='delete_message'),
    path('manage/', views.manage_chat, name='manage_chat'),
] 