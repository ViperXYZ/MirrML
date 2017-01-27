import os
import json

from clarifai import rest
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage


os.environ["CLARIFAI_APP_ID"] = "fXM043GazV7t45lQSFQpw3Jj8NIuRWO4PEVNtzBS"
os.environ["CLARIFAI_APP_SECRET"] = "mKsHrQ7CKaHXROyeNfZlaDNZ61W2BH3jjIJ9NJ_7"


app = ClarifaiApp()


# get the custom model 'modelv2'
model = app.models.get('Style-Categorizer')
tags = ["coat"]

# add the tag to concepts.
model.add_concepts(tags)

# use this file to add all images from a directory with appropriate training tags

image_filepath = 'C:\\Users\\nvara\\Desktop\\uofthacks4\\'
images = os.listdir(image_filepath)

failed = 0
total = 0
for image in images:
    image_path = image_filepath + image
    # add the selected image to the application with tags
    # batch downloader keeps corrupting download files so...
    try:
        json_image = app.inputs.create_image_from_filename(image_path, concepts=tags)
    except Exception as e:
        print("the image probably wasn't formatted correctly.")
        failed = failed + 1
    total = total + 1
    json_image = app.inputs.create_image_from_filename(image_path, concepts=tags)

print("failed: {}, total {}".format(failed, total))