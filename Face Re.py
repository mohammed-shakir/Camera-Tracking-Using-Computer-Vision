import cv2
import imutils
import numpy as np
import tensorflow as tf

# Loading the YOLO model
model = tf.keras.models.load_model('path_to_yolo_model.h5')

# Reading the video stream from a local file
# Replace the file path with the location of your video file
cap = cv2.VideoCapture("path_to_video_file.mp4")

while cap.isOpened():
    # Reading the video stream
    ret, image = cap.read()
    if ret:
        image = imutils.resize(image, width=min(1080, image.shape[1]))

        # Pre-processing the image for the model
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = tf.expand_dims(image, axis=0)
        image = image / 255.0

        # Running the YOLO model to detect objects
        pred = model.predict(image)

        # Decoding the predictions
        boxes, confidences, class_ids = [], [], []
        for out in pred[0]:
            # Extracting the class_id, confidence, and box coordinates
            class_id = np.argmax(out[5:])
            confidence = out[4]
            if confidence > 0.5:
                x, y, w, h = out[0:4] * [image.shape[2], image.shape[1], image.shape[2], image.shape[1]]
                x = int(x - w / 2)
                y = int(y - h / 2)
                boxes.append([x, y, int(w), int(h)])
                confidences.append(float(confidence))
                class_ids.append(class_id)

        # Drawing the bounding boxes around the detected objects
        for i in range(len(boxes)):
            if class_ids[i] == 0:  # Class 0 is the person class
                (x, y, w, h) = boxes[i]
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # Showing the output Image
        cv2.imshow("Person Detection", image)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
