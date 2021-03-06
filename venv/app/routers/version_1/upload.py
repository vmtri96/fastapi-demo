from fastapi import APIRouter, File, UploadFile, Depends
from pathlib import Path
import shutil
import os

from app.dependencies.verify_user import is_store


router = APIRouter()



@router.post('/up_product_image', dependencies=[Depends(is_store)])
async def up_image(file: UploadFile = File(...), user_id: int = None):
    file_object = file.file
    folder = f'./static/images/{user_id}/'
    if not os.path.exists(folder):
        Path(folder).mkdir(parents=True, exist_ok=True)
    upload_folder = open(os.path.join(folder, file.filename), 'wb+')
    shutil.copyfileobj(file_object, upload_folder)
    upload_folder.close()
    return {"file_url": f'/static/images/{user_id}/' + file.filename}