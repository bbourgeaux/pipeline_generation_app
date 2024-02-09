import cv2
import numpy as np

# Load the input images
img1 = cv2.imread('family_images.jpg')
img2 = cv2.imread('family_images.png')

# Convert the images to grayscale
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur to reduce noise
blur1 = cv2.GaussianBlur(gray1, (15, 15), 0)
blur2 = cv2.GaussianBlur(gray2, (15, 15), 0)

# Apply thresholding to create a binary image
ret1, thresh1 = cv2.threshold(blur1, 200, 255, cv2.THRESH_BINARY)
ret2, thresh2 = cv2.threshold(blur2, 200, 255, cv2.THRESH_BINARY)

# Find contours in the binary image
contours1, _ = cv2.findContours(thresh1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours2, _ = cv2.findContours(thresh2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Draw a rectangle around each contour
for contour in contours1:
    x, y, w, h = cv2.boundingRect(contour)
    cv2.rectangle(img1, (x, y), (x+w, y+h), (0, 255, 0), 2)

for contour in contours2:
    x, y, w, h = cv2.boundingRect(contour)
    cv2.rectangle(img2, (x, y), (x+w, y+h), (0, 255, 0), 2)

# Save the output images
cv2.imwrite('classified_images.jpg', img1)
cv2.imwrite('classified_images.png', img2)

