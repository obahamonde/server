from pytube import YouTube
import re
from pydantic import HttpUrl
import aiohttp
from fastapi import APIRouter
from typing import List, Union
import asyncio
from datetime import datetime
from os import remove
from app.handlers.upload import s3
from app.config import AWS_S3_BUCKET
from app.utils import uid

video_id_pattern = re.compile(r'(?<=watch\?v=){1}[a-zA-Z0-9-_]{11}')

async def fetch_raw(url: HttpUrl) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text(encoding='utf-8')
        
async def fetch_ids(url: HttpUrl) -> str:
    raw = await fetch_raw(url)
    return video_id_pattern.findall(raw)
    
    
async def fetch_url(url: HttpUrl) -> List[HttpUrl]:
    ids = await fetch_ids(url)
    urls = [f'https://www.youtube.com/watch?v={id}' for id in ids]
    response = []
    for _ in urls:
        if _ not in response:
            response.append(_)
    return response

async def fetch_many(url: HttpUrl) -> List[HttpUrl]:
    tasks = [fetch_url(u) for u in await fetch_url(url)]
    urls = [u for t in await asyncio.gather(*tasks) for u in t]
    response = []
    for _ in urls:
        if _ not in response:
            response.append(_)
    return response

def download_video(url: HttpUrl) -> str:
    i = uid()
    yt = YouTube(url)
    yt.streams.filter(file_extension='mp4').first().download(filename=f"tmp/{i}.mp4")
    with open(f"tmp/{i}.mp4", 'rb') as f:
        s3.put_object(Body=f, Bucket=AWS_S3_BUCKET, Key=f'youtube/{i}.mp4',
                        ContentType='video/mp4', ACL='public-read')
    remove(f"tmp/{i}.mp4")
    url = f'https://{AWS_S3_BUCKET}.s3.amazonaws.com/youtube/{i}.mp4'
    return url

app = APIRouter()

@app.post('/yt')
async def yt(url: HttpUrl):
    d = datetime.now()
    response = await fetch_url(url)
    print(f'{datetime.now() - d}')
    return{
        "url": url,
        "data": response,
        "time": datetime.now() - d,
        "urls/s": f"{len(response)/(datetime.now() - d).total_seconds()} urls/s"
    }
@app.get('/yt')
async def yt_many(url: HttpUrl):
    d = datetime.now()
    response = await fetch_many(url)
    print(f'{datetime.now() - d}')
    return {
        "url": url,
        "data": response,
        "time": datetime.now() - d,
        "urls/s": f"{len(response)/(datetime.now() - d).total_seconds()} urls/s"
    }

@app.get('/yt/video')
async def yt_upload(url: HttpUrl):
    return download_video(url)