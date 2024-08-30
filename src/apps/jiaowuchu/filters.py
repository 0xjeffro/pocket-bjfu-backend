import django_filters
from .models import JiaoWuChuNews


class JiaoWuChuNewsFilter(django_filters.rest_framework.FilterSet):
    url = django_filters.CharFilter(field_name='url', lookup_expr='exact')
    title = django_filters.CharFilter(field_name='title', lookup_expr='exact')

    class Meta:
        model = JiaoWuChuNews
        fields = ['url', 'title']