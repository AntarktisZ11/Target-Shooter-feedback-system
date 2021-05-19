import cv2

img = cv2.imread("Target\Webp.net-resizeimage.jpg", cv2.IMREAD_COLOR)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 180, 400)
cv2.imshow("Gray" ,gray)
cv2.imshow("Canny" ,edges)
cv2.waitKey()