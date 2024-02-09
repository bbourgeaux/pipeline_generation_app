
import numpy as np
import cv2

# Load the preprocessed image
img = cv2.imread('example1_preprocessed.jpg')

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply a Gaussian blur to reduce noise
gray = cv2.GaussianBlur(gray, (5, 5), 0)

# Apply edge detection using Canny method
edges = cv2.Canny(gray, 50, 150)

# Apply a dilation operation to connect nearby edges
edges = cv2.dilate(edges, (3, 3), 0)

# Apply a threshold operation to obtain a binary image
thresh = cv2.threshold(edges, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Apply morphological closing to remove small objects
kernel = np.ones((5, 5), np.uint8)
thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

# Apply a dilation operation to connect nearby edges
thresh = cv2.dilate(thresh, (3, 3), 0)

# Save the extracted features image
cv2.imwrite('example1_features.jpg', thresh)

