import os
import json

from clarifai import rest
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage


# run these lines to access the Mirror Mirror application
os.environ["CLARIFAI_APP_ID"] = "ldgNgiUGMGdgm9M2iGKRPQxGT3s-Ds9j2wtuZODX"
os.environ["CLARIFAI_APP_SECRET"] = "NkNVKSx41vBwAAqMe9OHAJlliFfrb3xMiIr8zzAq"
# getting started guide: https://developer.clarifai.com/guide/#getting-started
# visit https://preview.clarifai.com for UI (if logged into Caroline's account)
# user: ruoyi.lin@gmail.com pass: uthacks4

app = ClarifaiApp()

# set default model
# model = app.models.get('general-v1.3')

# make a new model (can also do on preview site)
# model = app.models.create('ladies_clothes2', concepts=['shirt', 'pants', 'skirt', 'dress'])
# print(model)


"""
image_filepath = 'C:\\Users\\Caroline\\Desktop\\clothing_tests\\'
images = os.listdir(image_filepath)

for image in images:
    image_path = image_filepath + image
    img = ClImage(file_obj=open(image_path, 'rb'))

    # add image to application db
    json_image = app.inputs.create_image_from_filename(image_path)
    # print(phi)
    # print(json.dumps(phi))
"""

