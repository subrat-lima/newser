import httpx

from datetime import datetime
from selectolax.parser import HTMLParser


def get_html(url: str):
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0"
    }
    response = httpx.get(url, headers=headers)
    return response.text


class OdishaTVHeadlinesPage:
    def __init__(self, html: str):
        self.tree = HTMLParser(html)
        self.previous_date = datetime.now().strftime("%A, %d %B %Y")

    def parse_page(self):
        articles = self.tree.css(".listing-result-news")
        return [self.parse_headline(article) for article in articles]

    def parse_headline(self, article):
        title = article.css_first("h5").text()
        if "Latest Odisha Breaking News Updates" in title:
            date = title.split("-")[1].strip()
        else:
            try:
                date = article.css_first(
                    ".listing-result-news-subcontent > ul > li"
                ).text()
            except:
                date = self.previous_date
        self.previous_date = date
        date = datetime.strptime(date, "%A, %d %B %Y").strftime("%s")
        return {
            "url": article.css_first("a").attributes.get("href"),
            "date": date,
            "title": title,
        }

    @property
    def next_page(self):
        next_elem = self.tree.css_first("a[rel='next']")
        if next_elem is not None:
            return next_elem.attributes.get("href")
        return None


def convert_json_to_sfeed(json_data):
    sfeed_data = ""
    for article in json_data:
        sfeed_data += f"{article['date']}\t{article['title']}\t{article['url']}\n"
    return sfeed_data


def fetch_news(url, output="sfeed"):
    try:
        html = get_html(url)
    except:
        print("error fetching html, please try after sometime")
        return -1
    else:
        otv = OdishaTVHeadlinesPage(html)
        json_data = otv.parse_page()
        if output == "json":
            return json_data
        elif output == "sfeed":
            sfeed_data = convert_json_to_sfeed(json_data)
            return sfeed_data
    print("invalid format selected")
    return -2


def main():
    url = "https://odishatv.in/odisha"
    news = fetch_news(url)
    print(news)


if __name__ == "__main__":
    main()
