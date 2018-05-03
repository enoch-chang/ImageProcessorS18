# ImageProcessorS18    [![Build Status](https://travis-ci.org/enoch-chang/ImageProcessorS18.svg?branch=master)](https://travis-ci.org/enoch-chang/ImageProcessorS18) [![Documentation Status](https://readthedocs.org/projects/imageprocessings18/badge/?version=latest)](http://imageprocessings18.readthedocs.io/en/latest/?badge=latest) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**BME590 Final Project MyLittlePony**  
**Created by:** Enoch Chang, Anthony Schneider, Rich Wang

## About this Software
### Introduction
This repository contains an image processing web application that contains the front-end (React application), back-end (Flask) and associated algorithms. Users can create accounts to upload images, access previously uploaded images saved under their e-mail and perform image processing. As each image (both original or processed) is selected, additional metrics are displayed underneath the image.

### Front End

1. Enter your e-mail and click "LOG IN". 

![alt text](https://github.com/enoch-chang/ImageProcessorS18/blob/readme/screenshots/login.png?raw=true)

2. If this is your first log in, you will be prompted with a quick sign-up where you will be required to enter your name. Click 'CREATE NEW USER' when ready and you will be logged into the new user profile created.

If you wish to use another e-mail, clicking 'BACK' returns you to the log in screen and you may start again. 

![alt text](https://github.com/enoch-chang/ImageProcessorS18/blob/readme/screenshots/create-user.png)

3. Upon accessing a user profile, the upload option will be available. Simply select your files and click 'UPLOAD'.

NOTE: files must be either .jpg or .png and must be 1 MB or smaller.

You may also access another user profile by clicking 'CHANGE USER'.

![alt text](https://github.com/enoch-chang/ImageProcessorS18/blob/readme/screenshots/logged-in.png?raw=true)

4. You will be able to browse all images stored under your user profile as listed by filename and upload date in the table below. To view an image and its associated metrics, simply click on the filename of interest.

![alt text](https://github.com/enoch-chang/ImageProcessorS18/blob/readme/screenshots/viewer.png?raw=true)

5. As an image is selected, the file browser will refresh with processed images associated with the original image selected. The processed images will be listed again by filename and upload date. Clicking on a processed image will refresh the image viewer below with the image and metrics under the 'PROCESSED' tab. You may use the tabs to switch between the image and metrics of the original and processed images.

If, at any point, you would like to view other images not on the current list, simply click 'VIEW ALL ORIGINAL IMAGES'.

![alt text](https://github.com/enoch-chang/ImageProcessorS18/blob/readme/screenshots/viewer-p.png?raw=true)

6. The selected image under the 'ORIGINAL' tab can then be processed by a number of image processing techniques. Select the processing wanted from the drop-down menu and click 'GO!'.

![alt text](https://github.com/enoch-chang/ImageProcessorS18/blob/readme/screenshots/process.png?raw=true)


### Image Processing Module
The backend code of this project runs off a module named Image_processing.py, which contains several different functions to gather data about input images as well as to carry out image processing techniques on the uploaded images. It does so via estabilshing an Image class, which is initialized by inputting a base64 string containing the image data. This file format allows for image data to be transmitted back and forth between the VCM running this software and the client's machine making requests to it. The software functions by writing first converting the base64 string to a numpy array containing image data then saving the image to disc. These two image formats can be used to gather all pertinent information about the image (size, file extensions, etc) as well as to carry out the image processing techniques. The software is centered around four main functions: 
* histogram_equalization_complete(image_string)
* contrast_stretching_complete(image_string)
* reverse_video_complete(image_string)
* log_compression_complete(image_string)  

Each of these functions takes in a base64 string encoding for an image, carries out the specified image processing technique, then returns a base64 string encoding for the altered image along with the image's histogram data and the time it took to run the technique.

### Back End 
This program is running by Duke VCM. The backend code combines Server.py, mainfunction.py and models.py. The Server.py contains ```GET``` and ```POST``` connecting front end and image processing modules. ```GET /api/images/<user_email>
``` is for user to retrieve their data from this program database, MongoDB container. ```POST /api/images/create``` is for user creating their information in program database, which takes input user email and user name. ```POST /api/images/upload
 ```   is for the connection between front end and database. This function can help user store their uploading images in program database with the image information, including base64 string, filename, filetype, time stamp, image size and the original image histogram. ```POST /api/images/<email>/<filename>/process``` takes front end input image and image process type. After processing, this function will store the processed image information such as base64 string, processed image name with process type, original image name, time stamp, processing time duration and optional processed histogram. In the models.py, there is four fields, ```Email, Name, Image and Processed Image```, to store data in this programs.
 
## Setup Instructions
The current version of the code interacts with a server located on a continuously running VCM service (```http://vcm-3608.vm.duke.edu:5000```).

To deploy the server and back-end algorithms on a different machine, log into your VCM then spin up the database using the command "sudo mongod." After the database is running, open a new terminal window, log into your VCM again, cd into the folder titled "ImageProcessorS18", then run the flask applcation with the command ```"gunicorn --bind 0.0.0.0:5000 main:app"```. If you wish to use this application for an extended period, open these in a screen. If you set up the database on a machine other than ```http://vcm-3608.vm.duke.edu```, the machine must be specified in both the server code and the front end code. To run the front end code, you must then cd into the front-end folder, then image-processor, then run 'npm run start'.

## Other Notes
Due to volatility and unpredictability of the performance of the VCM, please expect high latency and fail rate of all GET/POST requests. Multiple attempts WILL be required for every request.

### Project Documentation
**RFC:** https://docs.google.com/document/d/1Mu7KEPWHF65n9_sypfO7raDynyUtr3FiK_S0V3Ok178/edit?usp=sharing
**Software Documentation:** imageprocessings18.readthedocs.io

### MIT License
MIT License

Copyright (c) [2018] [Enoch Chang], [Anthony Schneider], [Rich Wang]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
