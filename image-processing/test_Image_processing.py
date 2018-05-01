from Image_processing import Image
import Image_processing
from skimage import io
import pytest
import numpy as np
import base64

file_jpeg = open('image_test_jpeg.txt')
jpeg_string = file_jpeg.read()


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


def test_gather_data():
    # Test JPEG File
    test = Image(image_as_string=jpeg_string)
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


def test_get_file_extension():
    # Test JPEG File
    test = Image(image_as_string=jpeg_string)
    ext = test.get_file_ext()
    assert ext == '.JPEG'


# Run Tests
test_reverse_video()
test_gather_data()
test_log_compression()
test_get_file_extension()
