import requests
import config
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
stock_api = config.STOCK_API_KEY
news_api = config.NEWS_API_KEY
ACCOUNT_SID = config.account_sid
AUTH_TOKEN = config.auth_token

stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": stock_api,

}
response = requests.get(STOCK_ENDPOINT, params=stock_parameters)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
print(day_before_yesterday_closing_price)

difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

diff_percent = round((difference / float(yesterday_closing_price)) * 100)
print(diff_percent)


if abs(diff_percent) > 0:
    news_parameter = {
        "apiKey": news_api,
        "qInTitle": COMPANY_NAME,
    }
    response = requests.get(NEWS_ENDPOINT, params=news_parameter)
    response.raise_for_status()
    news_data = response.json()
    three_articles = news_data["articles"][:3]
    print(three_articles)
    # for article in three_articles:
    #     print(article["title"])
    #     print(article["description"])
    formatted_article = [f"Headline: {article['title']} brief: {article['description']}" for article in three_articles]
    print(formatted_article)

    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    for article in formatted_article:
        message = client.messages.create(
            body = article,
            from_='+18773984454',
            to='+16193419392'
        )