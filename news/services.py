from datetime import datetime
from xml.dom.minidom import parseString

import requests


def get_parsed_news():
    news_rss_url = 'https://www.mos.ru/eco/news/rss/'
    try:
        response = requests.get(news_rss_url)
    except Exception as e:
        return {'error': 'Новостей нет :('}

    if response.status_code != 200:
        return {'error': 'Новостей нет :('}

    news_document = parseString(response.content)

    news_items = news_document.getElementsByTagName("item")
    json_news = []
    for item in news_items:
        title = item.getElementsByTagName("title")[0].firstChild.data

        pub_date_str = item.getElementsByTagName("pubDate")[0].firstChild.data
        pub_date = datetime.strptime(pub_date_str, '%a, %d %b %Y %H:%M:%S %z')

        description = item.getElementsByTagName("description")[0].firstChild.data
        link = item.getElementsByTagName("link")[0].firstChild.data

        image = item.getElementsByTagName("enclosure")
        if image:
            image = image[0].getAttribute("url")
        else:
            image = None

        json_news.append({
            "title": title,
            "description": description,
            "link": link,
            "image": image,
            "date": pub_date,
        })

    return json_news
