import io
import json
import re
import sys

import requests
from bs4 import BeautifulSoup

def news_crowl():
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')
    result = []
    url = "http://www.newsmp.com/news/articleList.html?sc_section_code=S1N2&view_type=sm"
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        newslist = []
        data_news = {}
        thnlist = soup.select('.list-block')
        count = 0
        for i in thnlist:
            count += 1
            rank = count
            title = re.sub('(<([^>]+)>)', '', str(i.find("strong"))).replace("\n", "")
            summary = re.sub('(<([^>]+)>)', '', str(i.select(".list-summary > .line-height-3-2x"))).replace("\n", "").replace("\t", "").replace("[의약뉴스]", "").replace("]", "").replace("[", "")
            date = re.sub('(<([^>]+)>)', '', str(i.select(".list-dated"))).replace("\n", "").replace("[", "").replace("]", "")
            newslist.append([rank, title, summary, date])
            data_news[str(rank)] = {'title': title, 'summary': summary, 'date': date}
        json_val = json.dumps(data_news)
        return json_val