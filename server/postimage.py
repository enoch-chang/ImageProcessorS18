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


def pre_processing():
    with open('rich.png', 'rb') as imageFile:
        images = base64.b64encode(imageFile.read())

    images = images
    #images_names = filename
    image_function = Image_processing.Image(image_as_string=images)
    filetype = image_function.get_file_ext()
    time_stamp = datetime.datetime.now()
    base64_str = transfer_decode(images)
    imgdata = base64.b64decode(base64_str)
    im = Image.open(io.BytesIO(imgdata))
    image_size = [im.size]
    #histograms = Image_processing.output_altered_histogram_data()
    images_arr = [images, images_names, image_names, filetype, time_stamp, image_size,
                  [[0,0], [0,0], [0,0], [0,0]]]
    print(images)
    return images_arr

images = pre_processing()