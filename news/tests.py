from datetime import datetime

from django.test import TestCase
from django.urls import reverse
from unittest import mock

from news.services import get_parsed_news

test_rss_content = """ 
<rss xmlns:yandex="http://news.yandex.ru" xmlns:media="http://search.yahoo.com/mrss/" xmlns:infographic="https://www.mos.ru/mayor/infographic/" version="2.0">
<channel>
<title>Новости - Департамент природопользования и охраны окружающей среды города Москвы</title>
<link>https://www.mos.ru/eco/news/rss</link>
<description>Новостная лента официального портала Мэра и Правительства Москвы</description>
    <item>
        <title>Новость 1</title>
        <description>Описание новости 1</description>
        <yandex:full-text>Текст новости 1</yandex:full-text>
        <link>https://example.com/news/1</link>
        <enclosure url="picture.jpg" type="image/jpeg"/>
        <pubDate>Thu, 01 Dec 2024 17:15:44 +0300</pubDate>
    </item>
        <item>
        <title>Новость 2</title>
        <description>Описание новости 2</description>
        <yandex:full-text>Текст новости 2</yandex:full-text>
        <link>https://example.com/news/1</link>
        <pubDate>Thu, 02 Dec 2024 17:15:44 +0300</pubDate>
    </item>
    </channel>
    </rss>
     """


class NewsViewsTest(TestCase):
    def test_news(self):
        response = self.client.get(reverse('news'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news.html')



class NewsServicesTest(TestCase):

    @mock.patch('news.services.requests')
    def test_get_parsed_news(self, mock_requests):
        mock_response = mock.MagicMock(status_code=200)
        mock_requests.get.return_value = mock_response

        mock_response.content = test_rss_content

        parsed_news = get_parsed_news()

        self.assertEqual(len(parsed_news), 2)

        self.assertEqual(parsed_news[0]['title'], 'Новость 1')
        self.assertEqual(parsed_news[0]['image'], 'picture.jpg')
        self.assertEqual(parsed_news[0]['description'], 'Описание новости 1')
        self.assertEqual(parsed_news[0]['link'], 'https://example.com/news/1')
        self.assertEqual(parsed_news[0]['date'], datetime.strptime('Thu, 01 Dec 2024 17:15:44 +0300', '%a, %d %b %Y %H:%M:%S %z'))

        self.assertEqual(parsed_news[1]['image'], None)

    @mock.patch('news.services.requests')
    def test_get_parsed_news_error(self, mock_requests):
        mock_response = mock.MagicMock(status_code=500)
        mock_requests.get.return_value = mock_response

        parsed_news = get_parsed_news()

        self.assertEqual(parsed_news['error'], 'Новостей нет :(')