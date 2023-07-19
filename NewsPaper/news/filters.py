import django_filters
from .models import News, Article

class NewsFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    category = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = News
        fields = ['title', 'category']

class ArticleFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    category = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Article
        fields = ['title', 'category']
