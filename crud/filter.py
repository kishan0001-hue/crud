from random import choices

import django_filters

from .models import blog

class BlogFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(lookup_expr='icontains')
    topic = django_filters.CharFilter(lookup_expr='icontains')
    author = django_filters.CharFilter(field_name='author__username',lookup_expr='icontains')
    id = django_filters.UUIDFilter()

    ordering = django_filters.ChoiceFilter(
        choices = [
            ('newest' , 'Newest'),
            ('oldest' , 'Oldest'),
            ('name_asc' , 'Name A-Z'),
            ('name_desc' , 'Name Z-A'),
        ],
        method= 'filter_ordering'
    )

    class Meta:
        model = blog
        fields = [
            'name',
            'topic',
            'author',
            'ordering',
        ]

    def filtering_order(self, queryset , name ,value):

        if value == 'newest':
            return queryset.order_by('created_at')
        elif value == 'oldest ':
            return queryset.order_by('created_at')
        elif value == 'name_asc' :
            return queryset.order_by('name')
        elif value == 'name_desc' :
            return queryset.order_by('-name')
        return queryset
    