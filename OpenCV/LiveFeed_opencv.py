# import the opencv library
import cv2
  
  
# define a video capture object
integratedCamera = cv2.VideoCapture(0)
IP_camera1 = cv2.VideoCapture("http://130.240.105.144/cgi-bin/mjpeg?resolution=1920x1080&amp;framerate=30&amp;quality=1")
  
while(True):
      
    # Capture the video frame
    # by frame
    ret, frame = IP_camera1.read()
  
    # Display the resulting frame
    cv2.imshow('frame', frame)
      
    # the 'q' button is set as the quit button
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()