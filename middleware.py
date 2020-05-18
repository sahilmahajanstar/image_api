from PIL import Image
from PIL.ExifTags import TAGS
import os
import jwt

def check_extension(filename):
    ext=os.path.splitext(filename)[-1].lower()
    if ext=='.png'or ext=='.jpg' or ext=='.jpeg':
        return True
    else:
        return False

def generate_token(key,count,exp):
    return jwt.encode({ 'count':count,
            'apikey':key, 
            'exp':exp
            },
            'apirate',
            algorithm='HS256')

def get_metadata(imagename):
   # return metada of images
    print(imagename)
    metadata={}
    image = Image.open(imagename)
    metadata["width"]=image.width
    metadata["height"]=image.height
    metadata["size"]=image.size
    metadata["format"]=image.format
    metadata["url"]=f'http://127.0.0.1:5000{image.filename[1:]}'
    print(metadata)
    return metadata