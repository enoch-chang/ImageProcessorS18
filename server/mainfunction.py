from pymodm import connect
import models
import datetime


def processed_his(email, images, timing):
    user = models.User.objects.raw({"_id": email}).first()
    user.user_images_his.append(images)
    user.user_images_pro_time.append(timing)
    user.save()


def processed_contrast(email, images, timing):
    user = models.User.objects.raw({"_id": email}).first()
    user.user_images_contrast.append(images)
    user.user_images_pro_time.append(timing)
    user.save()


def processed_log(email, images, timing):
    user = models.User.objects.raw({"_id": email}).first()
    user.user_images_log.append(images)
    user.user_images_pro_time.append(timing)
    user.save()


def processed_reverse(email, images, timing):
    user = models.User.objects.raw({"_id": email}).first()
    user.user_images_reverse.append(images)
    user.user_images_pro_time.append(timing)
    user.save()


def add_images(email, image_info):
    """
    Appends images to specific user email and the images corresponding information, including the
    base64 str of the images, filename, id, filetype, time stamp, image size and unaltered histograms.
    :param email: str email of the user
    :param image_info: a list of image information
    """
    user = models.User.objects.raw({"_id": email}).first()  # Get the first user where _id=email
    user.images.append(image_info)  # append image to the user's list of images
    user.save()  # save the user to the database

def add_pro_images(email, image_info):
    """
    After processing, this function is to appends images to specific user email and the images
    corresponding information, including the
    base64 str of the processed images, filename, id, process type, time stamp, time duration and
    processed histograms.
    :param email: str email of the user
    :param image_info: a list of image information
    """
    user = models.User.objects.raw({"_id": email}).first()  # Get the first user where _id=email
    user.pro_images.append(image_info)  # append image to the user's list of images
    user.save()  # save the user to the database


def create_user(email, name):
    """
    Creates a user with the specified email and name. If the user already exists in the DB this will
    overwrite that user.
    :param email: str email of the new user
    :param name: str name of the new user
    """
    u = models.User(email, name, [], [])  # create a new User instance
    #u.images.append(["No images", "No images", "No images", "No images", "No images",
    #                 [0, 0], [[0, 0], [0, 0], [0, 0]]])
    #u.pro_images.append(["No images", "No images", "No images", "No images", "No images",
    #                    [0, 0], [[0, 0], [0, 0], [0, 0]]])
    #u.name = name
    u.save() # save the user to the database


def check_user(email):
    return models.User.objects.raw({"_id": email}).count()>0


def print_user(email):
    """
    Prints the user with the specified email
    :param email: str email of the user of interest
    :return:
    """
    user = models.User.objects.raw({"_id": email}).first()  # Get the first user where _id=email
    print(user.email, user.name, user.images, user.pro_images)
    return user


if __name__ == "__main__":
    connect("mongodb://vcm-3608.vm.duke.edu:27017/fp_images")  # open up connection to db
