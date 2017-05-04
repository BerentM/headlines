import feedparser
from flask import Flask
from flask import render_template
from flask import request
import json
import urllib.parse as urllib
import urllib.request as urllib2

app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://iol.co.za/cmlink/1.640'}

DEFLAUTS = {'publication': 'bbc',
            'city': 'London,UK'}

WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=2e9f596ba0ddd4175505db729821a5d7"


@app.route('/')
def home():
    # pobierz nagłówki zgodne z wyborem użytkownika
    publication = request.args.get('publication')
    if not publication:
        publication = DEFLAUTS['publication']
    articles = get_news(publication)
    # pobierz pogodę dla miasta określonego przez użytkownika
    city = request.args.get('city')
    if not city:
        city = DEFLAUTS['city']
    weather = get_weather(city)
    return render_template("home.html", articles=articles, weather=weather)


def get_news(query):
    # query = request.args.get("publication")
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFLAUTS['publication']
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    # weather = get_weather("London,UK")
    # return render_template("home.html", articles=feed['entries'],
    # weather=weather)
    return feed['entries']


def get_weather(query):
    query = urllib.quote(query)
    url = WEATHER_URL.format(query)
    data = urllib2.urlopen(url).read()
    # str_data = data.read().decode('utf-8')
    parsed = json.loads(data.decode('utf-8'))
    # parsed = json.loads(str_data)
    weather = None
    if parsed.get('weather'):
        weather = {'description': parsed['weather'][0]['description'],
                   'temperature': parsed['main']['temp'],
                   'city': parsed['name'],
                   'country': parsed['sys']['country']}
        return weather


if __name__ == '__main__':
    app.run(port=8000, debug=True)
