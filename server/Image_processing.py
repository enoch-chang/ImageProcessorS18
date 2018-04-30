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


class Image:

    def __init__(self, file_name=None, file_ext=None,
                 color_type=None,
                 image_array=None, dimensions=None,
                 contrast_stretch_array=None, hist_eq_array=None,
                 rev_video_array=None):
        self.file_name = file_name
        self.file_ext = file_ext
        self.color_type = color_type
        self.image_array = image_array
        self.contrast_stretch_array = contrast_stretch_array
        self.hist_eq_array = hist_eq_array
        self.rev_video_array = rev_video_array
        self.dimensions = dimensions

    # Load and Gather Image Data (Size, color / greyscale, file type)
    def gather_data(self):
        self.image_array = io.imread(self.file_name+self.file_ext)
        image_info = {}
        rows, columns, channels = self.image_array.shape
        self.dimensions = (rows, columns)
        if channels == 1:
            self.color_type = 'greyscale'
        else:
            self.color_type = 'color'
        return self.color_type, self.dimensions, self.image_array

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
    def output_histogram_data(self):
        red = np.zeros(self.dimensions, dtype=int)
        green = np.zeros(self.dimensions, dtype=int)
        blue = np.zeros(self.dimensions, dtype=int)
        rows, columns, channels = self.image_array.shape
        for row in range(0, rows):
            for column in range(0, columns):
                red_val, blue_val, green_val = self.image_array[row, column]
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
        plt.plot(x_vals, green_hist)
        plt.show()
        return red_hist, blue_hist, green_hist, x_vals


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


#test = Image(file_name='color_image_test', file_ext='.JPEG',
#             color_type='color')
#test.gather_data()
#test.output_histogram_data()
