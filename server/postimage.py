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

with open('coach.jpeg', 'rb') as imageFile:
    images = base64.b64encode(imageFile.read())
def get_hist_data(string):
    red_hist, blue_hist, green_hist, x_vals = Image_processing.histogram_data(string)
    return [red_hist, blue_hist, green_hist, x_vals]

def pre_processing():
    with open('coach.jpeg', 'rb') as imageFile:
        images = base64.b64encode(imageFile.read())
    red_hist, blue_hist, green_hist, x_vals = Image_processing.histogram_data(images)
    images64 = images
    images_names = filename
    image_function = Image_processing.Image(image_as_string=images)
    filetype = image_function.get_file_ext()
    time_stamp = datetime.datetime.now()
    base64_str = images[images.find(",")+1:]
    base64_str = rm_strheader(images)
    base64result = images(images.indexOf(',') + 1)
    imgdata = base64.b64decode(images)
    im = Image.open(io.BytesIO(imgdata))
    image_size = im.size
    histograms = Image_processing.histogram_data(images)
    images_arr = [images64, None, None, filetype, time_stamp, image_size, histograms]
    print(images)
    print(images_arr)
    return images_arr

file_jpeg = open('image_test_png.txt')
jpeg_string = file_jpeg.read()
a = Image_processing.contrast_stretching_complete(jpeg_string)
red_data = a[0]
b = Image_processing.histogram_data(jpeg_string)
print(b[0])
print(range(0,256))