
import cv2
import jetson.inference
import jetson.utils

from  jetson.utils import cudaToNumpy
import numpy as np
import time

# function
def rgba2rgb(rgba, background=(255,255,255)):
    row, col, ch = rgba.shape

    if ch == 3:
        return rgba

    assert ch == 4, 'RGBA image has 4 channels.'

    rgb = np.zeros((row, col, 3), dtype='float32')
    r, g, b, a = rgba[:,:,0], rgba[:,:,1], rgba[:,:,2], rgba[:,:,3]

    a = np.asarray(a, dtype='float32') / 255.0

    R, G, B = background

    rgb[:,:,0] = r * a + (1.0 - a) * R
    rgb[:,:,1] = g * a + (1.0 - a) * G
    rgb[:,:,2] = b * a + (1.0 - a) * B

    return np.asarray(rgb, dtype='uint8')


def get_iou(boxA, boxB):
    lA = boxA[0]
    rA = boxA[0] + boxA[2]
    tA = boxA[1]
    bA = boxA[1] + boxA[3]

    lB = boxB[0]
    rB = boxB[0] + boxB[2]
    tB = boxB[1]
    bB = boxB[1] + boxB[3]

    xA = max(lA, lB)
    yA = max(tA, tB)
    xB = min(rA, rB)
    yB = min(bA, bB)

    interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)

    boxAArea = (rA - lA + 1) * (bA - tA + 1)
    boxBArea = (rB - lB + 1) * (bB - tB + 1)

    iou = interArea / float(boxAArea + boxBArea - interArea)

    return iou if iou > 0 else -iou


img_pre_time, tracker_init_time, tracker_update_time = 0, 0, 0

# detection
net = jetson.inference.detectNet("ssd-inception-v2", threshold=0.55)
camera = jetson.utils.gstCamera(1280, 720, "0")
# camera = jetson.utils.gstCamera(1920, 1080, "0")
display = jetson.utils.glDisplay()

# Tracker
re_init_limit = 5
re_init_counter = 0; 
tracker = cv2.TrackerBoosting_create()

while display.IsOpen():
    img, width, height = camera.CaptureRGBA(zeroCopy=1)
    detections = net.Detect(img, width, height)
   
    # if detected something, prepare np array in rgb for the tracker
    if len(detections) > 0:            
        img_pre_start = time.time()
        img_np = cudaToNumpy(img)       # Convert to np.array in rgb
        img_np_rgb = rgba2rgb(img_np)
        img_pre_time = (time.time() - img_pre_start)*1000

        # if reach the thetime, re-initiate
        if re_init_counter >= re_init_limit:
            tracker_init_start = time.time()
            ok = tracker.init(img_np_rgb, (detections[0].Left, detections[0].Top , detections[0].Width ,detections[0].Height ))
            tracker_init_time = (time.time() - tracker_init_start)*1000 

            re_init_counter = 0
            b_box = [0,0,0,0]
            print('* * * Initiate the tracker * * * ')
        # else, just update
        else:
            tracker_update_start = time.time()
            ok, b_box = tracker.update(img_np_rgb)
            tracker_update_time = (time.time() - tracker_update_start)*1000
            iou = get_iou( \
                [detections[0].Left, detections[0].Top , detections[0].Width ,detections[0].Height], \
                b_box)   
            print('- - - Updated the tracker - - - ')
            print('Tracker:', b_box)
            print('Predict:', "({:.1f}, {:.1f}, {:.1f}, {:.1f})".format( \
                detections[0].Left, detections[0].Top , detections[0].Width ,detections[0].Height))
            print("IoU    :", "None" if iou == 1 or b_box == [0,0,0,0] else "{:.2%}".format(iou))
          

        # results
        print("Prediction time      :", net.GetNetworkTime())
        print("Image converting time:", 0 if img_pre_time == 0 else img_pre_time)
        print("Tracker initial time :", 0 if tracker_init_time == 0 else tracker_init_time)
        print("Tracker update time  :", 0 if tracker_update_time == 0 else tracker_update_time)
        
        print("")        
        img_pre_time, tracker_init_time, tracker_update_time = 0, 0, 0
        b_box = [0,0,0,0]
    
    re_init_counter += 1
    
    # Render the stream 
    display.RenderOnce(img, width, height)
    display.SetTitle("Object Detection | Network {:.0f} FPS | Time {:.8f}".format(net.GetNetworkFPS(), net.GetNetworkTime()))









