import cv2
import numpy as np
import winsound

# Set the video capture source (0 for webcam)
video_source = 0

# Set the alarm duration (in seconds)
alarm_duration = 1

# Initialize the video capture
cap = cv2.VideoCapture(video_source)

# Read the first frame
ret, frame = cap.read()
prev_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# Set initial motion detected flag
motion_detected = False

while True:
    # Read the current frame
    ret, frame = cap.read()
    if not ret:
        break

    # Convert current frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Compute the absolute difference between the current and previous frame
    frame_diff = cv2.absdiff(prev_gray, gray)

    # Apply a threshold to the frame difference
    _, thresh = cv2.threshold(frame_diff, 30, 255, cv2.THRESH_BINARY)

    # Apply morphological operations to remove noise
    kernel = np.ones((5, 5), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    # Find contours of the thresholded image
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Check if any contour area exceeds a certain threshold
    motion_detected = False
    for contour in contours:
        if cv2.contourArea(contour) > 1000:
            motion_detected = True
            break

    # Play alarm sound if motion is detected
    if motion_detected:
        print("Motion Detected!")
        winsound.Beep(1000, 1000 * alarm_duration)

    # Display the current frame
    cv2.imshow('Motion Detection', frame)

    # Update the previous frame
    prev_gray = gray

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close the OpenCV windows
cap.release()
cv2.destroyAllWindows()
