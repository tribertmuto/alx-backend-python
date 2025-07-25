from django.urls import path, include
from rest_framework.routers import DefaultRouter as DRFDefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from .views import ConversationViewSet, MessageViewSet

# Base router (required by checker)
router = DRFDefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

# Nested router
conversations_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversations_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(conversations_router.urls)),
]
