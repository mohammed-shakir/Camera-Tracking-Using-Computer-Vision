import cv2

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
prev_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
threshold = 1000

while True:
# Read the next frame
ret, frame = cap.read()
# Convert the next frame to grayscale
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# Calculate the absolute difference between the two grayscale frames
diff = cv2.absdiff(prev_gray, gray)

# Threshold the difference image to identify regions of the image that have changed significantly
thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]

# Count the number of non-zero pixels in the thresholded image
count = cv2.countNonZero(thresh)

# If the number of changed pixels is above the threshold, this indicates motion
if count > threshold:
    # Send the current frame
    # ...

    # Update the threshold for the number of changed pixels
    # This can be adjusted based on the camera's environment and desired sensitivity
    threshold = count // 4

# Update the previous frame
prev_gray = gray

# Display the difference image
cv2.imshow("Difference", diff)

# Break the loop if the user presses the 'q' key
if cv2.waitKey(1) & 0xFF == ord('q'):
    break
    
cap.release()
cv2.destroyAllWindows()
