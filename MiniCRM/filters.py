import django_filters
from .models import Message


class MessageFilter(django_filters.FilterSet):
    message = django_filters.CharFilter(field_name='message', lookup_expr='icontains')
    # message = django_filters.MultipleChoiceFilter(lookup_expr='i_contains')

    class Meta:
        model = Message
        fields = ('message',)
