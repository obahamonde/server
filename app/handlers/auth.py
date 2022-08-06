from pydantic import HttpUrl
from app.config import environ
from app.lib import net
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import Callable
from app.models.schemas import User
import asyncio

AUTH0_DOMAIN = environ.get('AUTH0_DOMAIN')
AUTH0_CLIENT_ID = environ.get('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = environ.get('AUTH0_CLIENT_SECRET')
AUTH0_API_AUDIENCE = environ.get('AUTH0_API_AUDIENCE')
AUTH0_API_SCOPE = environ.get('AUTH0_API_SCOPE')
AUTH0_API_GRANT_TYPE = environ.get('AUTH0_API_GRANT_TYPE')


async def user_info(token: str):
    url:str = f'https://{environ.get("AUTH0_DOMAIN")}/userinfo'
    headers = {'Authorization': f'Bearer {token}'}
    return await net._fetch(url, headers)

def user(request:Request):
    return request.state.user

def use_auth(app:FastAPI)->FastAPI:
    @app.middleware('http')
    async def auth_client(request:Request, call_next:Callable):
        if request.url.path.find('/api/') == 0:
            try:
                token = request.headers.get('Authorization').split(' ')[1]
                print(token)
                request.state.user = User(**await user_info(token))
            except Exception as e:
                raise e
        return await call_next(request)
    @app.get('/{token}')
    async def get_user(token: str):
        return User(**await user_info(token)).save()
    app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])
    return app