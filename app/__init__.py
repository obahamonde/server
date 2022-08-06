from fastapi import FastAPI
from app.handlers.auth import use_auth
from app.handlers.upload import app as upload_app
from app.handlers.email import app as email_app
from app.handlers.crawl import app as crawl_app
from app.handlers.yt import app as yt_app
from app.utils import log

def app():
    _ = use_auth(FastAPI())
    _.include_router(upload_app, prefix='/api', tags=['upload'])
    _.include_router(email_app, tags=['email'])
    _.include_router(crawl_app, tags=['crawl'])
    _.include_router(yt_app, tags=['yt'])
    log("See the docs at: http://localhost:8000/docs ")    
    return _

