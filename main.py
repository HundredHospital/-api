# uvicorn main:app --reload --host=0.0.0.0 --port=8000

import json
from typing import Optional, List, Union
from fastapi import FastAPI, Header
import requests
import re

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/search")
async def say_hello(name: Union[str] = Header(default=None), company: Union[str] = Header(default=None), use: Union[str] = Header(default=None)):

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
    for i in data['body']['items']:
        data_appro = {}
        data_appro["name"] = i['itemName']
        data_appro["company"] = i['entpName']
        data_appro["use"] = re.sub('(<([^>]+)>)', '', i['efcyQesitm']).replace("\n", "")
        data_appro["amount"] = re.sub('(<([^>]+)>)', '', i['useMethodQesitm']).replace("\n", "")
        data_appro["danger"] = re.sub('(<([^>]+)>)', '', str(i['atpnQesitm'])).replace("\n", "")
        data_appro["keep"] = re.sub('(<([^>]+)>)', '', str(i['depositMethodQesitm'])).replace("\n", "")
        result.append(data_appro)

    return result
