from fastapi import APIRouter
from boto3 import Session
from app.config import AWS_S3_BUCKET, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION_NAME
from app.models.schemas import Email

app = APIRouter()

ses = Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION_NAME
).client("ses")

@app.post("/email")
async def send_email_with_ses(email: Email):
    email.save()
    ses.send_email(
        Source=environ.get("AWS_SES_SOURCE"),
        Destination={
            "ToAddresses": [environ.get("AWS_SES_SOURCE")]
        },
        Message={
            "Subject": {
                "Data": f"email from {email.subject}<{email.from_}>"
            },
            "Body": {
                "Text": {
                    "Data": email.body
                }
            }
            
        }
    )   
    return {"message": "Email sent"}