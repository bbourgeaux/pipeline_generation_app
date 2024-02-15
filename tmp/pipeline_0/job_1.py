import random

# Function to generate random data
def generate_data(filename):
  with open(filename, 'wb') as f:
    for i in range(100000):
      f.write(str(random.randint(1, 100)).encode())

# Call the function to generate data
generate_data('data1.ext')