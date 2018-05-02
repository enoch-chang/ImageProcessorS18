# ImageProcessorS18[![Build Status](https://travis-ci.org/enoch-chang/ImageProcessorS18.svg?branch=master)](https://travis-ci.org/enoch-chang/ImageProcessorS18)
BME590 Final Project MyLittlePony 
## About this Software
### Introduction
### Front End
- INSERT IMAGE HERE - 
### Image Processing Module
The backend code of this project runs off a module named Image_processing.py, which contains several different functions to gather data about input images as well as to carry out image processing techniques on the uploaded images. It does so via estabilshing an Image class, which is initialized by inputting a base64 string containing the image data. This file format allows for image data to be transmitted back and forth between the VCM running this software and the client's machine making requests to it. The software functions by writing first converting the base64 string to a numpy array containing image data then saving the image to disc. These two image formats can be used to gather all pertinent information about the image (size, file extensions, etc) as well as to carry out the image processing techniques. The software is centered around four main functions: 
* histogram_equalization_complete(image_string)
* contrast_stretching_complete(image_string)
* reverse_video_complete(image_string)
* log_compression_complete(image_string)
## Setup Instructions
## Using the Software
## Other Notes
