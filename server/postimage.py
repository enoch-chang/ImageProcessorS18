from flask import Flask, jsonify, request
from flask_cors import CORS
import pymodm
from pymodm import connect
import mainfunction
import numpy as np
import models
import datetime
import time
import Image_processing
import io
import base64
import PIL
from PIL import Image

def transfer_decode(image_str):
    index = image_str.find(',')
    image_str = image_str[index + 1:]
    image_bytes = image_str.encode()
    return image_bytes

def pre_processing():
    with open('rich.png', 'rb') as imageFile:
        images = base64.b64encode(imageFile.read())

    images = images
    #images_names = filename
    image_function = Image_processing.Image(image_as_string=images)
    filetype = image_function.get_file_ext()
    time_stamp = datetime.datetime.now()
    #base64_str = transfer_decode(images)
    imgdata = base64.b64decode(images)
    im = Image.open(io.BytesIO(imgdata))
    image_size = [im.size]
    #histograms = Image_processing.histogram_data(images)
    images_arr = [images, None, None, filetype, time_stamp, image_size, None]
    print(images)
    print(images_arr)
    return images_arr

images = pre_processing()