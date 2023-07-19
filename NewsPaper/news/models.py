from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django import template
import django_filters
from django import forms
from .models import News, Article
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from .filters import NewsFilter, ArticleFilter
from django.core.paginator import Paginator


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.post_set = None

    def update_rating(self):
       postRat = self.post_set.aggregate(Sum('rating'))
       pRat = 0
       pRat += postRat.get('postRating')

       commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
       cRat = 0
       cRat + commentRat.get('commentRating')

       self.ratingauthor = pRat *3 + cRat
       self.save()


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)


class Post (models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE )

    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )
    categoryType = models.CharField(max_lenght=2, choices=CATEGORY_CHOICES, default=ARTICLE)
    dateCreation = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    titel = models.CharField(max_lenght=128)
    text = models.TextField()
    ratingAuthor = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:123] + '...'



class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

register = template.Library()

@register.filter(name='censor')
def censor(value):
    censored_words = ['редиска', 'мат', 'оскорбление']  # список нежелательных слов
    for word in censored_words:
        value = value.replace(word, '*' * len(word))
    return value

class NewsFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label='Название')
    category = django_filters.CharFilter(lookup_expr='icontains', label='Категория')
    date__gt = django_filters.DateFilter(field_name='date', lookup_expr='gt', label='Дата публикации позже')

    class Meta:
        model = News
        fields = ['title', 'category', 'date__gt']


class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    is_news = models.BooleanField(default=False)

def __str__(self):
    return self.title

class News:
    pass


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content']


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']

class NewsCreateView(CreateView):
    model = News
    form_class = NewsForm
    template_name = 'news_create.html'
    success_url = '/news/create/'

class ArticleCreateView(CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'article_create.html'
    success_url = '/articles/create/'


class NewsListView(ListView):
    model = News
    template_name = 'news_list.html'
    context_object_name = 'news_list'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        filter = NewsFilter(self.request.GET, queryset=queryset)
        return filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(context['news_list'], self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context


class ArticleListView(ListView):
    model = Article
    template_name = 'article_list.html'
    context_object_name = 'article_list'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        filter = ArticleFilter(self.request.GET, queryset=queryset)
        return filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(context['article_list'], self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context