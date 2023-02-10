import cv2
import imutils

# Initializing the HOG person
# detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

cap = cv2.VideoCapture("http://130.240.105.145/cgi-bin/mjpeg?resolution=1920x1080&amp;framerate=120&amp;quality=1")

while cap.isOpened():
    # Reading the video stream
    ret, image = cap.read()
    if ret:
        image = imutils.resize(image,
                               width=min(400, image.shape[1]))

        # Detecting all the regions
        # in the Image that has a
        # pedestrians inside it
        (regions, _) = hog.detectMultiScale(image,
                                            winStride=(2, 2),
                                            padding=(4, 4),
                                            scale=0.9)

        # Drawing the regions in the
        # Image
        for (x, y, w, h) in regions:
            cv2.rectangle(image, (x, y),
                          (x + w, y + h),
                          (0, 0, 255), 2)

            # Print coordinates of detected person
            print("x: " + str(x) + " y: " + str(y) + " width: " + str(w) + " height: " + str(h))
            # find center of person
            center_x = x + w / 2
            center_y = y + h / 2
            print("center_x: " + str(center_x) + " center_y: " + str(center_y))

        # Showing the output Image
        cv2.imshow("Image", image)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()