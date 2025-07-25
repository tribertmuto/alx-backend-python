import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    sent_at = django_filters.DateFromToRangeFilter()
    sender = django_filters.CharFilter(field_name='sender__username')
    conversation = django_filters.UUIDFilter(field_name='conversation__conversation_id')

    class Meta:
        model = Message
        fields = ['sender', 'sent_at', 'conversation']
