from app.models.schemas import Product, User, Upload
from app.lib.fql import FQLModel as Q
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

app = APIRouter()

