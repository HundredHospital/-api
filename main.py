# uvicorn main:app --reload --host=0.0.0.0 --port=5055

import json
from typing import Optional, List, Union
from fastapi import FastAPI, Header
import requests
import re
from fastapi.middleware.cors import CORSMiddleware
from crowl_json.newsRank_crowl import newsRank_crowl
from crowl_json.news_crowl import news_crowl
from crowl_json.news_crowl2 import news_crowl2
from get_api.e_approApi import e_appro_search

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/search")
async def appro_search(name: Union[str] = Header(default=None), company: Union[str] = Header(default=None), use: Union[str] = Header(default=None)):
    return e_appro_search(name, company, use)


# @app.get("/news")
# async def news(value: Union[str] = Header(default=None)):
#     return news_crowl2(value)

@app.get("/news")
async def news(value: Union[str] = Header(default=None)):
    return news_crowl(value)


@app.get("/newsRank")
async def newsRank():
    result = []
    res = json.loads(newsRank_crowl())
    result.append(res)
    return result