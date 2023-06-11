from bson import objectid
from fastapi import status, File, UploadFile
from Api.models.records import Record
from Api.Routes.utils import getResponse, riseHttpExceptionIfNotFound
from Api.helpers.save_picture import save_picture
from Api.Services import recordsService as service
from fastapi import APIRouter
import calendar
import time
import datetime

recordRoutes = APIRouter()
base = '/data/'
UploadImage = f'{base}image-upload/'

_notFoundMessage = "Could not find record with the given Id."

@recordRoutes.get(base)
async def getAll():
    return await service.getAllRecord()

@recordRoutes.get('/dataCount')
async def getAllRecordCount():
    return await service.getAllRecordCount()
    
@recordRoutes.get(base+'{id}')
async def getById(id):
    return await resultVerification(id)   


@recordRoutes.get(base+'{long}'+'/'+'{lat}')
async def getByLongLat(long,lat):
    return await service.getByLongLat(long,lat) 

@recordRoutes.get('/record/'+'{hashtag}')
async def getByHashTag(hashtag):
    return await service.getByHashTag(hashtag)   

@recordRoutes.post(base)
async def InsertRecord(data: Record):
    return await service.InsertRecord(data)


@recordRoutes.put(base+'{id}', status_code=status.HTTP_204_NO_CONTENT)
async def updateRecord(id, data: Record):
    await resultVerification(id)
    done : bool = await service.updateRecord(id,data);
    return getResponse(done, errorMessage="An error occurred while editing the information.")


@recordRoutes.delete(base+'{id}', status_code=status.HTTP_204_NO_CONTENT)
async def deleteRecord(id):
    await resultVerification(id)
    done : bool = await service.deleteRecord(id);
    return getResponse(done, errorMessage="There was an error.")   


@recordRoutes.post(UploadImage+'{id}', status_code=status.HTTP_204_NO_CONTENT)
async def uploadImage(id: str, file: UploadFile = File(...)):
    result = await resultVerification(id)
    current_GMT = time.gmtime()
    time_stamp = calendar.timegm(current_GMT)
    imageUrl = save_picture(file=file, folderName='records', fileName=str(time_stamp))
    done = await service.savePicture(id, imageUrl)
    return getResponse(done, errorMessage="An error occurred while saving user image.")


@recordRoutes.post("/uploadPicture/"+'{hastag}', status_code=201)
async def saveContent(hastag: str, file: UploadFile = File(...)):
    current_GMT = time.gmtime()
    time_stamp = calendar.timegm(current_GMT)
    imageUrl = save_picture(file=file, folderName='records', fileName=str(time_stamp))
    imageData = service.getImageMetaDataDetails(imageUrl)
    imageUrl  = imageUrl
    if imageData._has_exif:
        longitude = str(imageData.gps_longitude) if hasattr(imageData, 'gps_longitude') else "-"
        latitude = str(imageData.gps_latitude) if hasattr(imageData, 'gps_latitude') else "-"
        altitude = str(imageData.gps_altitude) if hasattr(imageData, 'gps_altitude') else "-"
        created_at = str(imageData.datetime_original) if hasattr(imageData, 'datetime_original') else datetime.datetime.now().strftime("%m:%d:%Y %H:%M:%S")
        updated_at = str(imageData.datetime_original) if hasattr(imageData, 'datetime_original') else datetime.datetime.now().strftime("%m:%d:%Y %H:%M:%S")
    else:
        longitude = "-"
        latitude = "-"
        altitude = "-"
        created_at = datetime.datetime.now().strftime("%m:%d:%Y %H:%M:%S")
        updated_at = datetime.datetime.now().strftime("%m:%d:%Y %H:%M:%S")
    data = Record(longitude = longitude, latitude = latitude, altitude = altitude, has_tag = hastag, imageUrl = imageUrl, created_at = created_at, updated_at = updated_at);
    initialResult = await service.InsertRecord(data)
    return initialResult


# Helpers

async def resultVerification(id: objectid) -> dict:
    result = await service.getById(id)
    await riseHttpExceptionIfNotFound(result, message=_notFoundMessage)
    return result
