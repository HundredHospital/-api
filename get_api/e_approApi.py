import json
from typing import Optional, List, Union
from fastapi import FastAPI, Header
import requests
import re

def e_appro_search(name, company, use):

    if name is not None:
        name = '='+name
    if company is not None:
        company = '='+company
    if use is not None:
        use = '='+use

    result = []
    url = f"http://apis.data.go.kr/1471000/DrbEasyDrugInfoService/getDrbEasyDrugList?" \
          f"serviceKey=hLIMsRTbYc8aY8HV9IIyK79wlrdv9gW1AIol1wtLBjlIcBXmKwcAkLhOIFi8QoDSVg%2B9wvXzdH3gZY91%2FnSUjQ%3D%3D&type=json&itemName{name}&entpName{company}&efcyQesitm{use}"
    res = requests.get(url)
    data = json.loads(res.text)
    count = 0
    if data['body']['totalCount'] == 0:
        data_appro = {}
        data_appro["name"] = "검색결과가 없습니다"
        result.append(data_appro)
        return result
    else:
        for i in data['body']['items']:
            data_appro = {}
            count += 1
            data_appro["id"] = count
            data_appro["name"] = i['itemName']
            data_appro["company"] = i['entpName']
            data_appro["use"] = re.sub('(<([^>]+)>)', '', i['efcyQesitm']).replace("\n", "")
            data_appro["amount"] = re.sub('(<([^>]+)>)', '', i['useMethodQesitm']).replace("\n", "")
            data_appro["danger"] = re.sub('(<([^>]+)>)', '', str(i['atpnQesitm'])).replace("\n", "")
            data_appro["keep"] = re.sub('(<([^>]+)>)', '', str(i['depositMethodQesitm'])).replace("\n", "")
            if i['itemImage'] is None:
                data_appro["img"] = "이미지 없음"
            else:
                data_appro["img"] = i['itemImage']
            result.append(data_appro)
    return result