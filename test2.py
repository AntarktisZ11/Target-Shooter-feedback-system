import numpy as np
import cv2

# Read image as gray-scale
img = cv2.imread("Target\Webp.net-resizeimage.jpg", cv2.IMREAD_COLOR)
# img = cv2.imread("Target\moose.jpg", cv2.IMREAD_COLOR)
# Convert to gray-scale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Blur the image to reduce noise
img_blur = cv2.medianBlur(gray, 1)
# Apply hough transform on the image
circles = cv2.HoughCircles(img_blur, cv2.HOUGH_GRADIENT, 1, 1, param1=200, param2=60, minRadius=5, maxRadius=40)
# Draw detected circles
if circles is not None:
    circles = np.mean(circles, axis=1)
    circles = np.uint16(np.around(circles))
    # for i in circles[0, :]:
    # Draw outer circle
    cv2.circle(img, (circles[0,0], circles[0,1]), circles[0,2], (0, 255, 0), 2)
    # Draw inner circle
    cv2.circle(img, (circles[0,0], circles[0,1]), 2, (0, 0, 255), 3)
# Show result image
cv2.imshow("Result Image", img)
cv2.waitKey()