import django_filters
from .models import Comment


class CommentListFilter(django_filters.rest_framework.FilterSet):
    contentId = django_filters.CharFilter(field_name='contentId', lookup_expr='exact')
    commentId = django_filters.CharFilter(field_name='commentId', lookup_expr='exact')

    class Meta:
        model = Comment
        fields = ['contentId', 'commentId']