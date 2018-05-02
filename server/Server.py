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

connect("mongodb://vcm-3608.vm.duke.edu:27017/tag1.0.0")
app = Flask(__name__)
CORS(app)


@app.route("/api/images/<user_email>", methods=["GET"])
def app_get_user(user_email):
    """
    app_get_user Function takes the user_email input from the user, which
    help user to get his own images data from database with all the images
    information.
    :param email: str of the user email
    """
    try:
        user_data = mainfunction.print_user(user_email)

        result = {
            "email": user_email,
            "name": user_data.name,
            "images": user_data.images,
            "pro_images": user_data.pro_images,
            "success": 1
        }
    except pymodm.errors.DoesNotExist:
        result = {"success": 0}
        return jsonify(result), 200

    return jsonify(result), 200


def transfer_decode(image_str):
    """
    Remove the header of the images base64 bytes from front-end
    :param image_str: the input should be the base64 bytes of the image

    :returns: base64 string without data header

    :rtype: string
    """
    index = image_str.find(b',')
    image_str = image_str[index + 1:]
    image_type = str(image_str, 'utf-8')

    return image_type


def get_user(user_email):

    try:
        user_data = mainfunction.print_user(user_email)

        result = {
            "email": user_email,
            "name": user_data.name,
            "images": user_data.images,
            "pro_images": user_data.pro_images,
            "success": 1
        }
    except pymodm.errors.DoesNotExist:
        result = {"success": 0}
        return jsonify(result), 200

    return jsonify(result), 200


def aft_processing(filename, protype, proc_cmd):
    """
    After the specific image processing, this function process all the
    information regarding this image. After processing, this would return a
    image array including the corresponding information of the image,
    including: base64 str of the images, filename, id, process type, time
    stamp, time duration and processed histograms.
    :param filename: str of the name of the image
    :param protype: list of the post-processed image histogram
    :param proc_cmd: the str of process command which would be Reverse Video,
    Contrast Stretching, Log Compression and Histogram Equalization.

    :returns: a python array contains all the information fo the image after
    processing, including base64 str of the processed images, filename, id,
    process type, time stamp, time duration and processed histograms.

    :rtype: an array with string value
    """
    images = protype[4]

    image_type = str(images, 'utf-8')
    images_names = filename
    index = images_names.find('.')
    aft_name = images_names[:index] + ' ' + proc_cmd + images_names[index:]

    no_headerim = transfer_decode(images)
    image_function = Image_processing.Image(image_as_string=no_headerim)
    filetype = image_function.get_file_ext()

    time_stamp = datetime.datetime.now()
    time_duration = protype[5]

    red_his_str = str(protype[0])
    blue_his_str = str(protype[1])
    green_his_str = str(protype[2])
    x_vals_str = str(protype[3])

    pro_images_arr = [image_type, aft_name, images_names, filetype,
                      time_stamp, time_duration,
                      [red_his_str, blue_his_str, green_his_str, x_vals_str]]

    return pro_images_arr


@app.route("/api/images/create", methods=["POST"])
def create_user():
    """
    create_user Function takes the user_email input from the user including
    their setting email and their names. This function store and establish
    the user profile in the database.
    :param email: str of the user email
    :param name: str of the user name
    """
    r = request.get_json()

    email = r["email"]
    name = r["name"]

    mainfunction.create_user(email, name)
    result = {"sucess": "create user"}

    return jsonify(result), 200


def rm_strheader(images):
    """
    Remove the header of the images base64 string from front-end
    :param images: the input should be the base64 string of the image
    :raises TypeError: if input is not a string

    :returns: base64 string without data header

    :rtype: string
    """
    if type(images) is not str:
        raise TypeError('Error: imput should be a string')

    index = images.find(',')
    image_str = images[index + 1:]

    return image_str


@app.route("/api/images/upload", methods=["POST"])
def images_post():
    """
    images_post Function takes the input from the user such as email, images
    and the image filename, which performs the desired pre-processing on the
    image and saves as an array containing image information to the database.

    :param email: str of the user email
    :param images: base64 string of the images with headers from front-end
    :param filename: the str of images name as its specific identification
    """
    r = request.get_json()

    email = r["email"]
    images = r["images"]
    filename = r["filename"]

    noheader_images = rm_strheader(images)

    images_names = filename
    image_function = Image_processing.Image(image_as_string=noheader_images)
    filetype = image_function.get_file_ext()

    time_stamp = datetime.datetime.now()

    image_data = image_function.gather_data()
    image_size = image_data[1]

    histograms = Image_processing.histogram_data(noheader_images)
    red_his_str = str(histograms[0])
    blue_his_str = str(histograms[1])
    green_his_str = str(histograms[2])
    x_vals_str = str(histograms[3])

    images_arr = [images, images_names, images_names, filetype,
                  time_stamp, image_size,
                  [red_his_str, blue_his_str, green_his_str, x_vals_str]]
    mainfunction.add_images(email, images_arr)

    result = {"Success": "Cong! uploading successful"}

    return jsonify(result), 200


@app.route("/api/images/<email>/<filename>/process", methods=["POST"])
def pro_images_post(email, filename):
    """
    pro_images_post Function takes the input from the user such as email,
    images the image filename as identification and process type command,
    which performs the desired processing procedure on the image and saves
    as an array containing image information to the database.

    :param email: str of the user email
    :param process: process types of command
    :param images: base64 string of the images with headers from front-end
    :param filename: the str of images name as its specific identification
    """
    r = request.get_json()

    images_str = r["images"]
    image_pro_type = r["process"]

    filename_str = filename
    wk_images = rm_strheader(images_str)

    if image_pro_type == "Reverse Video":
        protype = Image_processing.reverse_video_complete(wk_images)
        images_info = aft_processing(filename_str, protype, image_pro_type)
        mainfunction.add_pro_images(email, images_info)
        result = {
            "Success": "Cong! Reverse Video completed"
        }
        return jsonify(result), 200

    elif image_pro_type == "Contrast Stretching":
        protype = Image_processing.contrast_stretching_complete(wk_images)
        images_info = aft_processing(filename_str, protype, image_pro_type)
        mainfunction.add_pro_images(email, images_info)
        result = {
            "Success": "Cong! Contrast Stretching completed"
        }
        return jsonify(result), 200

    elif image_pro_type == "Log Compression":
        protype = Image_processing.log_compression_complete(wk_images)
        images_info = aft_processing(filename_str, protype, image_pro_type)
        mainfunction.add_pro_images(email, images_info)
        result = {
            "Success": "Cong! Log Compression completed"
        }
        return jsonify(result), 200

    elif image_pro_type == "Histogram Equalization":
        protype = Image_processing.histogram_eq_complete(wk_images)
        images_info = aft_processing(filename_str, protype, image_pro_type)
        mainfunction.add_pro_images(email, images_info)
        result = {
            "Success": "Cong! Histogram Equalization completed"
        }
        return jsonify(result), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0")
