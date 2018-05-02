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

connect("mongodb://vcm-3608.vm.duke.edu:27017/fp_images")
app = Flask(__name__)
CORS(app)


@app.route("/api/images/<user_email>", methods=["GET"])
def app_get_user(user_email):

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
    index = image_str.find(b',')
    image_str = image_str[index + 1:]
    image_type = str(image_str, 'utf-8')
    return image_type


def decode_image(image_bytes, image_id):
    with open(image_id, 'wb') as images:
        images.write(base64.b64decode(image_bytes))


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
    image_data = image_function.gather_data()
    image_size = image_data[1]
    #histograms = Image_processing.histogram_data(noheader_images)
    images_arr = [images, images_names, images_names, filetype,
                  time_stamp, image_size, [[0,0],[0,0],[0,0],[0,0]]]

    return images_arr


def aft_processing(filename, protype):
    """
    After the specific image processing, this function process all the
    information regarding this image. After processing, this would return a
    image array including the corresponding information of the image,
    including: base64 str of the images, filename, id, rocess type, time
    stamp, time duration and processed histograms.
    :param images: base64 str of the image
    :param filename: str of the name of the image
    :param protype: list of the post-processed image histogram
    """
    images = protype[4]
    image_type = str(images, 'utf-8')
    images_names = filename
    no_headerim = transfer_decode(images)
    image_function = Image_processing.Image(image_as_string=no_headerim)
    filetype = image_function.get_file_ext()
    time_stamp = datetime.datetime.now()
    time_duration = protype[5]
    red_his_str = str(protype[0].tolist)
    blue_his_str = str(protype[1].tolist)
    green_his_str = str(protype[2].tolist)
    x_vals_str = str(protype[3].tolist)
    pro_images_arr = [image_type, images_names, images_names, filetype,
                      time_stamp, time_duration,
                      [red_his_str, blue_his_str, green_his_str, x_vals_str]]

    return pro_images_arr


@app.route("/api/images/create", methods=["POST"])
def create_user():

    r = request.get_json()

    email = r["email"]
    name = r["name"]

    mainfunction.create_user(email, name)
    result = {"sucess": "create user"}

    return jsonify(result), 200


def rm_strheader(images):
    index = images.find(',')
    image_str = images[index + 1:]

    return image_str


@app.route("/api/images/upload", methods=["POST"])
def images_post():

    r = request.get_json()

    email = r["email"]
    images = r["images"]
    filename = r["filename"]

    #for im, nm in zip(images, filename):
    noheader_images = rm_strheader(images)
    images_names = filename
    image_function = Image_processing.Image(image_as_string=noheader_images)
    filetype = image_function.get_file_ext()
    time_stamp = datetime.datetime.now()
    image_data = image_function.gather_data()
    image_size = image_data[1]
    histograms = Image_processing.histogram_data(noheader_images)
    red_his_str = str(histograms[0].tolist())
    blue_his_str = str(histograms[1].tolist())
    green_his_str = str(histograms[2].tolist())
    x_vals_str = str(histograms[3].tolist())
    images_arr = [images, images_names, images_names, filetype,
                  time_stamp, image_size,
                  [red_his_str, blue_his_str, green_his_str, x_vals_str]]
    #images_info = pre_processing(no_header_im, filename, images)
    mainfunction.add_images(email, images_arr)
    result = {"success": "Cong! uploading successful"}

    return jsonify(result), 200


@app.route("/api/images/<email>/<filename>/process", methods=["POST"])
def pro_images_post_his(email, filename):

    r = request.get_json()

    images_str = r["images"]
    image_pro_type = r["process"]
    filename_str = filename
    wk_images = rm_strheader(images_str)
    if image_pro_type == "Reverse Video":
        protype = Image_processing.reverse_video_complete(wk_images)
        images_info = aft_processing(filename_str, protype)
        mainfunction.add_pro_images(email, images_info)
        result = {
            "hope this works": "Yes it works"
        #    "images": images,
        #    "pro_images": images_info[4]
        }
        return jsonify(result), 200

    elif image_pro_type == "Constrast Stretching":
        protype = Image_processing.contrast_stretching_complete(wk_images)
        images_info = aft_processing(filename_str, protype)
        mainfunction.add_pro_images(email, images_info)
        result = {
            "hope this works": "Yes it works"
            #    "images": images,
            #    "pro_images": images_info[4]
        }
        return jsonify(result), 200

    elif image_pro_type == "Log Compression":
        protype = Image_processing.log_compression_complete(wk_images)
        images_info = aft_processing(filename_str, protype)
        mainfunction.add_pro_images(email, images_info)
        result = {
            "hope this works": "Yes it works"
            #    "images": images,
            #    "pro_images": images_info[4]
        }
        return jsonify(result), 200

    elif image_pro_type == "Histogram Equalization":
        protype = Image_processing.histogram_eq_complete(wk_images)
        images_info = aft_processing(filename_str, protype)
        mainfunction.add_pro_images(email, images_info)
        result = {
            "hope this works": "Yes it works"
            #    "images": images,
            #    "pro_images": images_info[4]
        }
        return jsonify(result), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0")
