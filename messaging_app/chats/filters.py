import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    timestamp = django_filters.DateFromToRangeFilter()
    sender = django_filters.CharFilter(field_name='sender__username')

    class Meta:
        model = Message
        fields = ['sender', 'timestamp']
