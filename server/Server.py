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
        #images_list = models.User.objects.raw({"_id": email}).first()

        #user_images = images_list.images
        #image_names = images_list.user_ori_images_id
        #filetype = Image_processing.Image.get_file_ext(user_images)
        #time_stamp = images_list.user_ori_images_time
        #histograms = Image_processing.output_altered_histogram_data()
        #images_arr = [user_images, image_names, image_names, filetype, time_stamp, None, None]

        #user_pro_images = images_list.pro_images
        #histograms = Image_processing.Image.show_histogram()
        #pro_images_arr = [user_pro_images , image_names, image_names, filetype, time_stamp, None, None]

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
        #images_list = models.User.objects.raw({"_id": email}).first()

        #user_images = images_list.images
        #image_names = images_list.user_ori_images_id
        #filetype = Image_processing.Image.get_file_ext(user_images)
        #time_stamp = images_list.user_ori_images_time
        #histograms = Image_processing.output_altered_histogram_data()
        #images_arr = [user_images, image_names, image_names, filetype, time_stamp, None, None]

        #user_pro_images = images_list.pro_images
        #histograms = Image_processing.Image.show_histogram()
        #pro_images_arr = [user_pro_images , image_names, image_names, filetype, time_stamp, None, None]

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

def pre_processing(images):

    r = request.get_json()

    images = r["image"]
    images_names = r["filename"]
    filetype = Image_processing.Image.get_file_ext(images)
    time_stamp = datetime.datetime.now()
    base64_str = transfer_decode(images)
    imgdata = base64.b64decode(base64_str)
    im = Image.open(io.BytesIO(imgdata))
    image_size = [im.size]
    #histograms = Image_processing.output_altered_histogram_data()
    images_arr = [images, images_names, image_names, filetype, time_stamp, image_size,
                  [[0,0], [0,0], [0,0], [0,0]]]

    return images_arr

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

@app.route("/api/images/upload", methods=["POST"])
def images_post():

    r = request.get_json()

    email = r["email"]
    images = r["images"]
    images_info = pre_processing(images)
    mainfunction.add_images(email, images_info)

    return get_user(email), 200

@app.route("/api/images/<email>/original/<images_id>", methods=["GET"])
def app_get_ori_images(user_ori_images):

    try:
        images_info = models.User.objects.raw({"_id": user_ori_images}).first()
        #images_gather = Image_processing.Image.gather_data()
        result = {
            "user_ori_images": images_info.images,
            "user_ori_images_id": images_info.user_ori_images_id,
            "user_ori_images_filetype": Image_processing.Image.get_file_ext(images_info.images),
            "user_ori_images_time": datetime.datetime.now(),
            "success": 1
            }
    except pymodm.errors.DoesNotExist:
        result = {"success": 0}
        return jsonify(result), 200

    return jsonify(result), 200

#@app.route("/api/images/<user_email>/<user_ori_images_id>/process", methods=["POST"])
#def pro_images_post_his():

#    r = request.get_json()

#    image_pro_type = r["image_pro_type"]
#    image_id = r[""]
#    if image_pro_type == "reverse video"





if __name__ == "__main__":
    app.run(host="0.0.0.0")
