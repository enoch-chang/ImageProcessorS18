from flask import Flask, jsonify, request
from flask_cors import CORS
import pymodm
from pymodm import connect
import numpy as np
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


def decode_image(image_bytes, image_id):
    with open(image_id, 'wb') as images:
        images.write(base64.b64decode(image_bytes))



def pre_processing(noheader_images, filename, images):
    """
    Do the pre-processing method for images that are about to be uploaded.
    After processing, this would return a image array including the corres
    -ponding information of the image, including: base64 str of the images,
    filename, id, filetype, time stamp, image size and unaltered
    histograms.
    :param images: base64 str of the image
    :param filename: str of the name of the image
    """
    images_names = filename
    image_function = Image_processing.Image(image_as_string=noheader_images)
    filetype = image_function.get_file_ext()
    time_stamp = datetime.datetime.now()
    imgdata = base64.b64decode(noheader_images)
    im = Image.open(io.BytesIO(imgdata))
    image_size = im.size
    histograms = Image_processing.histogram_data(noheader_images)
    images_arr = [images, images_names, images_names, filetype,
                  time_stamp, image_size, [[0,0],[0,0],[0,0],[0,0]]]

    return images_arr





    
file = open('image_test_jpeg.txt', 'r') 
string = file.read()
histograms = Image_processing.histogram_data(string)
print(histograms)
