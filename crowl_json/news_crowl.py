import io
import json
import re
import sys
import time
from urllib import parse

from bs4 import BeautifulSoup
import requests
from urllib3 import response


def request_url(value):
    result = []
    newslist = []
    data_news = {}
    dataJson = []
    pg_cnt = 1
    count = 0
    url = f"http://www.newsmp.com/news/articleList.html"
    if value is None:
        url += "?page=1&total=7064&box_idxno=&sc_area=A&view_type=sm&sc_word="
        request = requests.get(url)
        html = request.text
        soup = BeautifulSoup(html, 'html.parser')
        thnlist = soup.select(".list-block")
        for i in thnlist:
            title = re.sub('(<([^>]+)>)', '', str(i.select_one("strong").text)).replace("\n", "")
            summary = re.sub('(<([^>]+)>)', '', str(i.select_one(".line-height-3-2x").text)).replace("\n","").replace(" &amp;", "").replace("\t", "").replace("[의약뉴스]", "").replace("]", "").replace("[", "")
            date = re.sub('(<([^>]+)>)', '', str(i.select_one(".list-dated").text)).replace("\n", "").replace("[","").replace("]", "")
            link = "http://www.newsmp.com"
            link += re.sub('(<([^>]+)>)', '', str(i.select_one("a").get_attribute_list("href"))).replace("['","").replace("']", "")
            newslist.append([title, summary, link, date])
            data_news = {'title': title, 'summary': summary, 'link': link, 'date': date}
            dataJson.append(data_news)
        return dataJson
    elif len(decordeValue) < 2:
        data_news['title'] = '검색결과가 없습니다.'
        dataJson.append(data_news)
        return dataJson
    else:
        while(count < 20):
            decordeValue = parse.unquote(value)
            url += f"?page={pg_cnt}&total=7064&box_idxno=&sc_area=A&view_type=sm&sc_word={decordeValue}"
            pg_cnt += 1
            request = requests.get(url)
            html = request.text
            soup = BeautifulSoup(html, 'html.parser')
            thnlist = soup.select(".list-block")
            for i in thnlist:
                if decordeValue in i.select_one("strong").text:
                    count += 1
                    title = re.sub('(<([^>]+)>)', '', str(i.select_one("strong").text)).replace("\n", "")
                    summary = re.sub('(<([^>]+)>)', '', str(i.select_one(".line-height-3-2x").text)).replace("\n", "").replace(" &amp;", "").replace("\t", "").replace("[의약뉴스]", "").replace("]", "").replace("[", "")
                    date = re.sub('(<([^>]+)>)', '', str(i.select_one(".list-dated").text)).replace("\n", "").replace("[","").replace("]", "")
                    link = "http://www.newsmp.com"
                    link += re.sub('(<([^>]+)>)', '', str(i.select_one("a").get_attribute_list("href"))).replace("['","").replace("']", "")
                    newslist.append([title, summary, link, date])
                    data_news = {'title': title, 'summary': summary, 'link': link, 'date': date}
                    dataJson.append(data_news)
        return dataJson

def news_crowl(value):
    result = []
    newslist = []
    data_news = {}
    dataJson = []
    url = f"http://www.newsmp.com/news/articleList.html"
    count = 1
    cnt = 1
    dataJson = request_url(value)
    return dataJson