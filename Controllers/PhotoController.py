from PIL import Image
import PIL.ImageOps, io
from fastapi import APIRouter, File, Form, UploadFile
from fastapi.responses import StreamingResponse

controllerName = "photo"
photoController = APIRouter()


@photoController.post(f'/{controllerName}/')
async def photoGet(file: UploadFile = File(...)):
    request_object_content = await file.read()
    image = Image.open(io.BytesIO(request_object_content))
    inverted = PIL.ImageOps.invert(image)
    img_byte_arr = io.BytesIO()
    inverted.save(img_byte_arr, 'jpeg')
    img_byte_arr.seek(0)
    file.close()
    return StreamingResponse(img_byte_arr, media_type="image/jpeg")

