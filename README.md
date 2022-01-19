
# Facial Recognition Web Application using Flask

[![Watch the video](https://github.com/AlejandroSoumah/WebApplication_FaceRecognition/blob/main/FaceRecon.png)](https://youtu.be/BaHZWi6Kbcg)

This is a real-time facial recognition web application based on OpenCV. It is an execution of an OpenCV based facial recognition, it uses graphic interface using a website. It uses Flask (micro web framework written in Python) in order to execute the OpenCV facial recognition model, it works by using a webcam connected to your computer and getting the input from there. In order to be able to have your face recgnized a "database" of it needs to be created. It is created as seen in the video. It uses OpenCV real-time facial recognition and joins it with Flask to create a facial recognition web application that works for two users simultaneously.
## Table of contents
* [ Installation](#Installation)
* [ Execution](#Execution)
* [ Setup](#Setup)


### Installation:
   1. Install Python x3-6
   2. Install OpenCV
   3. Install Numpy
   4. Install Flask


### 2.0 Execution
   1. Execute the script <b> client2.py </b>
   3. Wait for execution to occur and website to load
   4. Create Dataset of your face, look at the camera and slowly turn your face to capture different angles
   5. Another user can repeat step 3, to create a dataset for another face.
   6. Click button <b>RUN</b> to execute
   7. Look at results

## 3.0 Setup
To run this project, install it locally using npm:

```
$ pip install opencv-contrib-python
$ pip install numpy
$ pip install flask
$ cd WebApplication_FaceRecognition/
$ export FLASK_APP=client2
$ python -m flask run
```
## Sources
OpenCV documentation https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html

