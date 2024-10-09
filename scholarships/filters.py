import django_filters
from .models import Scholarship
from django.db.models import Q

class ScholarshipFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_by_name_or_foundation')

    class Meta:
        model = Scholarship
        fields = ['financial_aid_type']  

    def filter_by_name_or_foundation(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) | Q(foundation_name__icontains=value)
        ) 
