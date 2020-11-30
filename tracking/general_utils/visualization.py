import matplotlib.pyplot as plt
import numpy as np
colors = plt.cm.hsv(np.linspace(0, 1, 21)).tolist()


def visualize_detection(input_img, detections):
    plt.clf()
    plt.figure(figsize=(3, 3))
    plt.imshow(input_img)
    current_axis = plt.gca()
    for box in detections:
        class_id = box[0]
        class_name = box[1]
        confidence = box[2]
        xmin, ymin, xmax, ymax = box[3:]
        color = colors[class_id]
        label = '{}: {:.2f}'.format(class_name, confidence)
        current_axis.add_patch(
            plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin, color=color, fill=False, linewidth=2))
        current_axis.text(xmin, ymin, label, size='small', color='black', bbox={'facecolor': color, 'alpha': 1.0})
    plt.axis('off')
    plt.show()

