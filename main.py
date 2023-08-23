"""Simple REST api using fastapi"""
import os
from typing import List
from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import FileResponse
from pymongo import MongoClient, DESCENDING

from dotenv import load_dotenv

from webparser.get_info import get_video_info
from database.schema import InfoResponse, ActressResponse

load_dotenv()


# MongoDB
client = MongoClient(os.getenv('MONGODB'))
db = client['av']


app = FastAPI()


@app.get("/")
async def root():
    """Home Page"""
    return {'message': 'Welcome'}


@app.get("/all", response_model=List[InfoResponse])
async def get_all():
    """Get all items"""
    items = db['info'].find().sort('release_date', DESCENDING)
    return [InfoResponse(id=str(item['_id']), **item) for item in items]


@app.get("/get/{sku}", response_model=InfoResponse)
async def get_info(sku: str):
    """Get info from database"""
    item = db['info'].find_one({"sku": sku})
    if item is None:
        return HTTPException(status_code=404, detail="Image not found")
    return InfoResponse(id=str(item['_id']), **item)


@app.get("/get-actress", response_model=List[ActressResponse])
async def get_all_actress():
    """Get all actress in database"""
    acts = db['actress'].find()
    return [ActressResponse(id=str(act['_id']), **act) for act in acts]


@app.get("/actress/{name}", response_model=List[InfoResponse])
async def get_actress(name: str):
    """Get all actress items from database"""
    acts = db['actress'].find_one({"name": name})
    if acts is None:
        return HTTPException(status_code=404, detail="Actress not found")
    videos = []
    for sku in acts["videos"]:
        item = db['info'].find_one({"sku": sku})
        videos.append(
            InfoResponse(id=str(item['_id']), **item)
            )
    return videos


@app.post("/insert/{sku}", response_model=InfoResponse)
async def insert_info(sku: str):
    """Insert info to database"""
    item = db['info'].find_one({"sku": sku})
    if item is not None:
        return HTTPException(status_code=505, detail="Item already in database")
    # Get video info
    item_dict = get_video_info(sku)
    # Add actress
    actress = item_dict['actress']
    if ',' in actress:
        item_dict['actress'] = [_.strip() for _ in actress.split(',')]
    else:
        item_dict['actress'] = [actress]
    # Add video to actress
    for actress in item_dict['actress']:
        act = db['actress'].find_one({"name": actress})
        if act is not None:
            db['actress'].update_one({"name": actress}, {"$push":{"videos": sku}}, upsert=True)
        else:
            db['actress'].insert_one({"name": actress, "videos": [sku]})
    # Once actress is added add video info
    item_id = db['info'].insert_one(item_dict).inserted_id
    item = db['info'].find_one({'_id': item_id})
    return InfoResponse(id=str(item['_id']), **item)


@app.get("/image/{sku}")
async def show_cover_image(sku: str):
    """Show cover image"""
    item = db['info'].find_one({"sku": sku})
    if item is None:
        return HTTPException(status_code=404, detail="Image not found")
    img_path = item['cover_image']
    return FileResponse(img_path, media_type='image/jpeg')


# @app.delete("/delete/{sku}")
# async def delete_item(sku: str):
#     """Delete an item"""
#     item = db['info'].find_one({'sku': sku})
#     if item is None:
#         return HTTPException(status_code=404, detail="Item not found")
#     db['info'].delete_one({'sku': sku})
#     return Response(status_code=200)


@app.delete("/reset")
async def reset_database():
    """Delete all items to reset database"""
    db['info'].delete_many({})
    db['actress'].delete_many({})
    return Response(status_code=200)
