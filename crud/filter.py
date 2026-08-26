import django_filters

from .models import blog

class BlogFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(lookup_expr='icontains')
    topic = django_filters.CharFilter(lookup_expr='icontains')
    author = django_filters.CharFilter(field_name='author__username',lookup_expr='icontains')
    id = django_filters.UUIDFilter()

    class Meta:
        model = blog
        fields = [
            'name',
            'topic',
            'author',
        ]