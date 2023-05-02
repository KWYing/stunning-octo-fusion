import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.encoders import jsonable_encoder
from dotenv import load_dotenv

load_dotenv()

from webparser import get_info

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/get/{sku}")
async def get_video_info(sku: str):
    try:
        dic = get_info.get_video_info(sku)
    except:
        dic = {}
    is_dmm = True if get_info.split_sku(
        sku)[1] not in ['abp', 'abw'] else False
    try:
        get_info.get_images(sku, is_dmm=is_dmm)
        dic['cover_image'] = f"{sku}" 
    except:
        dic['cover_image'] = ""
    samples = {}
    for i in range(1,13):
        try:
            get_info.get_images(sku, is_dmm, index=i)
            samples['img-'+str(i)] = f"{sku}?n={i:02d}"
        except:
            samples['img-'+str(i)] = ""
    dic['sample_images'] = samples
    return jsonable_encoder(dic)

@app.get("/images/{sku}")
async def display_cover_image(sku:str, n:int=None):
    base = os.getenv('IMAGE_PATH')
    avid, _ , _ = get_info.split_sku(sku)
    if n:
        link = os.path.join(base, os.path.join( 
            avid, f"{avid}-{n:02d}.jpg"
        ))
    else:
        link = os.path.join(base, os.path.join(
            avid, f"{avid}-cover.jpg"
        ))
    return FileResponse(link, media_type='image/jpg')