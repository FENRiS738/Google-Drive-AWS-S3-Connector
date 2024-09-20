from fastapi import FastAPI, HTTPException
from datetime import datetime
from pydantic import BaseModel
from .helpers import upload_to_s3

class UploadFile(BaseModel):
    file_id : str

app = FastAPI()

@app.post("/uplaod")
async def upload(upload_file : UploadFile):

    response = upload_to_s3(upload_file.file_id)

    return {
        "File Id" : upload_file.file_id,
        "Object Url" : response,
        "Created At" : datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    }