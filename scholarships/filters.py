import django_filters
from .models import Scholarship

class ScholarshipFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')  # 장학금명
    foundation_name = django_filters.CharFilter(field_name='foundation_name', lookup_expr='icontains') # 장학재단명
    financial_aid_type = django_filters.ChoiceFilter(field_name='financial_aid_type', choices=Scholarship.FINANCIAL_AID_CHOICES)  # 학자금 유형 필터 추가

    class Meta:
        model = Scholarship
        fields = ['name', 'foundation_name', 'financial_aid_type']  
