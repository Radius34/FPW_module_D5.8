from django.core.paginator import Paginator
from .filters import News
from django.shortcuts import render, redirect
from .models import News, Article
from django.views.generic.edit import CreateView, UpdateView, DeleteView





def news(request):
    articles = Article.objects.all().order_by('-date')  # получаем все статьи в порядке от новых к старым
    context = {
        'articles': articles
    }
    return render(request, 'news.html', context)

def news(request):
    news_list = News.objects.all().order_by('-date')  # получаем все новости в порядке от новых к старым

    # применяем фильтр, если он был отправлен в запросе
    news_filter = News(request.GET, queryset=news_list)
    filtered_news = news_filter.qs

    paginator = Paginator(filtered_news, 10)  # разбиваем список новостей на страниц


def create_news(request):
    if request.method == 'POST':
        # Получение данных из формы
        title = request.POST['title']
        content = request.POST['content']

        # Создание новости
        news = Article(title=title, content=content, is_news=True)
        news.save()

        return redirect('news_list')  # Перенаправление на страницу со списком новостей
    else:
        return render(request, 'create_news.html')

class NewsCreateView(CreateView):
    model = News
    fields = []  # Здесь перечислите поля модели News, которые должны отображаться на странице создания
    pass

class NewsUpdateView(UpdateView):
    model = News
    fields = []  # Здесь перечислите поля модели News, которые должны отображаться на странице редактирования
    pass

class NewsDeleteView(DeleteView):
    model = News
    pass

class ArticleCreateView(CreateView):
    model = Article
    fields = []  # Здесь перечислите поля модели Article, которые должны отображаться на странице создания
    pass

class ArticleUpdateView(UpdateView):
    model = Article
    fields = []  # Здесь перечислите поля модели Article, которые должны отображаться на странице редактирования
    pass

class ArticleDeleteView(DeleteView):
    model = Article
    pass