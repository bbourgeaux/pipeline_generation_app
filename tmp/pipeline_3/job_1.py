import os

def generate_file(input_path, output_path):
    with open(input_path, 'r') as f:
        data = f.read()
    with open(output_path, 'w') as f:
        f.write('Generate file : This Job generates a new file.')

generate_file('example.ext', 'new_file.ext')