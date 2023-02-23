import io
import json
import re
import sys
import time
from urllib import parse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup


def news_crowl(value):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_argument("headless")

    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')
    url = "http://www.newsmp.com/news/articleList.html?sc_section_code=S1N2&view_type=sm"
    driver.get(url)
    search_tag = driver.find_element(By.ID, "search")
    if value is None:
        value = " "
    decordeValue = parse.unquote(value)
    search_tag.send_keys(decordeValue)
    search_tag.send_keys(Keys.ENTER)
    time.sleep(1)
    thnlist = driver.find_elements(By.CLASS_NAME, "list-block")
    newslist = []
    data_news = {}
    count = 0
    # list2 = thnlist.find_all(".item")
    for i in thnlist:
        count += 1
        rank = count
        title = re.sub('(<([^>]+)>)', '', str(i.find_element(By.TAG_NAME, "strong").text)).replace("\n", "")
        summary = re.sub('(<([^>]+)>)', '', str(i.find_element(By.CLASS_NAME, "line-height-3-2x").text)).replace("\n","").replace(" &amp;", "").replace("\t", "").replace("[의약뉴스]", "").replace("]", "").replace("[", "")
        date = re.sub('(<([^>]+)>)', '', str(i.find_element(By.CLASS_NAME, "list-dated").text)).replace("\n","").replace("[","").replace("]", "")
        newslist.append([rank, title, summary, date])
        data_news[str(rank)] = {'title': title, 'summary': summary, 'date': date}
    json_val = json.dumps(data_news)
    return json_val
