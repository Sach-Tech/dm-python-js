from bson import ObjectId
from Api.config.db import db
from Api.models.records import Record
from Api.Schemas.serializeObjects import serializeDict, serializeList
from exif import Image

async def getAllRecord() -> list:
    return serializeList(db.records.find())

async def getAllRecordCount():
    return db.records.count_documents({})

async def getById(id):
    return serializeDict(db.records.find_one({"_id": ObjectId(id)})) 


async def getByLongLat(long,lat) -> list:
    return serializeList(db.records.find({"longitude": long, "latitude" : lat}))    

async def getByHashTag(hashtag) -> list:
    return serializeList(db.records.find({"has_tag": hashtag}))    


async def InsertRecord(data: Record):
    result = db.records.insert_one(dict(data))
    return serializeDict(db.records.find_one({"_id": ObjectId(result.inserted_id)}))

async def updateRecord(id, data: Record) -> bool:
    db.records.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(data)})
    return True

async def savePicture(id, imageUrl: str) -> bool:
    db.records.find_one_and_update({"_id": ObjectId(id)}, {"$set": { "imageUrl": imageUrl }})
    return True


async def deleteRecord(id) -> bool:
    db.records.find_one_and_delete({"_id": ObjectId(id)})
    return True

def getImageMetaDataDetails(imageUrl: str):
    with open(imageUrl, 'rb') as image_file:
         my_image = Image(image_file)
    return my_image;





