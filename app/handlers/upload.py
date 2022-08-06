from fastapi import UploadFile, File, Request, APIRouter
from pydantic import HttpUrl
from app.models.schemas import Upload, Music
from app.config import AWS_S3_BUCKET, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION_NAME
from app.utils import uuid4
from botocore.exceptions import ClientError, BotoCoreError
from boto3 import Session

aws = Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION_NAME
)

s3 = aws.client('s3')


def upload_file(key:str,file: UploadFile)->HttpUrl:
    try:
        s3.upload_fileobj(
            file.file,
            AWS_S3_BUCKET,
            key,
            ExtraArgs={
                'ContentType': file.content_type,
                'ACL': 'public-read'
            }
        )
        
    except (BotoCoreError, ClientError) as e:
        raise e
    return f'https://{AWS_S3_BUCKET}.s3.amazonaws.com/{key}'

app = APIRouter()

@app.post('/upload/{size}')
async def upload_file_to_s3(request: Request, size:float, file: UploadFile = File(...)):
    sub=request.state.user.sub
    fid=uuid4().hex
    url = upload_file(f'{sub}/{fid}.{file.filename.split(".")[-1]}', file)
    return Upload(
        
        sub=sub,
        filename=file.filename,
        url=url,
        mimetype=file.content_type,
        size=size
    ).create()

@app.get('/upload')
async def get_uploads(request:Request):
    sub = request.state.user.sub
    items = Upload.find_many("sub",sub,100)
    response  = []
    for item in items:
        if item['mimetype'].startswith("image"):
            response.append(item)
    return response

@app.get('/music')
async def get_music(request:Request):
    sub = request.state.user.sub
    uploads = Upload.find_many("sub",sub,100)
    responses = []
    for upload in uploads:
        if upload['mimetype'].startswith('audio'):
            responses.append(upload)
    return responses
        
@app.post('/music')
async def upload_music(request:Request, music:Music):
    user = request.state.user
    sub = user.sub
    return Music(
        sub=sub,
        image=music.image,
        artist=music.artist,
        title=music.title,
        album=music.album,
        category=music.category,
        size=music.size,
        duration=music.duration,
        url=music.url
    ).save()