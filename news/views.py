from django.shortcuts import render
from django.views.decorators.cache import cache_page

from news.services import get_parsed_news

def news_list_view(request):
    news = get_parsed_news()

    context = {
        'news': news
    }

    return render(request, 'news.html', context=context)
