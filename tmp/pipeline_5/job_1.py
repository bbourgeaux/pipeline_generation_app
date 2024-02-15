import os

input_dir = 'input_dir'
output_1 = 'output_1.txt'

def generate_first_file():
    os.makedirs(os.path.dirname(output_1), exist_ok=True)
    with open(output_1, 'w') as f:
        f.write('This is the first file.')

generate_first_file()