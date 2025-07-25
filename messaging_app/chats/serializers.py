from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 
                  'phone_number', 'role', 'created_at']
        read_only_fields = ['user_id', 'created_at']


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    conversation_id = serializers.UUIDField(write_only=True, required=False)

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'conversation', 'conversation_id', 
                  'message_body', 'sent_at']
        read_only_fields = ['message_id', 'sender', 'sent_at', 'conversation']
        extra_kwargs = {
            'conversation': {'read_only': True}
        }


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    participant_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False
    )
    last_message = serializers.SerializerMethodField()
    participant_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'participant_ids', 
                  'messages', 'created_at', 'last_message', 'participant_count']
        read_only_fields = ['conversation_id', 'created_at']

    def get_last_message(self, obj):
        last_message = obj.messages.order_by('-sent_at').first()
        if last_message:
            return {
                'message_body': last_message.message_body,
                'sent_at': last_message.sent_at,
                'sender': last_message.sender.username
            }
        return None

    def get_participant_count(self, obj):
        return obj.participants.count()


class ConversationListSerializer(serializers.ModelSerializer):
    """Lighter serializer for listing conversations without all messages"""
    participants = UserSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 
                  'last_message', 'unread_count']

    def get_last_message(self, obj):
        last_message = obj.messages.order_by('-sent_at').first()
        if last_message:
            return {
                'message_body': last_message.message_body[:50] + '...' 
                    if len(last_message.message_body) > 50 
                    else last_message.message_body,
                'sent_at': last_message.sent_at,
                'sender': last_message.sender.username
            }
        return None

    def get_unread_count(self, obj):
        # This is a placeholder - you'd need to implement read receipts
        return 0