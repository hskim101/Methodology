import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
 
def getNewsData(keyword, final):
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
    }
    response = requests.get(
        f"https://www.google.com/search?q={keyword}s&gl=us&tbm=nws&num=100", headers=headers
    )
    soup = BeautifulSoup(response.content, "html.parser")
    news_results = []
 
    for el in soup.select("div.SoaBEf"):
        final.append(
            {
                "link": el.find("a")["href"],
                "title": el.select_one("div.MBeuO").get_text(),
                "snippet": el.select_one(".GI74Re").get_text(),
                "date": el.select_one(".LfVVr").get_text(),
                "source": el.select_one(".NUnG9d span").get_text()
            }
        )

    return final
    # print(json.dumps(news_results, indent=2))
  
keywords = ['firenoodle', '불닭', '불닭챌린지', 'firenoodlechallenge', 'koreanspicynoodle', '불닭볶음면', '핵붉닭', 'nuclearfirenoodle', 'noodlechallenge']
final = []
for keyword in keywords:
    final = getNewsData(keyword, final)

result = pd.DataFrmae(final)
result.to_csv("f/home/lafesta/Desktop/Methodology/dataset/news/news.csv}")