from flask import Flask, jsonify, request
import pymodm
from pymodm import connect
import mainfunction
import numpy as np
import models
import datetime
import time
from flask_cors import CORS

CORS(app)
connect("mongodb://vcm-3539.vm.duke.edu:27017/fp_images")
app = Flask(__name__)

@app.route("/api/images/<user_email>", methods=["GET"])
def get_user(user_email):
    set_up_logging()

    try:
        user_data = mainfunction.print_user(user_email)

        result = {
            "user_email": user_email,
            "name": user_data.user_id,
            "images": user_data.images
        }
        logging.info("Logging success! Images can be retrieved.")
    except pymodm.errors.DoesNotExist:
        msg = "No data related to this input email. "
        logging.error(msg)
        return 0

    return jsonify(result), 200

@app.route("/api/images/create", methods=["POST"])
def post_images():
    set_up_logging()

    r = request.get_json()
    #valid = check_input(r)

    if valid is True:
        try:
            mainfunction.add_images(r["user_email"],
                                    r["user_names"],
                                    r["user_ori_images"],
                                    r["user_ori_images_time"])
            logging.info("Images added to existing user.")
        except pymodm.errors.DoesNotExist:
            mainfunction.create_user(r["user_email"],
                                     r["user_names"],
                                     r["user_ori_images"],
                                     r["user_ori_images_time"])
            logging.info("Images added to new user.")

        user = {
                "message": "Images successfully stored.",
                "user_email": r["user_email"],
                "user_names": r["user_names"],
                "user_ori_images": r["user_ori_images"]
                }
    else:
        msg = "Invalid input."
        return msg, 400

    return jsonify(user), 200

@app.route("/api/images/upload", methods=["POST"])
def images_post():







@app.route("/api/images/<user_email>/original/<image_id>", methods=["GET"])
def get_images(user_email):














@app.route("/api/images/<user_email>/processed/<image_id>", methods=["GET"])
def get_processed_images(user_email):






if __name__ == "__main__":
    app.run(host="127.0.0.1")