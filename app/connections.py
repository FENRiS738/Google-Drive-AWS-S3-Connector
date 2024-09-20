import os
import boto3
from botocore import  exceptions

from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

def connectToAwsS3():
    try: 
        s3 = boto3.client(
        's3',
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name = os.getenv("REGION_NAME")
        )
        return s3
    except exceptions.ClientError as cx:
        if cx.response['Error']['Code'] == 'AccessDenied':
            raise HTTPException(403, detail="Access to the S3 bucket is denied") from cx
        else:
            raise HTTPException(500, detail=f"Failed to upload to S3: {str(ex)}") from ex
    except exceptions.NoCredentialsError as ncx:
        raise HTTPException(401, detail="AWS credentials not found") from ncx
    except Exception as ex:
        raise HTTPException(500, detail=f"Unexpected error during file upload: {str(ex)}") from ex
