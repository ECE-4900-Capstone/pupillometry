import cv2
image = cv2.imread('opencv_eye1.png')

image = cv2.resize(image, (300,300))

cv2.imwrite("edited.png",image)