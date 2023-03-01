import cv2
import argparse
import numpy as np
import imutils
import sys
sys.path.insert(0, 'C:/Users/moham/Documents/code/Camera-Tracking-Using-UWB-Navigation')
from controller import Controller

controller = Controller()

controller.rotate(180, 140)

ap = argparse.ArgumentParser()
ap.add_argument('-c', '--config', required=True,
                help = 'path to yolo config file')
ap.add_argument('-w', '--weights', required=True,
                help = 'path to yolo pre-trained weights')
ap.add_argument('-cl', '--classes', required=True,
                help = 'path to text file containing class names')
args = ap.parse_args()

def get_output_layers(net):
    layer_names = net.getLayerNames()
    try:
        output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    except:
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    return output_layers

def draw_prediction(img, class_id, confidence, x, y, x_plus_w, y_plus_h):
    '''
    global person_class_id

    if class_id == person_class_id:
        label = str(classes[class_id])
        color = COLORS[class_id]
        cv2.rectangle(img, (x,y), (x_plus_w,y_plus_h), color, 2)
        cv2.putText(img, label, (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    '''
    if class_id == 0:
        label = 'person'
        color = (0, 255, 0) # green
        cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)
        cv2.putText(img, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)    

'''
classes = None
person_class_id = None

with open(args.classes, 'r') as f:
    classes = [line.strip() for line in f.readlines()]
    person_class_id = classes.index("person")

COLORS = np.random.uniform(0, 255, size=(len(classes), 3))
''' 

net = cv2.dnn.readNet(args.weights, args.config)

conf_threshold = 0.5
nms_threshold = 0.4

cap = cv2.VideoCapture(controller.kitchenCameraURL)

while True:
    ret, frame = cap.read()
    
    if not ret:
        break

    frame = imutils.resize(frame, width=min(800, frame.shape[1]))

    Width = frame.shape[1]
    Height = frame.shape[0]
    scale = 0.00392

    blob = cv2.dnn.blobFromImage(frame, scale, (256,256), (0,0,0), True, crop=False)

    net.setInput(blob)

    outs = net.forward(get_output_layers(net))

    class_ids = []
    confidences = []
    boxes = []

    person_found = False

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > conf_threshold:
                center_x = int(detection[0] * Width)
                center_y = int(detection[1] * Height)
                w = int(detection[2] * Width)
                h = int(detection[3] * Height)
                x = center_x - w / 2
                y = center_y - h / 2
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])
                # print("x: ", x, "y: ", y, "w: ", w, "h: ", h)

                if (x < 10):
                    print("left")
                    controller.left()
                elif ((x+w) > 790):
                    print("right")
                    controller.right()
                if (y < 10):
                    print("up")
                    controller.up()
                elif ((y+h) > 380):
                    print("down")
                    controller.down()
                

                person_found = True
                break

        if person_found:
            break

    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

    for i in indices:
        try:
            box = boxes[i]
        except:
            i = i[0]
            box = boxes[i]

        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]
        draw_prediction(frame, class_ids[i], confidences[i], round(x), round(y), round(x+w), round(y+h))

    cv2.imshow("object detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
