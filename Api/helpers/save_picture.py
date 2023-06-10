import os
from uuid import uuid4
from PIL import Image
import shutil


static = 'static'

def save_picture(file, folderName: str = '', fileName: str = None):
    randon_uid = str(uuid4())
    _, f_ext = os.path.splitext(file.filename)
    
    picture_name = (randon_uid if fileName==None else fileName.lower().replace(' ', '')) + f_ext 

    path = os.path.join(static,folderName)
    if not os.path.exists(path):
        os.makedirs(path)
        
    picture_path = os.path.join(path,picture_name)

    #new
    with open(picture_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    #new end
    #output_size = (600,480)
    #img = Image.open(file.file)
    
    #img.thumbnail(output_size)
    #img.save(picture_path)
    
    return f'{static}/{folderName}/{picture_name}'