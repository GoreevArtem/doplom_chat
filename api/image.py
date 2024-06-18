import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from pathlib import Path

from utils.JWT import JWTBearer

router = APIRouter(
    prefix='/images',
    tags=['images'],
)

UPLOAD_DIRECTORY = "./uploads"

# Убедитесь, что директория для загрузки существует
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

@router.post("/upload-photo/", dependencies=[Depends(JWTBearer())])
async def upload_photo(file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
    with open(file_location, "wb") as f:
        f.write(file.file.read())
    return {"info": f"file '{file.filename}' saved at '{file_location}'"}

@router.get("/get-photo/{filename}", dependencies=[Depends(JWTBearer())])
async def get_photo(filename: str):
    file_location = os.path.join(UPLOAD_DIRECTORY, filename)
    if os.path.exists(file_location):
        return FileResponse(file_location)
    return {"error": "File not found"}