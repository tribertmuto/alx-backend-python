from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer, UserSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter conversations to only show those the user is a participant in
        return self.queryset.filter(participants=self.request.user)

    def create(self, request):
        # Create a new conversation
        conversation = Conversation.objects.create()
        
        # Add the current user as a participant
        conversation.participants.add(request.user)
        
        # Add other participants if provided
        participant_ids = request.data.get('participant_ids', [])
        if participant_ids:
            participants = User.objects.filter(user_id__in=participant_ids)
            conversation.participants.add(*participants)
        
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def add_participants(self, request, pk=None):
        conversation = self.get_object()
        participant_ids = request.data.get('participant_ids', [])
        
        if not participant_ids:
            return Response(
                {'error': 'No participant IDs provided'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        participants = User.objects.filter(user_id__in=participant_ids)
        conversation.participants.add(*participants)
        
        serializer = self.get_serializer(conversation)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        conversation = self.get_object()
        messages = conversation.messages.all().order_by('sent_at')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter messages to only show those from conversations the user is in
        return self.queryset.filter(
            conversation__participants=self.request.user
        ).order_by('-sent_at')

    def create(self, request):
        # Extract data
        conversation_id = request.data.get('conversation_id')
        message_body = request.data.get('message_body')
        
        if not conversation_id or not message_body:
            return Response(
                {'error': 'conversation_id and message_body are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if conversation exists and user is a participant
        try:
            conversation = Conversation.objects.get(
                conversation_id=conversation_id,
                participants=request.user
            )
        except Conversation.DoesNotExist:
            return Response(
                {'error': 'Conversation not found or you are not a participant'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Create message
        message = Message.objects.create(
            sender=request.user,
            conversation=conversation,
            message_body=message_body
        )
        
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        # Allow filtering by conversation
        conversation_id = request.query_params.get('conversation_id')
        queryset = self.get_queryset()
        
        if conversation_id:
            queryset = queryset.filter(conversation__conversation_id=conversation_id)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        if not query:
            return Response([])
        
        users = self.queryset.filter(
            Q(username__icontains=query) | 
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        ).exclude(user_id=request.user.user_id)[:10]
        
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)