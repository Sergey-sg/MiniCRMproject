import django_filters
from .models import Company


class CompanyFilter(django_filters.FilterSet):

    o = django_filters.OrderingFilter(
        fields=(
            ('name', 'name'),
            ('date_created', 'date_created'),
        ),
    )

    class Meta:
        model = Company
        fields = ('name',)
