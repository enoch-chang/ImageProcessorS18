import os
import skimage
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import cv2
import base64
import imghdr

from skimage import io
from skimage import data, img_as_float
from skimage import exposure
from skimage import util


# Load and Gather Image Data (Size, color / greyscale, file type)
def gather_data(filename, file_type):
    image_name = filename + file_type
    image_array = io.imread(image_name)
    image_info = {}
    rows, columns, channels = image_array.shape
    dimensions = [columns, rows]
    if channels == 1:
        color_type = 'greyscale'
    else:
        color_type = 'color'
    image_info = {'size': dimensions,
                  'color_type': color_type}
    print(image_info)
    return image_info, image_array, image_name


# Generate Histogram
def show_histogram(img, color_type, image_name):
    if color_type == 'color':
        color = ('b', 'g', 'r')
        for i, col in enumerate(color):
            hist = cv2.calcHist([img], [i], None, [256], [0, 256])
            plt.plot(hist, color=col)
            plt.xlim([0, 256])
        plt.xlabel('Intensity'), plt.ylabel('Frequency (# of Pixels)')
        plt.title('Histogram for %s' % image_name)
        plt.show()
    elif color_type == 'greyscale':
        plt.hist(img.ravel(), 256, [0, 256], color='black')
        plt.xlabel('Intensity'), plt.ylabel('Frequency (# of Pixels)')
        plt.title('Histogram for %s' % image_name)
        plt.show()


# Equalization
def hist_eq(img, file_type):
    img_eq = exposure.equalize_hist(img)
    skimage.io.imsave('hist_equalized'+file_type, img_eq, plugin=None)
    return img_eq


# Contrast Stretching
def contrast_stretch(img, file_type):
    p2 = np.percentile(img, 2)
    p98 = np.percentile(img, 98)
    img_contrast_stretched = exposure.rescale_intensity(img, in_range=(p2,
                                                                       p98))
    skimage.io.imsave('contrast_stretched'+file_type, img_contrast_stretched,
                      plugin=None)
    return img_contrast_stretched


# Reverse Video
def reverse_video(img, color_type, file_type):
    inverted = np.zeros_like(img)
    if color_type == 'greyscale':
        inverted = util.invert(img)
    elif color_type == 'color':
        rows, columns, channels = img.shape
        for row in range(0, rows):
            for column in range(0, columns):
                inverted[row, column] = [255, 255, 255] - img[row, column]
    skimage.io.imsave('reverse_video' + file_type, inverted, plugin=None)
    return inverted


info, array, name = gather_data('greyscale_image_test', '.PNG')
reverse_video(array, 'greyscale', '.PNG')
