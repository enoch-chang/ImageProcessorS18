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
#connect("mongodb://localhost:27017/images")
app = Flask(__name__)
CORS(app)

@app.route("/api/images/<user_email>", methods=["GET"])
def app_get_user(user_email):

    #r = request.get_json()

    try:
        user_data = mainfunction.print_user(user_email)

        result = {
            "email": user_email,
            "name": user_data.name,
            "images": user_data.images,
            "pro_images": user_data.pro_images,
            "success":1
        }
    except pymodm.errors.DoesNotExist:
        result = {"success":0}
        return jsonify(result), 200

    return jsonify(result), 200

def transfer_decode(image_str):
    index = image_str.find(',')
    image_str = image_str[index + 1:]
    image_bytes = image_str.encode()
    return image_bytes

def decode_image(image_bytes, image_id):
    with open(image_id, 'wb') as images:
        images.write(base64.b64decode(image_bytes))

def get_user(user_email):

    #r = request.get_json()

    try:
        user_data = mainfunction.print_user(user_email)

        result = {
            "email": user_email,
            "name": user_data.name,
            "images": user_data.images,
            "pro_images": user_data.pro_images,
            "success":1
        }
    except pymodm.errors.DoesNotExist:
        result = {"success":0}
        return jsonify(result), 200

    return jsonify(result), 200

def pre_processing(noheader_images, filename, images):
    """
    Do the pre-processing method for images that are about to be uploaded. After processing, this
    would return a image array including the corresponding information of the image, including:
    base64 str of the images, filename, id, filetype, time stamp, image size and unaltered histograms.
    :param images: base64 str of the image
    :param filename: str of the name of the image
    """
    #image64 = noheader_images
    images_names = filename
    image_function = Image_processing.Image(image_as_string=noheader_images)
    filetype = image_function.get_file_ext()
    time_stamp = datetime.datetime.now()
    imgdata = base64.b64decode(noheader_images)
    im = Image.open(io.BytesIO(imgdata))
    image_size = im.size
    #histograms = Image_processing.histogram_data(images)
    images_arr = [images, images_names, images_names, filetype, time_stamp, image_size, [[0,0],[0,0],[0,0],[0,0]]]

    return images_arr

def aft_processing(images, filename, protype):
    """
    After the specific image processing, this function process all the information regarding this image.
    After processing, this would return a image array including the corresponding information of the
    image, including:
    base64 str of the images, filename, id, rocess type, time stamp, time duration and
    processed histograms.
    :param images: base64 str of the image
    :param filename: str of the name of the image
    :param protype: list of the post-processed image histogram
    """
    #images = images
    #images_names = filename
    #image_function = Image_processing.Image(image_as_string=images)
    #time_stamp = datetime.datetime.now()
    #time_duration = protype[5]
    #histograms = [protype]
    #pro_images_arr = [images, images_names, image_names, filetype, time_stamp, time_duration, histograms]

    #return pro_images_arr

@app.route("/api/images/create", methods=["POST"])
def create_user():

    r = request.get_json()

    email = r["email"]
    name = r["name"]

#    if mainfunction.check_user(email):
#        result = {"warning": "User exist, do not need to add"}
#        return jsonify(result), 400
#    else:
    mainfunction.create_user(email, name)
    result = {"sucess": "create user"}
    return jsonify(result), 200

def rm_strheader(images):
    index = images.find(',')
    image_str = images[index + 1:]
    #base64bytes = image_str.encode()
    return image_str

@app.route("/api/images/upload", methods=["POST"])
def images_post():

    r = request.get_json()

    email = r["email"]
    images = r["images"]
    filename = r["filename"]

    #for i in enumerate(images, filename):
    no_header_im = rm_strheader(images)
    images_info = pre_processing(no_header_im, filename, images)
    mainfunction.add_images(email, images_info)
    result = {"success": "Cong! uploading successful"}

    return jsonify(result), 200

@app.route("/api/images/<user_email>/<image_id>/process", methods=["POST"])
def pro_images_post_his(user_email, image_id):

    r = request.get_json()

    user_email = r["email"]
    images = r["images"] #how to retrieve this string
    image_id = r["image_id"] #how to get this info
    image_pro_type = r["process"]

    wk_images = rm_strheader(images)
    if image_pro_type == "reverse video":
        protype = Image_processing.reverse_video_complete(wk_images)
        images_info = aft_processing(wk_images, filename, protype)
        mainfunction.add_pro_images(user_email, images_info)

    elif image_pro_type == "constrast stretching":
        protype = Image_processing.contrast_stretching_complete(wk_images)
        images_info = aft_processing(wk_images, filename, protype)
        mainfunction.add_pro_images(user_email, images_info)

    elif image_pro_type == "log compression":
        protype = Image_processing.log_compression_complete(wk_images)
        images_info = aft_processing(wk_images, filename, protype)
        mainfunction.add_pro_images(user_email, images_info)

    elif image_pro_type == "histogram eq":
        protype = Image_processing.histogram_eq_complete(wk_images)
        images_info = aft_processing(wk_images, filename, protype)
        mainfunction.add_pro_images(user_email, images_info)
 #   result = {
 #       "images":
 #   }

 #   return jsonify(result), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0")
