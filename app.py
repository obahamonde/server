from bs4 import BeautifulSoup as Bs, Tag, NavigableString
from typing import Optional, List, Dict, Tuple, Union, Any
from pydantic import HttpUrl, Field
import asyncio
import aiohttp
from datetime import datetime

async def _fetch(url:HttpUrl):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return [a['href'] for a in Bs(str(await response.text(encoding='utf-8')), 'lxml').find_all('a', href=True)]

async def fetch(url:HttpUrl)->List[HttpUrl]:
    return await _fetch(url)
async def parse(url:HttpUrl)->List[HttpUrl]:
    urls = [url]
    for u in await fetch(url):
        if '#' and 'javascript:' and 'mailto:' and 'tel:' and 'sms:' and 'whatsapp:' not in u and u.startswith('/'):
            urls.append(url+u)
        elif u.startswith(url):
            urls.append(u)
        else:
            pass
    return urls
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def get_urls(url:HttpUrl):
    d = datetime.now()
    urls = await parse(url)
    tasks = []
    for u in urls:
        tasks.append(asyncio.create_task(parse(u)))
    result = await asyncio.gather(*tasks)
    for r in result:
        for i in r:
            if i not in urls:
                urls.append(i)
    return {
        "base_url": url,
        "count": len(urls),
        "children": urls,
        "response_time": datetime.now()-d,
        "urls/s": len(urls)/(datetime.now()-d).total_seconds()
    }
@app.post("/")
async def post_urls(url:HttpUrl):
    d = datetime.now()
    response = await parse(url)
    return {
        "base_url": url,
        "count": len(response),
        "children": response,
        "response_time": f"{(datetime.now() - d).total_seconds()} seconds",
        "urls/s": len(response) / (datetime.now() - d).total_seconds()
    }