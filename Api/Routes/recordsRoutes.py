from bson import objectid
from fastapi import status, File, UploadFile
from Api.models.records import Record
from Api.Routes.utils import getResponse, riseHttpExceptionIfNotFound
from Api.helpers.save_picture import save_picture
from Api.Services import recordsService as service
from fastapi import APIRouter
import calendar
import time

recordRoutes = APIRouter()
base = '/data/'
UploadImage = f'{base}image-upload/'

_notFoundMessage = "Could not find record with the given Id."


@recordRoutes.get(base)
async def getAll():
    return await service.getAllRecord()


@recordRoutes.get(base+'{id}')
async def getById(id):
    return await resultVerification(id)   


@recordRoutes.get(base+'{long}'+'/'+'{lat}')
async def getByLongLat(long,lat):
    return await service.getByLongLat(long,lat)   

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



# Helpers

async def resultVerification(id: objectid) -> dict:
    result = await service.getById(id)
    await riseHttpExceptionIfNotFound(result, message=_notFoundMessage)
    return result
