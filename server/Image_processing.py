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
import math

from skimage import io
from skimage import data, img_as_float
from skimage import exposure
from skimage import util

#with open('color_image_test.JPEG', 'rb') as imageFile:
#    string = base64.b64encode(imageFile.read())


class Image:

    def __init__(self, file_name=None, file_ext=None,
                 color_type=None,
                 image_array=None, dimensions=None,
                 contrast_stretch_array=None, hist_eq_array=None,
                 rev_video_array=None, image_as_string=None,
                 log_comp_array=None, max_intensity_val=None):
        self.file_name = file_name
        self.file_ext = file_ext
        self.color_type = color_type
        self.image_array = image_array
        self.contrast_stretch_array = contrast_stretch_array
        self.hist_eq_array = hist_eq_array
        self.rev_video_array = rev_video_array
        self.dimensions = dimensions
        self.image_as_string = image_as_string
        self.log_comp_array = log_comp_array
        self.max_intensity_val = max_intensity_val

    # Load and Gather Image Data (Size, color / greyscale, file type)
    def gather_data(self):
        self.decode_string()
        self.image_array = io.imread('working_image.JPEG')
        rows, columns, channels = self.image_array.shape
        self.dimensions = (rows, columns)
        if channels == 1:
            self.color_type = 'greyscale'
        else:
            self.color_type = 'color'
        return self.color_type, self.dimensions, self.image_array

    # Decode Base64 string into workable image
    def decode_string(self):
        self.get_file_ext()
        fh = open("working_image"+self.file_ext, 'wb')
        fh.write(self.image_as_string.decode('base64'))

    # Read the image file type from Base64 string
    def get_file_ext(self):
        string = self.image_as_string
        if string[0] == '/':
            self.file_ext = '.JPEG'
        elif string[0] == 'i':
            self.file_ext = '.PNG'
        return self.file_ext

    # Generate Histogram
    def show_histogram(self):
        if self.color_type == 'color':
            color = ('b', 'g', 'r')
            for i, col in enumerate(color):
                hist = cv2.calcHist([self.image_array], [i], None, [256], [0,
                                                                           256
                                                                           ])
                plt.plot(hist, color=col)
                plt.xlim([0, 256])
                plt.xlabel('Intensity'), plt.ylabel('Frequency (# of Pixels)')
                plt.title('Histogram for %s' % self.file_name)
            plt.show()
        elif self.color_type == 'greyscale':
            plt.hist(self.image_array.ravel(), 256, [0, 256], color='black')
            plt.xlabel('Intensity'), plt.ylabel('Frequency (# of Pixels)')
            plt.title('Histogram for %s' % self.filename)
            plt.show()

    # Generate plottable histogram data
    def output_histogram_data(self, hist_type):
        red = np.zeros(self.dimensions, dtype=int)
        green = np.zeros(self.dimensions, dtype=int)
        blue = np.zeros(self.dimensions, dtype=int)
        rows, columns, channels = self.image_array.shape

        if hist_type == 'original':
            array = self.image_array
        elif hist_type == 'hist_eq':
            array = self.hist_eq_array
        elif hist_type == 'rev_vid':
            array = self.rev_video_array
        elif hist_type == 'contrast_stretch':
            array = self.contrast_stretch_array
        elif hist_type == 'log_comp':
            array = self.log_comp_array
        for row in range(0, rows):
            for column in range(0, columns):
                red_val, blue_val, green_val = array[row, column]
                red[row, column] = red_val
                green[row, column] = green_val
                blue[row, column] = blue_val
        red_data = np.histogram(red, bins=256)
        blue_data = np.histogram(blue, bins=256)
        green_data = np.histogram(green, bins=256)
        red_hist = red_data[0]
        blue_hist = blue_data[0]
        green_hist = green_data[0]
        x_vals = range(0, 256)
        return [[red_hist], [bluehist], [green_hist], [x_vals]]

    # Equalization
    def hist_eq(self):
        self.hist_eq_array = exposure.equalize_hist(self.image_array)
        skimage.io.imsave('hist_equalized'+self.file_ext, self.hist_eq_array,
                          plugin=None)
        return self.hist_eq_array

    # Contrast Stretching
    def contrast_stretch(self):
        p2 = np.percentile(self.image_array, 2)
        p98 = np.percentile(self.image_array, 98)
        self.contrast_stretch_array = exposure.rescale_intensity(
            self.image_array, in_range=(p2, p98))
        skimage.io.imsave('contrast_stretched'+self.file_ext,
                          self.contrast_stretch_array, plugin=None)
        return self.contrast_stretch_array

    # Logarithmic Compression
    def log_compression(self):
        log_comp = np.zeros_like(self.image_array)
        scaling_const = 255/(np.log(255)+1)  # assumes max val is 255
        print(scaling_const)
        rows, columns, channels = self.image_array.shape

        for row in range(0, rows):
            for column in range(0, columns):
                log_comp[row, column] = scaling_const*np.log((
                                                             np.absolute(self.
                                                            image_array[
                                                            row, column])))

        self.log_comp_array = log_comp
        skimage.io.imsave('log_compressed'+self.file_ext,
                          self.log_comp_array, plugin=None)
        return self.log_comp_array

    # Reverse Video
    def reverse_video(self):
        inverted = np.zeros_like(self.image_array)
        if self.color_type == 'greyscale':
            inverted = util.invert(self.image_array)
        elif self.color_type == 'color':
            rows, columns, channels = self.image_array.shape
            for row in range(0, rows):
                for column in range(0, columns):
                    inverted[row, column] = [255, 255, 255] - \
                                            self.image_array[row, column]
        skimage.io.imsave('reverse_video' + self.file_ext, inverted,
                          plugin=None)
        self.rev_video_array = inverted
        return self.rev_video_array


# Encode created images into Base64
def encode_string(filename, file_ext):
    with open(filename + file_ext, 'rb') as imageFile:
        string = base64.b64encode(imageFile.read())
    return string


# Generate plottable histogram data
def output_altered_histogram_data(hist_type, file_ext):
    filename = ''
    if hist_type == 'hist_eq':
        filename = 'hist_equalized'+file_ext
    elif hist_type == 'rev_vid':
        filename = 'reverse_video'+file_ext
    elif hist_type == 'contrast_stretch':
        filename = 'contrast_stretched'+file_ext
    elif hist_type == 'log_comp'+file_ext:
        filename = 'log_compressed'+file_ext

    image = io.imread(filename)
    rows, columns, channels = image.shape
    dimensions = (rows, columns)
    red = np.zeros(dimensions, dtype=int)
    green = np.zeros(dimensions, dtype=int)
    blue = np.zeros(dimensions, dtype=int)

    for row in range(0, rows):
        for column in range(0, columns):
            red_val, blue_val, green_val = image[row, column]
            red[row, column] = red_val
            green[row, column] = green_val
            blue[row, column] = blue_val
    red_data = np.histogram(red, bins=256)
    blue_data = np.histogram(blue, bins=256)
    green_data = np.histogram(green, bins=256)
    red_hist = red_data[0]
    blue_hist = blue_data[0]
    green_hist = green_data[0]
    x_vals = range(0, 256)
    return red_hist, blue_hist, green_hist, x_vals


# Create callable functions for each process
def initialize_image(image_string):
    image = Image(image_as_string=image_string)
    image.decode_string()
    image.gather_data()
    return image


# Histogram equalization - Callable Function
def histogram_eq_complete(image_string):
    image = initialize_image(image_string)
    image.hist_eq()
    red_hist, blue_hist, green_hist, x_vals = output_altered_histogram_data(
        'hist_eq', image.file_ext)
    base64_string = encode_string('hist_equalized', image.file_ext)
    return red_hist, blue_hist, green_hist, x_vals, base64_string


# Contrast stretching - Callable Function
def contrast_stretching_complete(image_string):
    image = initialize_image(image_string)
    image.contrast_stretch()
    red_hist, blue_hist, green_hist, x_vals = \
        output_altered_histogram_data('contrast_stretch', image.file_ext)
    base64_string = encode_string('contrast_stretched', image.file_ext)
    return red_hist, blue_hist, green_hist, x_vals, base64_string


# Reverse video - Callable Function
def reverse_video_complete(image_string):
    image = initialize_image(image_string)
    image.reverse_video()
    red_hist, blue_hist, green_hist, x_vals = \
        output_altered_histogram_data('rev_vid', image.file_ext)
    base64_string = encode_string('reverse_video', image.file_ext)
    plt.plot(x_vals, red_hist)
    plt.show()
    return red_hist, blue_hist, green_hist, x_vals, base64_string


# Log Compression - Callable Function
def log_compression_complete(image_string):
    image = initialize_image(image_string)
    image.log_compression()
    red_hist, blue_hist, green_hist, x_vals = \
        output_altered_histogram_data('log_comp', image.file_ext)
    base64_string = encode_string('log_compressed', image.file_ext)
    return red_hist, blue_hist, green_hist, x_vals, base64_string


# Output histogram data for unaltered image
def histogram_data(image_string):
    image = initialize_image(image_string)
    red_hist, blue_hist, green_hist, x_vals = image.output_histogram_data(
        'original')
    return [[red_hist], [blue_hist], [green_hist], [x_vals]]


#histogram_data(string)
#test = Image(image_as_string=string)
#test.gather_data()
#test.log_compression()