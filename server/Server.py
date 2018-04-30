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

connect("mongodb://vcm-3608.vm.duke.edu:27017/fp_images")
#connect("mongodb://localhost:27017/images")
app = Flask(__name__)
CORS(app)

@app.route("/api/images/<user_email>", methods=["GET"])
def app_get_user(user_email):

    #r = request.get_json()

    try:
        #user_data = mainfunction.print_user(user_email)
        images_list = models.User.objects.raw({"_id": user_email}).first()

        user_images = images_list.user_ori_images
        image_names = images_list.user_ori_images_id
        filetype = Image_processing.Image.get_file_ext(user_images)
        time_stamp = images_list.user_ori_images_time
        #histograms = Image_processing.output_altered_histogram_data()
        images_arr = [user_images, image_names, image_names, filetype, time_stamp, None, None]

        user_pro_images = images_list.user_processed_images
        #histograms = Image_processing.Image.show_histogram()
        pro_images_arr = [user_pro_images , image_names, image_names, filetype, time_stamp, None, None]

        result = {
            "user_email": images_list.user_email,
            "name": images_list.user_names,
            "images": images_arr,
            "pro_images": pro_images_arr,
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
        #user_data = mainfunction.print_user(user_email)
        images_list = models.User.objects.raw({"_id": user_email}).first()

        user_images = images_list.user_ori_images
        image_names = images_list.user_ori_images_id
        filetype = Image_processing.Image.get_file_ext(user_images)
        time_stamp = images_list.user_ori_images_time
        #histograms = Image_processing.output_altered_histogram_data()
        images_arr = [user_images, image_names, image_names, filetype, time_stamp, None, None]

        user_pro_images = images_list.user_processed_images
        pro_images_type = images_list.image_pro_type
        # filetype = Image_processing.Image.decode_filetype()
        #histograms = Image_processing.Image.show_histogram()
        pro_images_arr = [user_pro_images , image_names, image_names, pro_images_type, time_stamp, None, None]

        result = {
            "user_email": images_list.user_email,
            "name": images_list.user_names,
            "images": images_arr,
            "pro_images": pro_images_arr,
            "success":1
        }
    except pymodm.errors.DoesNotExist:
        result = {"success":0}
        return jsonify(result), 200

    return jsonify(result), 200

@app.route("/api/images/create", methods=["POST"])
def create_user():

    r = request.get_json()

    email = r["email"]
    user_id = r["name"]

    if mainfunction.check_user(email):
        msg = {"warning": "User exist, do not need to add"}
        return jsonify(msg), 400
    else:
        mainfunction.create_user(email, user_id)
        logging.info("Images added to new user.")
        return get_user(user_email), 200

@app.route("/api/images/upload", methods=["POST"])
def images_post():

    r = request.get_json()

    email = r["user_email"]
    user_id = r["user_names"]
    images = r["user_ori_images"]

    if mainfunction.check_user(email):
        mainfunction.add_images(email, user_id, images, datetime.datetime.now())
        msg = {"warning": "User exist, do not need to add"}
        return jsonify(msg), 200
    else:
        mainfunction.create_user(email, user_id)
        mainfunction.add_images(email, user_id, images, datetime.datetime.now())
        return get_user(user_email), 200

@app.route("/api/images/<user_email>/original/<images_id>", methods=["GET"])
def app_get_ori_images(user_ori_images):

    try:
        images_info = models.User.objects.raw({"_id": user_ori_images}).first()
        #images_gather = Image_processing.Image.gather_data()
        result = {
            "user_ori_images": images_info.user_ori_images,
            "user_ori_images_id": images_info.user_ori_images_id,
            "user_ori_images_filetype": Image_processing.Image.get_file_ext(images_info.user_ori_images),
            "user_ori_images_time": datetime.datetime.now(),
            "success": 1
            }
    except pymodm.errors.DoesNotExist:
        result = {"success": 0}
        return jsonify(result), 200

    return jsonify(result), 200

@app.route("/api/images/<user_email>/<user_ori_images_id>", methods=["POST"])
def pro_images_post_his():

    r = request.get_json()


    images_list = models.User.objects.raw({"_id": user_email}).first()
    images = images_list.user_ori_images
    show_histogram(images, color_type)




if __name__ == "__main__":
    app.run(host="0.0.0.0")
