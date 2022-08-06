from pydantic import HttpUrl, EmailStr, Field
from typing import Optional, Union, Any, List, Dict
from app.lib.fql import FQLModel as Q
from app.utils import get_avatar, uid



class User(Q):
    sub: str = Field(...)
    given_name: Optional[str] = Field()
    family_name: Optional[str] = Field()
    nickname: Optional[str] = Field()
    name: Optional[str] = Field()
    picture: Optional[Union[HttpUrl, str]] = Field(default_factory=get_avatar)
    locale: Optional[Union[str, None]] = Field()
    updated_at: Optional[str] = Field()
    email: Optional[Union[EmailStr, str, None]] = Field(index=True)
    email_verified: Optional[Union[bool, str]] = Field()

class Upload(Q):
    id: str = Field(default_factory=uid, index=True)
    sub: str = Field(..., index=True)
    filename: Optional[str] = Field()
    size: Optional[float] = Field()
    mimetype: Optional[str] = Field()
    url: Optional[Union[HttpUrl, str]] = Field()

class Email (Q):
    from_:Union[EmailStr, str, Any] = Field(index=True, default="oscar.bahamonde.dev@gmail.com")
    to:Union[EmailStr, str, Any] = Field(index=True, default="oscar.bahamonde.dev@gmail.c")
    subject:Optional[str] = Field()
    body:Optional[str] = Field()
    
    
class Product(Q):
    sub: str = Field(..., index=True)
    title: str = Field(...)
    subtitle: Optional[str] = Field()
    description: Optional[str] = Field()
    tags:Optional[List[str]] = Field()
    price:float=Field(...)
    uploads:List[HttpUrl] = Field(default_factory=list)
    
   
class Music(Q):
    image:HttpUrl = Field(default="https://mypublics3bucket.s3.amazonaws.com/google-oauth2%7C110452235728654321644/bd589a8378334121bd1316bf023125ea.jpg")
    artist:Optional[str] = Field()
    title:Optional[str] = Field()
    album:Optional[str] = Field()
    category:Optional[str] = Field()
    size:Optional[str] = Field()
    duration:Optional[str] = Field()
    url:Optional[Union[HttpUrl,str]] = Field()