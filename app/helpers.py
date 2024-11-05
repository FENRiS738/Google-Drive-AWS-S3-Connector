import os
import gdown
from gdown import exceptions
from fastapi import HTTPException

from .connections import connectToAwsS3

def download_file_from_google_drive(file_id):
    try:
        file_url = f"https://drive.google.com/uc?export=view&id={file_id}"
        file = gdown.download(file_url, quiet=False)
        return file
    except  exceptions.FileURLRetrievalError as e:
        if os.path.exists(file):
            os.remove(file)
        raise HTTPException(403, detail=f"Unable to download file from Google Drive: {str(e)}") from e
    except Exception as ex:
        if os.path.exists(file):
            os.remove(file)
        raise HTTPException(500, detail=f"Unexpected error during file upload: {str(ex)}") from ex




def upload_to_s3(file_id):

    file = download_file_from_google_drive(file_id)

    object_key = os.path.basename(file)
    bucket_name = 'test_bucket'
    s3 = connectToAwsS3()
    try: 
        s3.upload_file(file, bucket_name, object_key)
        response = s3.generate_presigned_url('get_object',
                                            Params={'Bucket': bucket_name, 'Key': object_key})
        os.remove(file)

        return response
    except FileNotFoundError as fx:
        if os.path.exists(file):
            os.remove(file)
        raise HTTPException(404, detail=f"File not found: {str(fx)}") from fx
    except Exception as ex:
        if os.path.exists(file):
            os.remove(file)
        raise HTTPException(500, detail=f"Unexpected error during file upload: {str(ex)}") from ex
