import django_filters
from .models import Scholarship

class ScholarshipFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')  # 장학금명
    foundation_name = django_filters.CharFilter(field_name='foundation_name', lookup_expr='icontains') # 장학재단명

    class Meta:
        model = Scholarship
        fields = ['name', 'foundation_name']
