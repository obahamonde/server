import aiohttp
import asyncio
from typing import List, Dict, Any
from pydantic import HttpUrl
from starlette.responses import JSONResponse

async def _fetch(url: HttpUrl, headers: Any=None) -> Dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(str(url), headers=headers) as response:
            return await response.json()

async def fetch_many(urls: List[HttpUrl]) -> List[Dict]:
    return await asyncio.gather(*[asyncio.create_task(_fetch(url)) for url in urls])

def fetch(urls: List[HttpUrl]) -> List[Dict]:
    return asyncio.get_event_loop().run_until_complete(fetch_many(urls))

async def _post(url: HttpUrl, headers: Any, data: Any) -> Dict:
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=data) as response:
            return await response

async def post_many(urls: List[HttpUrl], headers: Any, data: Any) -> List[Dict]:
    return await asyncio.gather(*[asyncio.create_task(_post(url, headers, data)) for url in urls])

def post(urls: List[HttpUrl], headers: Any, data: Any) -> List[Dict]:
    return asyncio.get_event_loop().run_until_complete(post_many(urls, headers, data))

async def _put(url: HttpUrl, headers: Any, data: Any) -> Dict:
    async with aiohttp.ClientSession() as session:
        async with session.put(url, headers=headers, data=data) as response:
            return await response.json()

async def put_many(urls: List[HttpUrl], headers: Any, data: Any) -> List[Dict]:
    return await asyncio.gather(*[asyncio.create_task(_put(url, headers, data)) for url in urls])
    
def put(urls: List[HttpUrl], headers: Any, data: Any) -> List[Dict]:
    return asyncio.get_event_loop().run_until_complete(put_many(urls, headers, data))
    
async def _delete(url: HttpUrl, headers: Any) -> Dict:
    async with aiohttp.ClientSession() as session:
        async with session.delete(url, headers=headers) as response:
            return await response.json()

async def delete_many(urls: List[HttpUrl], headers: Any) -> List[Dict]:
    return await asyncio.gather(*[asyncio.create_task(_delete(url, headers)) for url in urls])
    
def delete(urls: List[HttpUrl], headers: Any) -> List[Dict]:
    return asyncio.get_event_loop().run_until_complete(delete_many(urls, headers))

