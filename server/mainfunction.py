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

def add_images(user_email, user_names, images, times):
    """
    Appends a heart_rate measurement at a specified time to the user specified by
    email. It is assumed that the user specified by email exists already.
    :param email: str email of the user
    :param heart_rate: number heart_rate measurement of the user
    :param time: the datetime of the heart_rate measurement
    """
    user = models.User.objects.raw({"_id": user_email}).first()  # Get the first user where _id=email
    user.user_names = user_names
    user.user_ori_images.append(images)  # append the current time to the user's list of heart rate times
    user.user_ori_images_time.append(times)  # append the current time to the user's list of images
    user.save()  # save the user to the database


def create_user(email, name):
    """
    Creates a user with the specified email and age. If the user already exists in the DB this WILL
    overwrite that user. It also adds the specified heart_rate to the user
    :param email: str email of the new user
    :param age: number age of the new user
    :param heart_rate: number initial heart_rate of this new user
    :param time: datetime of the initial heart rate measurement
    """
    u = models.User(email, name, [], [])  # create a new User instance
    u.images.append(["No images", "No images", "No images", "No images", "No images",
                     [0, 0], [[0, 0], [0, 0], [0, 0]]])
    u.pro_images.append(["No images", "No images", "No images", "No images", "No images",
                        [0, 0], [[0, 0], [0, 0], [0, 0]]])
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
