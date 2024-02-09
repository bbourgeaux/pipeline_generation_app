
import os
import cv2
import numpy as np

# Resize images
def resize_image(image, width, height):
    return cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)

# Crop images
def crop_image(image, x, y, width, height):
    return image[y:y+height, x:x+width]

# Preprocess images
def preprocess_images(input_dir, output_dir):
    for filename in os.listdir(input_dir):
        if filename.endswith('.jpg'):
            image = cv2.imread(os.path.join(input_dir, filename))
            image = resize_image(image, 256, 256) # resize image
            image = crop_image(image, 64, 64, 192, 192) # crop image
            cv2.imwrite(os.path.join(output_dir, filename), image)

# Main function
def main():
    input_dir = 'family_images/'
    output_dir = 'preprocessed_images/'
    preprocess_images(input_dir, output_dir)

if __name__ == '__main__':
    main()

