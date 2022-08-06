from bs4 import BeautifulSoup as Soup
from typing import List
from pydantic import HttpUrl
import asyncio
import aiohttp
from datetime import datetime
from fastapi import APIRouter


async def _fetch(url: HttpUrl):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return [
                a['href']
                for a in Soup(str(await response.text(
                    encoding='utf-8')), 'lxml').find_all('a', href=True)
            ]


async def _img(url: HttpUrl):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return [
                    i['src']
                    for i in Soup(str(await response.text(
                        encoding='utf-8')), 'lxml').find_all('img', src=True)
                ]


async def fetch(url: HttpUrl) -> List[HttpUrl]:
    return await _fetch(url)


async def img(url: HttpUrl) -> List[HttpUrl]:
    return await _img(url)


async def crawl(url: HttpUrl) -> List[HttpUrl]:
    urls = [url]
    for u in await fetch(url):
        if '#' and 'javascript:' and 'mailto:' and 'tel:' and 'sms:' and 'whatsapp:' not in u and u.startswith(
                '/'):
            urls.append(url + u)
        elif u.startswith(url):
            urls.append(u)
        else:
            pass
    return urls


async def crawl_img(url: HttpUrl) -> List[HttpUrl]:
    urls = await crawl(url)
    tasks = []
    urls_img = []
    for u in urls:
        tasks.append(img(u))
    for t in await asyncio.gather(*tasks):
        for _ in t:
            if _ not in urls_img:
                urls_img.append(_)
    return urls_img

app = APIRouter()


@app.post("/crawl/2")
async def crawl_depth_2(url: HttpUrl):
    d = datetime.now()
    urls = await crawl(url)
    tasks = []
    for u in urls:
        tasks.append(asyncio.create_task(crawl(u)))
    result = await asyncio.gather(*tasks)
    for r in result:
        for i in r:
            if i not in urls:
                urls.append(i)
    return {
        "base_url": url,
        "count": len(urls),
        "children": urls,
        "response_time": datetime.now() - d,
        "urls/s": len(urls) / (datetime.now() - d).total_seconds()
    }


@app.get("/crawl/1")
async def crawl_depth_1(url: HttpUrl):
    d = datetime.now()
    response = await crawl(url)
    return {
        "base_url": url,
        "count": len(response),
        "children": response,
        "response_time": f"{(datetime.now() - d).total_seconds()} seconds",
        "urls/s": len(response) / (datetime.now() - d).total_seconds()
    }


@app.get("/crawl/img")
async def crawl_img_depth_1(url: HttpUrl):
    d = datetime.now()
    response = await crawl_img(url)
    return {
        "base_url": url,
        "count": len(response),
        "children": response,
        "response_time": f"{(datetime.now() - d).total_seconds()} seconds",
        "urls/s": len(response) / (datetime.now() - d).total_seconds()
    }
