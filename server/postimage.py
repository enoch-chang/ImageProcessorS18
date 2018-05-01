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

def rm_strheader(images):
    print(type(images))
    index = images.find(b',')
    image_str = images[index + 1:]
    return image_str

def encode_string(filename, file_ext):
    with open(filename + file_ext, 'rb') as imageFile:
        string = base64.b64encode(imageFile.read())
    return string

def pre_processing():
    with open('rich.PNG', 'rb') as imageFile:
        images = base64.b64encode(imageFile.read())

    images64 = images
    #images_names = filename
    image_function = Image_processing.Image(image_as_string=images)
    filetype = image_function.get_file_ext()
    time_stamp = datetime.datetime.now()
    #base64_str = images[images.find(",")+1:]
    base64_str = rm_strheader(images)
    #base64result = images(images.indexOf(',') + 1)
    imgdata = base64.b64decode(images)
    im = Image.open(io.BytesIO(imgdata))
    image_size = im.size
    histograms = Image_processing.histogram_data(base64_str)
    images_arr = [images64, None, None, filetype, time_stamp, image_size, histograms]
    print(images)
    print(images_arr)
    return images_arr

imagesy = pre_processing()