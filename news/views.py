from django.shortcuts import render
from django.views.decorators.cache import cache_page

from news.services import get_parsed_news, get_news_detail


def news_list_view(request):
    news = get_parsed_news()

    context = {
        'news': news
    }

    return render(request, 'news.html', context=context)

def news_detail_view(request, news_id):
    news = get_news_detail(news_id)

    context = {
        'news': news
    }

    return render(request, 'news-detail.html', context=context)