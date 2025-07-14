import json
import urllib.request
from datetime import datetime, timedelta
from config import GNEWS_API, PERPLEXITY_API, categories, prompt
from openai import OpenAI
from pydantic import BaseModel

client = OpenAI(api_key=PERPLEXITY_API, base_url="https://api.perplexity.ai")

class ResponseFormat(BaseModel):
    topic: str
    explainer: str
    latest_coverage: str
    diverging_perspectives: str

messages = [
    {
        "role": "system",
        "content": (
            prompt
        ),
    },
    {   
        "role": "user",
        "content": (
            "Topic: "
        ),
    },
]

def fetch_news(category: str, country: str):

    now = datetime.utcnow()              
    yesterday = now - timedelta(days=1) 
    print(now, yesterday)
    apikey = GNEWS_API
    # category = "technology"
    # country = "sg"
    # url = f"https://gnews.io/api/v4/top-headlines?category={category}&country=us&lang=en&max=100&from=2025-07-10T00:00:00Z&to=2025-07-11T00:00:00Z&apikey={apikey}"
    url = (
        f"https://gnews.io/api/v4/top-headlines"
        f"?category={category}"
        f"&country={country}"
        f"&lang=en"
        f"&max=100"
        f"&from={yesterday.strftime('%Y-%m-%dT%H:%M:%SZ')}"
        f"&to={now.strftime('%Y-%m-%dT%H:%M:%SZ')}"
        f"&apikey={apikey}&sortBy:relevance"
    )
    headlines = []
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode("utf-8"))
        articles = data["articles"]
        for i in range(len(articles)):
            # print(articles[i])
            print(f"Title: {articles[i]['title']}")
            # # articles[i].description
            print(f"Description: {articles[i]['description']}")
            print(f"Source: {articles[i]['source']}")
            art = articles[i]
            headlines.append({
                "title":       art["title"],
                "description": art.get("description", ""),
                "source":      art["source"]["name"],
                "url":         art["url"],
            })
        print("-----------------------")

        return headlines

for category in categories[:1]:
    print(category)
    country = 'sg'
    category = 'health'
    articles = fetch_news(category, country)
    # print(articles[0])
    print(messages[1]['content'])
    messages[1]['content'] += f"{articles[0]['title']}, Description: {articles[0]['description']}, Source: {articles[0]['source']}"
    print(messages[1]['content'])
    # for article in artic/les:
    response = client.chat.completions.create(
        model="sonar-pro",
        messages=messages,
        response_format={
            "type": "json_schema",
            "json_schema": {"schema": ResponseFormat.model_json_schema()}
        }
    )
    # print(response.choices[0].message.content)
    summary = response.choices[0].message.content
    print(summary)
    print(summary[0])
    print(summary[1])
    print(summary[2])
    print(summary[3])
    # print(summary['topic'])
    # print(summary['explainer'])
    # print(summary['latest_coverage'])
    # print(summart['diverging_perspectives'])

    break

        # make perplexity API call