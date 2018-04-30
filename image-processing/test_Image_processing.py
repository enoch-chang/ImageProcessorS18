from Image_processing import Image
from skimage import io
import pytest
import numpy as np
import base64


with open('greyscale_image_test.JPEG', 'rb') as imageFile:
    string = base64.b64encode(imageFile.read())

def test_reverse_video():
    test = Image(image_as_string=string)
    test.gather_data()
    output = test.reverse_video()
    inverted_1 = [255, 255, 255] - test.image_array[50, 50]
    inverted_2 = [255, 255, 255] - test.image_array[0, 0]
    assert output[50, 50].all() == inverted_1.all()
    assert output[0, 0].all() == inverted_2.all()


def test_gather_data():
    test = Image(image_as_string=string)
    test.gather_data()
    assert test.dimensions == (1080, 1920)
    assert test.color_type == 'color'


def test_log_compression():
    test = Image(image_as_string=string)
    test.gather_data()
    output = test.log_compression()
    scaling_const = 255 / (np.log(255) + 1)
    assert output[50, 50].all() == scaling_const(np.log((np.absolute(
        test.image_array[50, 50]))))


test_reverse_video()
test_gather_data()
test_log_compression()
