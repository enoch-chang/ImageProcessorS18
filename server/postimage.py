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


#def rm_strheader(images):
#    print(type(images))
#    index = images.find(',')
#    image_str = images[index + 1:]

#    return image_str

def rm_strheader(images):
    #print(type(images))
    index = images.find(b',')
    image_str = images[index + 1:]
    #print(type(image_str))
    test = str(image_str, 'utf-8')
    #print(type(test))
    return test

def encode_string(filename, file_ext):
    with open(filename + file_ext, 'rb') as imageFile:
        string = base64.b64encode(imageFile.read())
    return string


with open('coach.jpeg', 'rb') as imageFile:
    images = base64.b64encode(imageFile.read())


def pre_processing():
    with open('coach.jpeg', 'rb') as imageFile:
        images = base64.b64encode(imageFile.read())
    #images64 = images
    #images_names = filename
    image_function = Image_processing.Image(image_as_string=images)
    filetype = image_function.get_file_ext()
    time_stamp = datetime.datetime.now()
    #base64_str = images[images.find(",")+1:]
    base64_bytes = rm_strheader(images)
    #base64result = images(images.indexOf(',') + 1)
    imgdata = base64.b64decode(base64_bytes)
    im = Image.open(io.BytesIO(imgdata))
    image_size = im.size
    #histograms = Image_processing.histogram_data(images)
    images_arr = [base64_bytes, None, None, filetype,
                  time_stamp, image_size, None]
    print(base64_bytes)
    # print(images_arr)
    return images_arr



#image = pre_processing()
file_jpeg = open('image_test_png.txt')
jpeg_string = file_jpeg.read()
#con = "data:image/jpeg;base64," + jpeg_string
#image_function = Image_processing.Image(image_as_string=jpeg_string)
#image_data = image_function.gather_data()
#dimen = image_data[1]
#print(dimen)
#a = Image_processing.contrast_stretching_complete(jpeg_string)
#red_data = a[0]
#a = rm_strheader(con)
#print(con)
#print(a)
b = Image_processing.histogram_data(jpeg_string)
#print(jpeg_string)
a = b[0]
print(a.tolist())
#print(range(0, 256))
