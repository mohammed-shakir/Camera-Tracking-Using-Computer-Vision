import cv2
import imutils
from controller import Controller

controller = Controller()
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

kitchenCamera = cv2.VideoCapture(controller.kitchenCameraURL)
print(kitchenCamera.isOpened())
bedroomCamera = cv2.VideoCapture(controller.bedroomCameraURL)


def drawregion(image, regions, captureCamera, _):
    # Drawing the regions in the Image
    for i, (x, y, w, h) in enumerate(regions):
        if _[i] > 0.5:
            cv2.rectangle(image, (x, y),
                          (x + w, y + h),
                          (0, 0, 255), 2)

            # print(_[i])

            # find center of person
            center_x = x + w / 2
            center_y = y + h / 2

            print("center_x: " + str(center_x) + " center_y: " + str(center_y))
            if captureCamera == bedroomCamera:
                controller.followPerson(x, y, w, "Bedroom")
            elif captureCamera == kitchenCamera:
                controller.followPerson(x, y, w, "Kitchen")

def personDetection(captureCamera):
    while captureCamera.isOpened():
        # Reading the video stream
        ret, image = captureCamera.read()

        if ret:
            image = imutils.resize(image, width=min(400, image.shape[1]))

            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            (regions, _) = hog.detectMultiScale(image, winStride=(4, 4), padding=(8, 8), scale=1.01)

            drawregion(image, regions, captureCamera, _)

            # Showing the output Image
            cv2.imshow("Image", image)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break

    captureCamera.release()
    cv2.destroyAllWindows()


personDetection(kitchenCamera)
# personDetection(bedroomCamera)
