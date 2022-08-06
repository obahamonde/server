import pulumi
import pulumi.automation as a
from pulumi_aws import s3
from json import dumps

def ensure_plugins():
    ws = a.LocalWorkspace()
    ws.install_plugin("aws","v4.0.0")

def s3_program(content:str):
    site_bucket = s3.Bucket(
        "s3-site-bucket",website=aws.s3.BucketWebsiteArgs(
            index_document="index.html")
    )
    index_content= content
    s3.BucketObject(
        "index",
        bucket=site_bucket.id,
        content=index_content,
        key="index.html",
        content_type="text/html; charset=utf-8",
    )

    # Set the access policy for the bucket so all objects are readable
    s3.BucketPolicy(
        "bucket-policy",
        bucket=site_bucket.id,
        policy=site_bucket.id.apply(
            lambda id:dumps(
                {
                    "Version": "2012-10-17",
                    "Statement": {
                        "Effect": "Allow",
                        "Principal": "*",
                        "Action": ["s3:GetObject"],
                        "Resource": [f"arn:aws:s3:::{id}/*"],
                    },
                }
            )
        ),
    )
    pulumi.export("website_url", site_bucket.website_endpoint)
    pulumi.export("website_content", index_content)

