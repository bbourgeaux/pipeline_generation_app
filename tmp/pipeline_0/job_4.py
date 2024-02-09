
import numpy as np
import tensorflow as tf
from keras.applications.resnet50 import ResNet50, preprocess_input
from keras.preprocessing import image
from keras.applications.resnet50.preprocessing import decode_predictions

# Load the pre-trained model
model = ResNet50(weights='imagenet')

# Load the input image
img = image.load_img('example1.jpg', target_size=(224, 224))
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)
x = preprocess_input(x)

# Make predictions
preds = model.predict(x)

# Decode the predictions
top_preds = decode_predictions(preds, top=5)[0]

# Write the classification results to a file
with open('example1_classification.txt', 'w') as f:
    for i, pred in enumerate(top_preds):
        f.write(f"{i+1}. {pred[1]} ({pred[2]*100:.2f}%)\n")

