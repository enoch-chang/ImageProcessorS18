import os
import skimage
import numpy
import matplotlib
import numpy as np
import png

from skimage import io
from skimage import data, img_as_float
from skimage import exposure

# Load Image
image_name = 'bad_contrast.JPEG'
image = io.imread(image_name)


# Equalization
img_eq = exposure.equalize_hist(image)

skimage.io.imsave('hist_equalized.JPEG', img_eq, plugin=None)
