import os

def process_files(input_files, output_file):
    with open(input_files[0], 'r') as f1, open(input_files[1], 'r') as f2:
        content1 = f1.read()
        content2 = f2.read()

    with open(output_file, 'w') as f:
        f.write(content1)
        f.write(content2)

# Job 2
input_files = ['input1.txt', 'input2.txt']
output_file = 'output2.txt'

process_files(input_files, output_file)