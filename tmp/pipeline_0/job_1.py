import numpy as np
from PIL import Image

# Load the image
image = Image.open('example1.jpg')

# Convert the image to grayscale
gray_image = image.convert('L')

# Resize the image
resized_image = gray_image.resize((256, 256))

# Convert the image to a numpy array
np_image = np.array(resized_image)

# Apply Gaussian filter to the image
kernel = np.ones((5, 5), np.uint8)
blurred_image = cv2.GaussianBlur(np_image, kernel, 0)

# Apply edge detection to the image
edges = cv2.Canny(blurred_image, 100, 200)

# Save the preprocessed image
cv2.imwrite('example1_preprocessed.jpg', edges)

