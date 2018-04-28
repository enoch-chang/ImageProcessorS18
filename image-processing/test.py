import Image_processing
from skimage import io
import pytest


def test_reverse_video():
    image = io.imread('color_image_test.JPEG')
    file_type = '.JPEG'
    output = Image_processing.reverse_video(image, 'color', file_type)
    inverted_1 = [255, 255, 255] - image[50, 50]
    inverted_2 = [255, 255, 255] - image[0, 0]
    assert output[50, 50].all() == inverted_1.all()
    assert output[0, 0].all() == inverted_2.all()


def test_gather_data():
    image_info, image_array, image_name = Image_processing.gather_data(
        'color_image_test', '.JPEG')
    assert image_info['size'] == [1200, 777]
    assert image_info['color_type'] == 'color'

test_reverse_video()
