import cv2
import imutils
from controller import Controller

cont = Controller()

# Initializing the HOG person
# detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

cap = cv2.VideoCapture("http://130.240.105.144/cgi-bin/mjpeg?resolution=1920x1080&amp;framerate=120&amp;quality=1")

while cap.isOpened():
    # Reading the video stream
    ret, image = cap.read()

    if ret:
        image = imutils.resize(image,
                               width=min(400, image.shape[1]))
        
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detecting all the regions
        # in the Image that has a
        # pedestrians inside it
        (regions, _) = hog.detectMultiScale(image,
                                            winStride=(4, 4),
                                            padding=(8, 8),
                                            scale=1.01)

        # Drawing the regions in the
        # Image
        for (x, y, w, h) in regions:
            if(len(regions) > 1):
                break
            cv2.rectangle(image, (x, y),
                            (x + w, y + h),
                            (0, 0, 255), 2)            

            # Print coordinates of detected person
            #print("x: " + str(x) + " y: " + str(y) + " width: " + str(w) + " height: " + str(h))
            # find center of person
            center_x = x + w / 2
            center_y = y + h / 2
            print("center_x: " + str(center_x) + " center_y: " + str(center_y))

            if(x < 100):
                print("left")
                cont.left()
            elif((x+w) > 300):
                print("right")
                cont.right()
            else:
                print("center")

        # Showing the output Image
        cv2.imshow("Image", image)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()