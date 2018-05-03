from pymodm import connect
import models
import datetime


def add_images(email, image_info):
    """
    Appends images to specific user email and the images corresponding
    information, including the base64 str of the images, filename, id,
    filetype, time stamp, image size and unaltered histograms.
    :param email: str email of the user
    :param image_info: a list of image information
    """
    user = models.User.objects.raw({"_id": email}).first()
    # Get the first user where _id=email
    user.images.append(image_info)
    # append image to the user's list of images
    user.save()
    # save the user to the database


def add_pro_images(email, image_info):
    """
    After processing, this function is to appends images to specific user
    email and the images corresponding information, including the
    base64 str of the processed images, filename, id, process type,
    time stamp, time duration and processed histograms.
    :param email: str email of the user
    :param image_info: a list of image information
    """
    user = models.User.objects.raw({"_id": email}).first()
    # Get the first user where _id=email
    user.pro_images.append(image_info)
    # append image to the user's list of images
    user.save()
    # save the user to the database


def create_user(email, name):
    """
    Creates a user with the specified email and name. If the user already
    exists in the DB this will overwrite that user.
    :param email: str email of the new user
    :param name: str name of the new user
    """
    u = models.User(email, name, [], [])  # create a new User instance
    u.images.append(["No images", "No images", "No images", "No images",
                     "No images", [0, 0], [[0, 0], [0, 0], [0, 0]]])
    u.pro_images.append(["No images", "No images", "No images", "No images",
                         "No images", [0, 0], [[0, 0], [0, 0], [0, 0]]])
    # initialization of the images and processed images lists
    u.save()
    # save the user to the database


def delete_init():
    user = models.User.objects.raw({"_id": email}).first()
    user.images.remove(["No images", "No images", "No images", "No images",
                        "No images", [0, 0], [[0, 0], [0, 0], [0, 0]]])
    user.pro_images.remove(["No images", "No images", "No images", "No images",
                            "No images", [0, 0], [[0, 0], [0, 0], [0, 0]]])
    u.save()


def check_user(email):
    """
    Check if the user exists in the database. If user exists, this will
    return > 0, if not it would be 0.
    :param email: str email of the new user
    """
    return models.User.objects.raw({"_id": email}).count() > 0


def print_user(email):
    """
    Prints the user with the specified email
    :param email: str email of the user of interest
    :return:
    """
    user = models.User.objects.raw({"_id": email}).first()
    # Get the first user where _id=email
    print(user.email, user.name, user.images, user.pro_images)
    return user


if __name__ == "__main__":
    connect("mongodb://vcm-3608.vm.duke.edu:27017/fp_images")
    # open up connection to db

