from tensorflow.python.client import device_lib
import argparse



def get_available_gpus():
    local_device_protos = device_lib.list_local_devices()
    return [x.name for x in local_device_protos if x.device_type == 'GPU']


get_available_gpus()
import tensorflow as tf

tf.device(
    '/device:GPU:0'
)

from general_utils.processing import letterbox_image_padded, decode_detection_raw
from general_utils.visualization import visualize_detection

import cv2
import time
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import scipy.misc

colors = plt.cm.hsv(np.linspace(0, 1, 21)).tolist()

from detectors.yolov3 import YOLOv3_MobileNetV1
from detectors.yolov3 import YOLOv3_Darknet53
from detectors.ssd import SSD300, SSD512
from detectors.frcnn import FRCNN


import json
import cv2

(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')



def getFrame(sec):
    vidcap.set(cv2.CAP_PROP_POS_MSEC, sec * 1000)
    hasFrames, img = vidcap.read()
    return (img, hasFrames)


def generateCv2img(cv2img, tracker, count, starter, signal, track_signal, fps, detection_processed, pre_id, ok, loser,
                   path=None, display=False):
    fontScale = 0.7  # font & text block ratio
    # if len(detection_processed)>1:
    #  print("many objects in the "+str(count)+" image")

    if signal and len(detection_processed) >= 1:
        starter = count
        signal = False

    for box in detection_processed:

        id, label, conf = box[0], box[1], box[2]
        x1, y1, x2, y2 = box[3], box[4], box[5], box[6]
        cv2.rectangle(cv2img, (x1, y1), (x2, y2), (0, 255, 0), 6)

        labelSize = cv2.getTextSize(label, cv2.FONT_HERSHEY_COMPLEX, fontScale, 2)
        _x1 = x1
        _y1 = y1
        _x2 = _x1 + int(labelSize[0][0] * fontScale)
        _y2 = y1 - int(labelSize[0][1] * fontScale)
        cv2.rectangle(cv2img, (_x1, _y1), (_x2, _y2), (0, 255, 0), cv2.FILLED)
        cv2.putText(cv2img, label, (x1, y1), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)
        if count - starter == 0:
            pre_id = id
    meow = (count - starter) % fps
    print('track_signal=', track_signal, meow, len(detection_processed), pre_id)
    if (not ok and len(detection_processed) >= 1) or (
            not track_signal and (meow == 0 or meow == 1 or meow == 2 or meow == 3) and len(
            detection_processed) >= 1 and pre_id == id):
        print('gggtrack_signal=', track_signal)

        if count - starter > 0:
            print(tracker)
            try:
                del tracker
            except Exception as e:
                print(e)

        tracker = cv2.TrackerBoosting_create()

        print(meow, 'loser=', loser)
        ok = tracker.init(cv2img, (x1, y1, x2 - x1, y2 - y1))
        if ok:
            track_signal = True
            print('initial ok', (x1, y1, x2, y2))

            cv2.rectangle(cv2img, (x1, y1), (x2, y2), (255, 255, 255), 6)
        else:
            print('still not ok')
            track_signal = False

    elif tracker != None:
        # colding for tracking
        if not (meow == 0 or meow == 1 or meow == 2 or meow == 3):
            track_signal = False

        if ok:
            st_time = time.time()
            ok, b_box = tracker.update(cv2img)
            if ok:
                print('tracker time=', time.time() - st_time)
                #
                start_point, end_point = (int(b_box[0]), int(b_box[1])), (
                int(b_box[0]) + int(b_box[2]), int(b_box[1]) + int(b_box[3]))
                cv2.rectangle(cv2img, start_point, end_point, (0, 0, 255), 6)  #
                loser = 0
            else:
                track_signal = False
                print('checker update fails')
        if not ok:
            loser += 1
            print('not ok loser=', loser)
            ok, b_box = tracker.update(cv2img)

    if path != None:
        cv2.imwrite(path + str(count) + ".jpg", cv2img)

    if display:
        cv2_imshow(cv2img)

    return cv2img, tracker, signal, track_signal, starter, pre_id, ok, loser

    cv2.destroyAllWindows()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='sample command:  python run.py -vid videos/video.mp4 '
                                                 '-model')
    parser.add_argument("-vid", "--video_path", dest='video_path',
                        help="Path to the video to do detection")
    parser.add_argument("-model", "--model_detector", dest='model',
                        help="The detector model to use [frcnn | ssd300 | ssd512 | mobilenet | darknet | ensemble]")
    args = parser.parse_args()
    ensemble = False
    if args.model.lower() == 'frcnn':
        detector = FRCNN().cuda(device=0).load(r'model_weights/FRCNN_VOC0712_VGG16.pth')
    elif args.model.lower() == 'ssd300':
        detector = SSD300(weights=r'model_weights/SSD_VOC0712_VGG16_300x300.h5')
    elif args.model.lower() == 'ssd512':
        detector = SSD512(weights=r'model_weights/SSD_VOC0712_VGG16_512x512.h5')
    elif args.model.lower() == 'mobilenet':
        detector = YOLOv3_MobileNetV1(weights=r'model_weights/YOLOv3_VOC0712_MobileNetV1.h5')
    elif args.model.lower() == 'darknet':
        detector = YOLOv3_Darknet53(weights=r'model_weights/YOLOv3_VOC0712_Darknet53.h5')
    elif args.model.lower() == 'ensemble':
        ensemble = True
        detector_ssd = SSD300(weights=r'model_weights/SSD_VOC0712_VGG16_300x300.h5')
        detector_yolo = YOLOv3_MobileNetV1(weights=r'model_weights/YOLOv3_VOC0712_MobileNetV1.h5')
        detector_dn = YOLOv3_Darknet53(weights=r'model_weights/YOLOv3_VOC0712_Darknet53.h5')
    else:
        print('Supplied model name not recognized. Exiting...')
        exit()

    try:
        vidcap = cv2.VideoCapture(args.video_path)
    except Exception as e:
        # vidcap = cv2.VideoCapture(r'videos/president-on-tech-green.mov')
        # vidcap = cv2.VideoCapture(r'videos/video.mp4')
        # vidcap = cv2.VideoCapture(r'videos/man-walking-in-tokyo.mov')
        # vidcap = cv2.VideoCapture(r'videos/night_drive.mov')
        # vidcap = cv2.VideoCapture(r'videos/racing_car.mov')
        print(e)
        print('Error loading video. Exiting...')
        exit()

    # Parameters
    sec = 0
    fps = 10
    frameRate = 1.0 / fps  # interval between frames
    count = 0
    success = getFrame(sec)
    images = []
    cv2imgs = []
    times = []
    confidence_list = []
    starter = 0
    signal = True
    track_signal = False
    # Convert the video to frames and make prediction
    modelName = "yolov3mobile"
    path = r'output/'
    result_imgs = []
    results = []
    tracker = None
    pre_id = -1
    ok = False
    loser = 0
    while success:
        count = count + 1
        sec = sec + frameRate
        sec = round(sec, 2)
        image, success = getFrame(sec)

        if not success:
            continue

        # convert np array back to image

        cv2img = image
        cv2imgs.append(image)
        image = Image.fromarray(image)
        images.append(image)

        # Time and make prediction
        start = time.time()
        if ensemble:
            # detect from each model
            # detection_processed in form (class_num, class_name, confidence, bb1, bb2, bb3, bb4)
            x_query, x_meta = letterbox_image_padded(image, size=detector_yolo.model_img_size)
            detection_raw_yolo = detector_yolo.detect(x_query, conf_threshold=detector_yolo.confidence_thresh_default)
            detection_processed_yolo = decode_detection_raw(detection_raw_yolo, x_meta, detector_yolo.classes)

            x_query, x_meta = letterbox_image_padded(image, size=detector_ssd.model_img_size)
            detection_raw_ssd = detector_ssd.detect(x_query, conf_threshold=detector_ssd.confidence_thresh_default)
            detection_processed_ssd = decode_detection_raw(detection_raw_ssd, x_meta, detector_ssd.classes)

            x_query, x_meta = letterbox_image_padded(image, size=detector_dn.model_img_size)
            detection_raw_dn = detector_dn.detect(x_query, conf_threshold=detector_dn.confidence_thresh_default)
            detection_processed_dn = decode_detection_raw(detection_raw_dn, x_meta, detector_dn.classes)

            dim = max(len(detection_processed_yolo), len(detection_processed_ssd), len(detection_processed_dn))
            detections = [detection_processed_yolo, detection_processed_dn, detection_processed_ssd]
            det_matrix = []

            # create mxn matrix of model predictions. m = number of models,
            # n = max(number of objects detected by any model in frame)
            for d in detections:
                row = []
                for j in range(0, dim):
                    if j > len(d) - 1:
                        row.append([])
                    else:
                        row.append(d[j])
                det_matrix.append(row)

            detection_processed = []
            conf = False
            # voting process
            for det_num in range(len(det_matrix[0])):
                conf = False
                vote_count = 0
                max_pred = None
                max_conf = -1
                for model_det in det_matrix:
                    d = model_det[det_num]
                    # if a detection was made by the model
                    if len(d):
                        try:
                            if max_pred is None:
                                max_pred = d
                            # if the bounding box is different and the confidence is high enough
                            elif d[2] > max_conf and sum([(d[i] - max_pred[i]) / (d[i]+1) for i in range(3, 7)]) / 4 > 0.05:
                                max_conf = d[2]
                                max_pred = d
                            # if the confidence is higher than 0.9 automatically add
                            if d[2] > 0.9:
                                conf = True
                            vote_count += 1
                        except Exception as e:
                            print(e)

                if conf or vote_count >= 2:
                    detection_processed.append(max_pred)
        else:
            x_query, x_meta = letterbox_image_padded(image, size=detector.model_img_size)
            detection_raw = detector.detect(x_query, conf_threshold=detector.confidence_thresh_default)
            detection_processed = decode_detection_raw(detection_raw, x_meta, detector.classes)

        times.append(time.time() - start)
        print('detection', time.time() - start)

        # Generate and save the result image
        result_img, tracker, signal, track_signal, starter, pre_id, ok, loser = generateCv2img(cv2img, tracker, count,
                                                                                               starter, signal,
                                                                                               track_signal, fps,
                                                                                               detection_processed,
                                                                                               pre_id, ok, loser,
                                                                                               path=path)
        result_imgs.append(result_img)

        # Collect the result
        results.append(detection_processed)
        if len(detection_processed):
            confidence_list.append(detection_processed[0][2])
    print("Prediction time list", times)
    print("Max:", max(times))
    print("Min:", min(times))
    print("Avg:", sum(times) / len(times))
    print("sec list:", times)
    print('max conf: ', max(confidence_list))
    print('min conf: ', min(confidence_list))
