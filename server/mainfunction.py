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

#def save_image(base64image, filename):
#    with open(filename, “wb”) as image_out:
#        image_out.write(base64.b64decode(base64image))




#def image_decode():
#   with open(request.GET[filename], "im") as images
#        image_string = base64.b64encode(images.read())
#    image_list = db.database_name.insert(){ "images" : image_string
#    })
#    return image_list

def add_images(email, images, times):
    """
    Appends a heart_rate measurement at a specified time to the user specified by
    email. It is assumed that the user specified by email exists already.
    :param email: str email of the user
    :param heart_rate: number heart_rate measurement of the user
    :param time: the datetime of the heart_rate measurement
    """
    user = models.User.objects.raw({"_id": email}).first()  # Get the first user where _id=email
    user.user_ori_images.append(images)  # append the current time to the user's list of heart rate times
    user.user_ori_images_time.append(times)
    user.save()  # save the user to the database


def create_user(email, user_id, images, processed_images):
    """
    Creates a user with the specified email and age. If the user already exists in the DB this WILL
    overwrite that user. It also adds the specified heart_rate to the user
    :param email: str email of the new user
    :param age: number age of the new user
    :param heart_rate: number initial heart_rate of this new user
    :param time: datetime of the initial heart rate measurement
    """

    u = models.User(email, user_id, [], [])  # create a new User instance
    u.user_id.append(user_id)
    u.images.append(images)
    u.processed_images.append(processed_images)
    u.save()  # save the user to the database


def print_user(email):
    """
    Prints the user with the specified email
    :param email: str email of the user of interest
    :return:
    """
    user = models.User.objects.raw({"_id": email}).first()  # Get the first user where _id=email
    print(user.email)

if __name__ == "__main__":
    connect("mongodb://vcm-3539.vm.duke.edu:27017/MyLittlePony")  # open up connection to db