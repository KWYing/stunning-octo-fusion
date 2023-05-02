from fastapi import FastAPI
from fastapi.responses import FileResponse
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
    dic['cover_image'] = get_info.get_images(sku, is_dmm=is_dmm)
    samples = {}
    for i in range(1,13):
        samples['img-'+str(i)] = get_info.get_images(sku, is_dmm, index=i)
    dic['sample_image'] = samples
    return dic

@app.get("/image/{path}")
async def display_cover_image(path:str):
    link = "images/abw00003/abw00003-cover.jpg"
    return FileResponse(link, media_type='image/jpg')