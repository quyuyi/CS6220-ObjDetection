# Installation
1. Create a virtual environment
2. Activate the virtual environment
3. Install libraries: `pip install -r requirements.txt`

Requirements are slightly different than the original object detection zoo in order to run on the Windows 10 machine used for testing. The testing and packages used were those compatible with CUDA 10 on a NVIDIA GeForce graphics card, so it is possible that you may need to install a different version of tensorflow.

# Running the file
The ensemble method and standard object tracking are both run using the run.py file. run.py takes command line arguments for video path and model. 
Example command: "python run.py -vid videos/video.mov -model frcnn" 
The -vid argument is the path to the video to use for object detection. The videos folder in the working directory contains sample videos. 
The -model argument is the type of model to use for the detector. 
The options for model are 'frcnn', 'ssd300', 'ssd512', 'mobilenet', 'darknet', 'ensemble'. 
Choosing 'ensemble' will run the weighted confidence ensemble method of SSD300, Yolo3 Mobilenet, and Yolo3 Darknet described in our report.

The object tracking will run regardless of the choice of the model. Output images of video stills with bounding boxes will be saved to an output folder. Note that the output folder must exist before running, and existing images in the output folder will be overwritten for each run.

# 

# Acknowledgement
This project is developed based on the following repositories:
* [qqwweee/keras-yolo3](https://github.com/qqwweee/keras-yolo3)
* [Adamdad/keras-YOLOv3-mobilenet](https://github.com/Adamdad/keras-YOLOv3-mobilenet)
* [pierluigiferrari/ssd_keras](https://github.com/pierluigiferrari/ssd_keras)
* [chenyuntc/simple-faster-rcnn-pytorch](https://github.com/chenyuntc/simple-faster-rcnn-pytorch)
