from Image_processing import Image
from skimage import io
import pytest


def test_reverse_video():
    test = Image(file_name='color_image_test', file_ext='.JPEG',
                 color_type='color')
    test.gather_data()
    output = test.reverse_video()
    inverted_1 = [255, 255, 255] - test.image_array[50, 50]
    inverted_2 = [255, 255, 255] - test.image_array[0, 0]
    assert output[50, 50].all() == inverted_1.all()
    assert output[0, 0].all() == inverted_2.all()


def test_gather_data():
    test = Image(file_name='color_image_test', file_ext='.JPEG',
                 color_type='color')
    test.gather_data()
    assert test.dimensions == [1200, 777]
    assert test.color_type == 'color'


test_reverse_video()
test_gather_data()
