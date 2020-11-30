from PIL import Image
import numpy as np


def letterbox_image_padded(image, size):
    """ Resize image with unchanged aspect ratio using padding """
    image_copy = image.copy()
    iw, ih = image_copy.size
    w, h = size
    scale = min(w / iw, h / ih)
    nw = int(iw * scale)
    nh = int(ih * scale)

    image_copy = image_copy.resize((nw, nh), Image.BICUBIC)
    new_image = Image.new('RGB', size, (0, 0, 0))
    new_image.paste(image_copy, ((w - nw) // 2, (h - nh) // 2))
    new_image = np.asarray(new_image)

    meta = ((w - nw) // 2, (h - nh) // 2, nw + (w - nw) // 2, nh + (h - nh) // 2, scale)
    mask = np.zeros(shape=(1, *new_image.shape))
    mask[:, meta[1]:meta[3], meta[0]:meta[2], :] = 1.
    new_image = np.asarray([new_image]) / 255.
    return new_image, meta


def bbox_to_original_scale(bbox, margin_left, margin_top, margin_right, margin_bottom, scale):
    xmin, ymin, xmax, ymax = list(map(int, bbox))
    if not (margin_left <= (xmin + xmax) / 2. <= margin_right and margin_top <= (ymin + ymax) / 2. <= margin_bottom):
        return None
    xmin = int((max(margin_left, xmin) - margin_left) / scale)
    ymin = int((max(margin_top, ymin) - margin_top) / scale)
    xmax = int((min(margin_right, xmax) - margin_left) / scale)
    ymax = int((min(margin_bottom, ymax) - margin_top) / scale)
    return xmin, ymin, xmax, ymax


def decode_detection_raw(detection_raw, x_meta, classes):
    detections_processed = []
    for row in detection_raw:
        bbox_raw = map(int, row[-4:])
        bbox = bbox_to_original_scale(bbox_raw, *x_meta)
        if bbox is None:
            continue
        class_id = int(row[0])
        class_name = classes[class_id]
        confidence = float(row[1])
        detections_processed.append((class_id, class_name, confidence, *bbox))
    return detections_processed
