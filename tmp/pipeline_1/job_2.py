
import os
import numpy as np
from PIL import Image
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Read the preprocessed images
preprocessed_images = os.listdir('preprocessed_images/')

# Initialize an empty list to store feature images
feature_images = []

# Define the path to the feature vectorizer
vectorizer_path = 'feature_vectorizer/'

# Create the feature vectorizer
vectorizer = CountVectorizer()

# Create the feature matrix and save it to a file
feature_matrix = vectorizer.fit_transform(preprocessed_images).toarray()
np.save(vectorizer_path + 'feature_matrix.npy', feature_matrix)

# Compute the cosine similarity between all pairs of feature vectors
similarity = cosine_similarity(feature_matrix)

# Create a new image for each pair of feature vectors with a similarity score
for i in range(len(preprocessed_images)):
    for j in range(i+1, len(preprocessed_images)):
        if similarity[i,j] > 0:
            # Combine the two feature vectors
            combined_vector = np.sum(feature_matrix[i:j+1,:], axis=0)
            # Normalize the combined vector
            normalized_vector = combined_vector / combined_vector.sum()
            # Create a new image from the normalized vector
            feature_image = np.zeros((256,256,3))
            for k in range(256):
                for l in range(256):
                    feature_image[k,l,:] = normalized_vector[k*256+l]
            # Save the feature image
            feature_images.append(feature_image)

# Save the feature images to a file
np.save(vectorizer_path + 'feature_images.npy', feature_images)

# Clean up the workspace
os.remove(vectorizer_path + 'feature_matrix.npy')

