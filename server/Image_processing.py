import skimage
import numpy as np
import cv2
import base64
import timeit
import logging
from skimage import io
from skimage import exposure
from skimage import util


# Set up logger
log_format = '%(levelname)s %(asctime)s %(message)s'
logging.basicConfig(filename='divlog.txt', format=log_format,
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG,
                    filemode='w')
logger = logging.getLogger()


class Image:

    def __init__(self, file_name=None, file_ext=None,
                 color_type=None,
                 image_array=None, dimensions=None,
                 contrast_stretch_array=None, hist_eq_array=None,
                 rev_video_array=None, image_as_string=None,
                 log_comp_array=None, max_intensity_val=None,
                 alpha_channel='no'):
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
        self.alpha_channel = alpha_channel

    # Load and Gather Image Data (Size, color / greyscale, file type)
    def gather_data(self):
        """Gathers useful information about an input image and stores the data
        as object attributes. Functions by taking in a base64 string,
        decoding it then saving it as a numpy array
        :returns self.color_type: a string stating 'greyscale' or 'color'
        :returns self.dimensions: an array in the form of (rows, columns)
        :returns self.image_array: a numpy array containing the digital
        image data
        :returns self.alpha_channel: a yes or no string indicating whether
        the contains an alpha channel
        """
        self.decode_string()
        self.image_array = io.imread('working_image' + self.file_ext)
        rows, columns, channels = self.image_array.shape
        self.dimensions = (rows, columns)

        logger.info('Image Dimensions: %s, %s' % (rows, columns))
        if channels == 1:
            self.color_type = 'greyscale'
        elif channels == 3:
            self.color_type = 'color'
        elif channels == 4:
            self.color_type = 'color'
            self.alpha_channel = 'yes'
            self.image_array = self.remove_alpha_channel()
            logger.warning('This image contains an alpha channel, '
                           'which will be automatically removed. Consider '
                           'trying an image without an alpha channel, '
                           'as its removal may impact image quality')

        logger.info('Image Color: %s' % self.color_type)
        return self.color_type, self.dimensions, self.image_array, \
               self.alpha_channel

    # Remove alpha channel if present
    def remove_alpha_channel(self):
        """ Removes alpha channel from image data array
        :returns self.image_array: image data array with alpha channel
        values removed
        """
        no_alpha = self.image_array[:, :, :3]
        self.image_array = no_alpha
        return self.image_array

    # Decode Base64 string into workable image
    def decode_string(self):
        """ Takes in base64 string containing image data, determines the
        file type (either PNG or JPEG) based off this info, then saves the
        image to disc under the name 'working_image' with the same file
        extension as the input file
        """
        ext = self.get_file_ext()
        fh = open('working_image' + ext, "wb")
        fh.write(base64.b64decode(self.image_as_string))
        logger.info('Base64 image successfully decoded')

    # Read the image file type from Base64 string
    def get_file_ext(self):
        """Reads base64 image data and determines image file type (
        PNG/JPEG)
        :returns self.file_ext: string reading either '.JPEG' or '.PNG'
        """
        string = self.image_as_string
        if string[0] == '/':
            self.file_ext = '.JPEG'
        elif string[0] == 'i':
            self.file_ext = '.PNG'
        logger.info('Image file extension: %s' % self.file_ext)
        return self.file_ext

    # Generate Histogram
    def show_histogram(self):
        """Generates histogram of image in Python
        """
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
        """ Outputs image histogram data as arrays
        :param hist_type: the type of data for which the histogram is being
        produced ('orignal' - unaltered image, 'hist_eq' - image altered by
        histogram equalization, 'rev_vid' - image altered by reverse video,
        'contrast_stretch' - image altered by contrast stretching,
        'log_comp' - image altered by logarithmic compression
        :returns red_hist: the red frequency values of the image's histogram
        :returns blue_hist: the blue frequency values of the image's histogram
        :returns green_hist: the green frequency values of the image's
        histogram
        :returns x_vals: the intensity values of the image (0-255)
        """
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
        logger.info('Histogram data generated')
        return red_hist, blue_hist, green_hist, x_vals

    # Equalization
    def hist_eq(self):
        """
        Carries out histogram equalization on input image
        :return self.hist_eq_array: numpy array containing image data of
        altered image
        :return run_time: the time it took to run this method in seconds
        """
        start_time = timeit.default_timer()
        self.hist_eq_array = exposure.equalize_hist(self.image_array)
        skimage.io.imsave('hist_equalized'+self.file_ext, self.hist_eq_array,
                          plugin=None)
        run_time = timeit.default_timer() - start_time
        logger.info('Histogram equalization completed in %s seconds' %
                    run_time)
        return self.hist_eq_array, run_time

    # Contrast Stretching
    def contrast_stretch(self):
        """
        Carries out contrast stretching on input image
        :return self.contrast_stretch_array: numpy array containing image
        data of altered image
        :return run_time: the time it took to run this method in seconds
        """
        start_time = timeit.default_timer()
        p2 = np.percentile(self.image_array, 2)
        p98 = np.percentile(self.image_array, 98)
        self.contrast_stretch_array = exposure.rescale_intensity(
            self.image_array, in_range=(p2, p98))
        skimage.io.imsave('contrast_stretched'+self.file_ext,
                          self.contrast_stretch_array, plugin=None)
        run_time = timeit.default_timer() - start_time
        logger.info('Contrast stretching completed in %s seconds' %
                    run_time)
        return self.contrast_stretch_array, run_time

    # Logarithmic Compression
    def log_compression(self):
        """
        Carries out logarithmic compression on input image
        :return self.log_comp_array: numpy array containing image
        data of altered image
        :return run_time: the time it took to run this method in seconds
        """
        start_time = timeit.default_timer()
        log_comp = np.zeros_like(self.image_array)
        scaling_const = 255/(np.log(255)+1)  # assumes max val is 255
        rows, columns, channels = self.image_array.shape

        for row in range(0, rows):
            for column in range(0, columns):
                log_comp[row, column] = scaling_const*np.log((
                                np.absolute(self.image_array[row, column])))

        self.log_comp_array = log_comp
        skimage.io.imsave('log_compressed'+self.file_ext,
                          self.log_comp_array, plugin=None)
        run_time = timeit.default_timer() - start_time
        logger.info('Logarithmic compression completed in %s seconds' %
                    run_time)
        return self.log_comp_array, run_time

    # Reverse Video
    def reverse_video(self):
        """
        Carries out reverse video on input image
        :return self.rev_video_array: numpy array containing image
        data of altered image
        :return run_time: the time it took to run this method in seconds
        """
        start_time = timeit.default_timer()
        inverted = np.zeros_like(self.image_array)

        if self.color_type == 'greyscale':
            inverted = util.invert(self.image_array)
        else:
            rows, columns, channels = self.image_array.shape
            for row in range(0, rows):
                for column in range(0, columns):
                    image_data = self.image_array[row, column]
                    inverted[row, column] = [255, 255, 255] - image_data
        skimage.io.imsave('reverse_video' + self.file_ext, inverted,
                          plugin=None)
        self.rev_video_array = inverted
        run_time = timeit.default_timer() - start_time
        logger.info('Reverse video completed in %s seconds' %
                    run_time)
        return self.rev_video_array, run_time


# Encode created images into Base64
def encode_string(filename, file_ext):
    """Encodes image saved on disc into a base64 string
    :param filename: filename  of image on disc which is to be encoded
    :param file_ext: file extension of filename (.PNG/.JPEG)
    :return string: base64 encoded image string
    """
    with open(filename + file_ext, 'rb') as imageFile:
        string = base64.b64encode(imageFile.read())
    logger.info('Image successfully encoded as string')
    return string


# Generate plottable histogram data
def output_altered_histogram_data(hist_type, file_ext):
    """Outputs arrays containing histogram data of altered images
    :param hist_type: the type of data for which the histogram is being
        produced ('orignal' - unaltered image, 'hist_eq' - image altered by
        histogram equalization, 'rev_vid' - image altered by reverse video,
        'contrast_stretch' - image altered by contrast stretching,
        'log_comp' - image altered by logarithmic compression
    :param file_ext: file extension of filename (.PNG/.JPEG)
    :returns red_hist: the red frequency values of the image's histogram
    :returns blue_hist: the blue frequency values of the image's histogram
    :returns green_hist: the green frequency values of the image's
     histogram
    :returns x_vals: the intensity values of the image (0-255)
    """
    filename = ''
    if hist_type == 'hist_eq':
        filename = 'hist_equalized'+file_ext
    elif hist_type == 'rev_vid':
        filename = 'reverse_video'+file_ext
    elif hist_type == 'contrast_stretch':
        filename = 'contrast_stretched'+file_ext
    elif hist_type == 'log':
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
    logger.info('Histogram data successfully generated')
    return red_hist, blue_hist, green_hist, x_vals


# Create callable functions for each process
def initialize_image(image_string):
    """ Creates instance of Image class called 'image' with the input
    base64 string as the image_as_string attribute
    :param image_string: base64 string containing image data
    :return image: instance of Image class
    """
    image = Image(image_as_string=image_string)
    logger.info('Image initialized as instance of Image class')
    image.decode_string()
    image.gather_data()
    return image


# Histogram equalization - Callable Function
def histogram_eq_complete(image_string):
    """ Takes in base64 string, initializes an instance of Image class
    using this data, carries out histogram equalization, and generates
    plottable histogram data
    :param image_string: base64 string containing image data
    :return image: instance of Image class
    """
    image = initialize_image(image_string)
    hist_eq_array, run_time = image.hist_eq()
    red_hist, blue_hist, green_hist, x_vals = output_altered_histogram_data(
        'hist_eq', image.file_ext)
    base64_string = encode_string('hist_equalized', image.file_ext)
    return [red_hist, blue_hist, green_hist, x_vals, base64_string, run_time]


# Contrast stretching - Callable Function
def contrast_stretching_complete(image_string):
    """ Takes in base64 string, initializes an instance of Image class
    using this data, carries out contrast stretching, and generates
    plottable histogram data
    :param image_string: base64 string containing image data
    :returns red_hist: the red frequency values of the image's histogram
    :returns blue_hist: the blue frequency values of the image's histogram
    :returns green_hist: the green frequency values of the image's
     histogram
    :returns x_vals: the intensity values of the image (0-255) for histogram
    :returns base64_string: string containing data for altered image
    :returns run_time: the time it took to run the contrast stretching
    algorithm in seconds
    """
    image = initialize_image(image_string)
    contrast_stretch_array, run_time = image.contrast_stretch()
    red_hist, blue_hist, green_hist, x_vals = \
        output_altered_histogram_data('contrast_stretch', image.file_ext)
    base64_string = encode_string('contrast_stretched', image.file_ext)
    return [red_hist, blue_hist, green_hist, x_vals, base64_string, run_time]


# Reverse video - Callable Function
def reverse_video_complete(image_string):
    """ Takes in base64 string, initializes an instance of Image class
    using this data, carries out reverse video, and generates
    plottable histogram data
    :param image_string: base64 string containing image data
    :returns red_hist: the red frequency values of the image's histogram
    :returns blue_hist: the blue frequency values of the image's histogram
    :returns green_hist: the green frequency values of the image's
     histogram
    :returns x_vals: the intensity values of the image (0-255) for histogram
    :returns base64_string: string containing data for altered image
    :returns run_time: the time it took to run the reverse video
    algorithm in seconds
    """
    image = initialize_image(image_string)
    reverse_video_array, run_time = image.reverse_video()
    red_hist, blue_hist, green_hist, x_vals = \
        output_altered_histogram_data('rev_vid', image.file_ext)
    base64_string = encode_string('reverse_video', image.file_ext)
    return [red_hist, blue_hist, green_hist, x_vals, base64_string, run_time]


# Log Compression - Callable Function
def log_compression_complete(image_string):
    """ Takes in base64 string, initializes an instance of Image class
    using this data, carries out logarithmic compression, and generates
    plottable histogram data
    :param image_string: base64 string containing image data
    :returns red_hist: the red frequency values of the image's histogram
    :returns blue_hist: the blue frequency values of the image's histogram
    :returns green_hist: the green frequency values of the image's
     histogram
    :returns x_vals: the intensity values of the image (0-255) for histogram
    :returns base64_string: string containing data for altered image
    :returns run_time: the time it took to run the log compression algorithm
    algorithm in seconds
    """
    image = initialize_image(image_string)
    log_comp_array, run_time = image.log_compression()
    red_hist, blue_hist, green_hist, x_vals = \
        output_altered_histogram_data('log', image.file_ext)
    base64_string = encode_string('log_compressed', image.file_ext)
    return [red_hist, blue_hist, green_hist, x_vals, base64_string, run_time]


# Output histogram data for unaltered image
def histogram_data(image_string):
    """ Takes in base64 string, initializes an instance of Image class
    using this data, and generates plottable histogram data
    :param image_string: base64 string containing image data
    :returns red_hist: the red frequency values of the image's histogram
    :returns blue_hist: the blue frequency values of the image's histogram
    :returns green_hist: the green frequency values of the image's
     histogram
    :returns x_vals: the intensity values of the image (0-255) for histogram
    """
    image = initialize_image(image_string)
    red_hist, blue_hist, green_hist, x_vals = image.output_histogram_data(
        'original')
    return [red_hist, blue_hist, green_hist, x_vals]