# Face colorization website

## Introduction
 This is a website that automatically colorize grayscale face images. The purpose of this website is to help quickly colorize old portrait photos from the past that are usually black and white.
## Technical Overview
About the AI model:
- Using the [CelebA dataset](https://mmlab.ie.cuhk.edu.hk/projects/CelebA.html)
- Using autoencoder network

About website:
- Using Django framework
## How to install
- After downloading the code, install the requirements in the *requirements.txt* file.
```sh
pip install -r requirements.txt
```
- In the folder *face-colorization-website/mysite* create a *media* subfolder, in the *media* folder continue to create 2 subfolders *uploads* and *converted* to contain images.
- In the folder *face-colorization-website/mysite/colorweb* create a *my_model* subfolder and put the *colorize_face_model.h5* file here. This model can be found [here](https://drive.google.com/file/d/1h5DAnlMxl-YjyphX_lNXtL_YU6nbC0F8/view?usp=sharing). (Code to train the colorize model is [here](https://colab.research.google.com/drive/17rpJ1OQTG6wpP-m7rNkL4X1RkndSaYsx?usp=sharing))
- In the file *face-colorization-website/mysite/colorweb/convert_image.py*, change the path to the *colorize_face_model.h5* file to load the model.
## Usage
To run the website, at the terminal:
- Must be in the directory *face-colorization-website/mysite*. 
- First, create database:
```sh
py manage.py makemigrations
```
```sh
py manage.py migrate
```
- Then run server:
```sh
py manage.py runserver
```
- When the command runs successfully, you can access the link on the terminal:
+ Website link: http://127.0.0.1:8000/
+ API link: http://127.0.0.1:8000/api/my_image_conversion/

This website has a number of functions such as: register, login, logout, upload/download images, convert images.
- If user is not logged in, user can convert and download photos.
- For those who are logged in, besides the above functions, they can see some images they have converted before and download them.
