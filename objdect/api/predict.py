"""REST API for object prediction."""
import os
import matplotlib.pyplot as plt
import numpy as np
import base64
import cv2

import time
import json
from PIL import Image
import scipy.misc
colors = plt.cm.hsv(np.linspace(0, 1, 21)).tolist()

# import model_zoo

import flask
import objdect


def gen():
    app_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    prefix = app_path+'/var/output/yolov3dark24/'
    intervals = json.loads(json.load(open(prefix+'intervals.json')))
    counter = 0
    while counter < len(intervals):
        time.sleep(intervals[counter])
        counter += 1
        frame_name = prefix+str(counter)+'.jpg'
        frame = open(frame_name,'rb').read()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@objdect.app.route('/api/predict/', methods=["GET","POST"])
def video_feed():
    return flask.Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


# @objdect.app.route('/api/predict/<int:frame>',
#                     methods=["GET"])
# def send_prediction(frame):
#     """Return pre-calculated object prediction."""
#     print("api/predict/<int:frame>")
#     filename = 'var/output/ssd500/1.0FPS_'+str(frame)+'.jpg'
#     return flask.send_file(filename, mimetype='jpg')


# @objdect.app.route('/api/predict/', methods=["GET","POST"])
# def predict():
#     """Object prediction."""
#     print("/api/predict/")
#     context = {
#         "hello": "success"
#     }
#     code = 200
#     print(flask.request.json["hello"])
#     # open image from http request
#     image = flask.request.json["image"]
#     img = objdect.api.utils.readb64(image)
#     # run predictor
#     ssd_predictor(img)

#     # construct response and return
#     # prediction = img
#     # context["image"] = prediction
#     return flask.jsonify(**context), code


# def ssd_predictor(image):
#     detector = model_zoo.detectors.ssd.SSD512(weights='../zoo/model_weights/SSD_VOC0712_VGG16_512x512.h5')
#     x_query, x_meta = model_zoo.general_utils.processing.letterbox_image_padded(image, size=detector.model_img_size)
#     detection_raw = model_zoo.detector.detect(x_query, conf_threshold=detector.confidence_thresh_default)
#     detection_processed = model_zoo.general_utils.processing.decode_detection_raw(detection_raw, x_meta, detector.classes)

#     model_zoo.general_utils.visualization.visualize_detection(image, detection_processed)
    

# def save_prediction(image, detection_processed):
#     # Generate and save the result image
#     plt.clf()
#     plt.figure(figsize=(3, 3))
#     plt.imshow(image)
#     current_axis = plt.gca()
#     for box in detection_processed:
#         class_id = box[0]
#         class_name = box[1]
#         confidence = box[2]
#         xmin, ymin, xmax, ymax = box[3:]
#         color = colors[class_id]
#         label = '{}: {:.2f}'.format(class_name, confidence)
#         current_axis.add_patch(
#             plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin, color=color, fill=False, linewidth=2))
#         current_axis.text(xmin, ymin, label, size='small', color='black', bbox={'facecolor': color, 'alpha': 1.0})
#     plt.axis('off')
#     plt.savefig('./output/SSD512/FPS.jpg')
    

