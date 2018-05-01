from Image_processing import Image
from skimage import io
import pytest
import numpy as np
import base64


with open('image_test.JPEG', 'rb') as imageFile:
    jpeg_string = base64.b64encode(imageFile.read())

with open('image_test.png', 'rb') as imageFile:
    png_string = base64.b64encode(imageFile.read())


@pytest.mark.filterwarnings('ignore::RuntimeWarning')
def test_reverse_video():
    # Test JPEG File
    test = Image(image_as_string=jpeg_string)
    test.gather_data()
    output, time_to_run = test.reverse_video()
    inverted_1 = [255, 255, 255] - test.image_array[50, 50]
    inverted_2 = [255, 255, 255] - test.image_array[0, 0]
    assert output[50, 50].all() == inverted_1.all()
    assert output[0, 0].all() == inverted_2.all()
    # Test PNG file
    test = Image(image_as_string=png_string)
    test.gather_data()
    output, time_to_run = test.reverse_video()
    inverted_1 = [255, 255, 255] - test.image_array[50, 50]
    inverted_2 = [255, 255, 255] - test.image_array[0, 0]
    assert output[50, 50].all() == inverted_1.all()
    assert output[0, 0].all() == inverted_2.all()


def test_gather_data():
    # Test JPEG File
    test = Image(image_as_string=jpeg_string)
    test.gather_data()
    assert test.dimensions == (777, 1200)
    assert test.color_type == 'color'
    # Test PNG File
    test = Image(image_as_string=png_string)
    test.gather_data()
    assert test.dimensions == (777, 1200)
    assert test.color_type == 'color'


def test_log_compression():
    # Test JPEG File
    test = Image(image_as_string=jpeg_string)
    test.gather_data()
    output, time_to_run = test.log_compression()
    scaling_const = 255 / (np.log(255) + 1)
    array_values = scaling_const*np.log(np.absolute(test.image_array[50, 50]))
    assert output[50, 50].all() == array_values.all()
    # Test PNG File
    test = Image(image_as_string=png_string)
    test.gather_data()
    output, time_to_run = test.log_compression()
    scaling_const = 255 / (np.log(255) + 1)
    array_values = scaling_const*np.log(np.absolute(test.image_array[50, 50]))
    assert output[50, 50].all() == array_values.all()


def test_get_file_extension():
    # Test JPEG File
    test = Image(image_as_string=jpeg_string)
    ext = test.get_file_ext()
    assert ext == '.JPEG'
    # Test PNG File
    test = Image(image_as_string=png_string)
    ext = test.get_file_ext()
    assert ext == '.PNG'


# Run Tests
test_reverse_video()
test_gather_data()
test_log_compression()
test_get_file_extension()
