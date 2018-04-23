import os
import skimage
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import cv2

from skimage import io
from skimage import data, img_as_float
from skimage import exposure

# Load Image
image_name = 'bad_contrast.JPEG'
image = io.imread(image_name)


# Generate Histogram
def show_histogram(img, color_type):
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
def hist_eq(photo):
    img_eq = exposure.equalize_hist(photo)
    skimage.io.imsave('hist_equalized.JPEG', img_eq, plugin=None)
    return img_eq


show_histogram(image, color_type='greyscale')
