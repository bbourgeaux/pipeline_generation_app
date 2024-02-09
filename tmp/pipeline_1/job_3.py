
# Import necessary libraries
import os
from PIL import Image
from sklearn.cluster import KMeans

# Define path to input and output directories
input_dir = "feature_images"
output_dir = "classified_images"

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Define number of clusters for KMeans clustering
num_clusters = 3

# Load all images in input directory
images = []
for filename in os.listdir(input_dir):
    if filename.endswith(".jpg"):
        image = Image.open(os.path.join(input_dir, filename))
        images.append(image)

# Resize all images to a fixed size
max_width = max(image.width for image in images)
max_height = max(image.height for image in images)
for i, image in enumerate(images):
    image = image.resize((max_width, max_height), Image.ANTIALIAS)
    images[i] = image

# Convert all images to grayscale
for i, image in enumerate(images):
    image = image.convert("L")
    images[i] = image

# Convert all images to numpy arrays
images = [np.array(image) for image in images]

# Perform KMeans clustering on the images
kmeans = KMeans(n_clusters=num_clusters)
labels = kmeans.fit_predict(images)

# Save the labeled images to output directory
for i, label in enumerate(labels):
    filename = os.path.splitext(os.path.basename(input_dir + "/" + str(i) + ".jpg"))[0]
    output_file = os.path.join(output_dir, filename + "_" + str(label) + ".jpg")
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    images[i].save(output_file)

