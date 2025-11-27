import requests
from flask import Flask, render_template
import json

from bs4 import BeautifulSoup


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


class WebScraper:
    def __init__(self, url):
        self.url = url
        self.articles = []

    def fetch_news(self):
        """Fetch news from the given news site."""
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')

        temp = self.url.split('/')
        home = temp[0] + "//" + temp[2]

        for item in soup.find_all("article"):
            title = item.find("h3").getText().strip()
            link = home + item.find("a").get("href")
            image_link = item.find("a-img").get("src")
            paragraph = item.find("p")
            if paragraph:
                summary = paragraph.getText()

                self.articles.append({
                    'title': title,
                    'link': link,
                    'image_link': image_link,
                    'summary': summary
                })

        return self.articles


class NewsHandler:
    scraper = None
    articles = []

    def __init__(self):
        self.get_news()
        self.news_to_json()
        self.news_to_html()

    def get_news(self):
        print("Set up web scraper...")
        self.scraper = WebScraper("https://www.heise.de/newsticker/it/")
        print("Scrap news articles...")
        self.articles = self.scraper.fetch_news()
        print("News articles scrapped...")

    def news_to_json(self):
        with open('articles.json', 'w', encoding='utf-8') as f:
            json.dump(self.articles, f, ensure_ascii=False, indent=4)

    def news_to_html(self):
        file = open("templates/index.html", "w")
        file.write("<!DOCTYPE html>\n")
        file.write("<html lang=\"de\">\n")
        file.write("\t<head>\n")
        file.write("\t\t<meta charset=\"UTF-8\">\n")
        file.write("\t\t<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n")
        file.write("\t\t<title>News Scraper TEKO</title>\n")
        file.write("\t\t<link rel=\"shortcut icon\" type=\"image/png\" href=\"{{ url_for('static', filename='images/favicon.ico') }}\" />\n")
        file.write("\t\t<link rel=\"stylesheet\" href=\"{{ url_for('static', filename='css/index.css') }}\" />\n")
        file.write("\t</head>\n")
        file.write("\t<body>\n")
        file.write("\t\t<input id=\"searchbar\" placeholder=\"Durchsuche News...\" oninput=\"filterNews()\" />\n")
        file.write("\t\t<div id=\"article-holder\">\n")
        for article in self.articles:
            file.write("\t\t\t<article>\n")
            file.write(f"\t\t\t\t<a href=\"{article['link']}\" target=\"_blank\">\n")
            file.write(f"\t\t\t\t\t<img src=\"{article['image_link']}\"/>\n")
            file.write(f"\t\t\t\t\t<h3>{article['title']}</h3>\n")
            file.write(f"\t\t\t\t\t<p>{article['summary']}</p>\n")
            file.write("\t\t\t\t</a>\n")
            file.write("\t\t\t</article>\n")
        file.write("\t\t</div>\n")
        file.write("\t\t<script src=\"{{ url_for('static', filename='js/index.js') }}\"></script>\n")
        file.write("\t</body>\n")
        file.write("</html>\n")
        file.close()


if __name__ == '__main__':
    handler = NewsHandler()
    app.run()
