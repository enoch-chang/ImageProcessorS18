from flask import Flask, jsonify, request
from flask_cors import CORS
import pymodm
from pymodm import connect
import mainfunction
import numpy as np
import models
import datetime
import time
from Image_processing import show_histogram, hist_eq, contrast_stretch, reverse_video

connect("mongodb://vcm-3539.vm.duke.edu:27017/fp_images")
#connect("mongodb://localhost:27017/images")
app = Flask(__name__)
CORS(app)

@app.route("/api/images/<user_email>", methods=["GET"])
def app_get_user(user_email):

    #r = request.get_json()

    try:
        #user_data = mainfunction.print_user(user_email)
        images_list = models.User.objects.raw({"_id": user_email}).first()
        result = {
            "user_email": images_list.user_email,
            "name": images_list.user_names,
            "images": {"user_ori_images": images_list.user_ori_images,
                       "user_ori_images_id": images_list.user_ori_images_id,
                       "user_ori_images_filetype": images_list.user_ori_images_filetype,
                       "user_ori_images_time": datetime.datetime.now()
                       },
            "pro_images": {"user_ori_images": images_list.user_ori_images,
                           "user_ori_images_id": images_list.user_ori_images_id,
                           "user_images_his": images_list.user_images_his,
                           "user_images_log": images_list.user_images_log,
                           "user_images_contrast": images_list.user_images_contrast,
                           "user_images_reverse": images_list.user_images_reverse
                           }
        }
    except pymodm.errors.DoesNotExist:
        msg = {"warning": "No data related to this input email. "}
        return jsonify(msg), 0

    return jsonify(result), 200

def get_user(user_email):

    #r = request.get_json()

    try:
        #user_data = mainfunction.print_user(user_email)
        images_list = models.User.objects.raw({"_id": user_email}).first()
        result = {
            "user_email": images_list.user_email,
            "name": images_list.user_names,
            "images": {"user_ori_images": images_list.user_ori_images,
                       "user_ori_images_id": images_list.user_ori_images_id,
                       "user_ori_images_filetype": images_list.user_ori_images_filetype,
                       "user_ori_images_time": datetime.datetime.now()
                       },
            "pro_images": {"user_ori_images": images_list.user_ori_images,
                           "user_ori_images_id": images_list.user_ori_images_id,
                           "user_images_his": images_list.user_images_his,
                           "user_images_log": images_list.user_images_log,
                           "user_images_contrast": images_list.user_images_contrast,
                           "user_images_reverse": images_list.user_images_reverse
                           }
        }
    except pymodm.errors.DoesNotExist:
        msg = {"warning": "No data related to this input email. "}
        return jsonify(msg), 0

    return jsonify(result), 200

@app.route("/api/images/create", methods=["POST"])
def create_user():

    r = request.get_json()

    email = r["user_email"]
    user_id = r["user_names"]

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

@app.route("/api/images/<user_email>/<user_ori_images_id>/histogram", methods=["POST"])
def pro_images_post_his():

    #r = request.get_json()

    images_list = models.User.objects.raw({"_id": user_email}).first()
    images = images_list.user_ori_images
    show_histogram(images, color_type)




if __name__ == "__main__":
    app.run(host="0.0.0.0")