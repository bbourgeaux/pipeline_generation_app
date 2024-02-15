import random

def generate_random_data(input_file):
    with open(input_file, 'r') as f:
        data = f.read()

    # Generate random data
    random_data = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', k=len(data)))

    with open(input_file, 'w') as f:
        f.write(random_data)

# Call the function
generate_random_data('output1.ext')