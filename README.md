# ImageProcessorS18[![Build Status](https://travis-ci.org/enoch-chang/ImageProcessorS18.svg?branch=master)](https://travis-ci.org/enoch-chang/ImageProcessorS18) [![Documentation Status](https://readthedocs.org/projects/imageprocessings18/badge/?version=latest)](http://imageprocessings18.readthedocs.io/en/latest/?badge=latest)

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

Each of these functions takes in a base64 string encoding for an image, carries out the specified image processing technique, then returns a base64 string encoding for the altered image along with the image's histogram data and the time it took to run the technique. 
## Setup Instructions
First, log into your VCM then spin up the database using the command "sudo mongod." After the database is running, open a new terminal window, log into your VCM again, cd into the folder titled "ImageProcessorS18", then run the flask applcation with the command "gunicorn --bind 0.0.0.0:5000 main:app". If you wish to use this application for an extended period, open these in a screen. If you set up the database on a machine other than http://vcm-3608.vm.duke.edu, specify the machine in Server.py. 
## Using the Software
## Other Notes
### Project Documentation
**RFC:** https://docs.google.com/document/d/1Mu7KEPWHF65n9_sypfO7raDynyUtr3FiK_S0V3Ok178/edit?usp=sharing
**Software Documentation:** imageprocessings18.readthedocs.io
