
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.preprocessing.image import ImageDataGenerator

# Set the path to the input data
input_dir = 'input_data/'

# Define the output path
output_dir = 'output_data/'

# Create input and output directories if they don't exist
if not os.path.exists(input_dir):
    os.makedirs(input_dir)

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Define the model architecture
model = Sequential()
model.add(Dense(64, input_dim=128, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

# Compile the model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Define the data generators
train_datagen = ImageDataGenerator(
    rescale=1./255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest')

test_datagen = ImageDataGenerator(rescale=1./255)

# Define the train and test data generators
train_generator = train_datagen.flow_from_directory(
    input_dir,
    target_size=(128, 128),
    batch_size=32,
    class_mode='binary')

test_generator = test_datagen.flow_from_directory(
    input_dir,
    target_size=(128, 128),
    batch_size=32,
    class_mode='binary')

# Train the model
model.fit_generator(
    train_generator,
    steps_per_epoch=len(train_generator),
    epochs=10,
    validation_data=test_generator,
    validation_steps=len(test_generator))

# Save the trained model
model.save(output_dir + 'example1_model.h5')

