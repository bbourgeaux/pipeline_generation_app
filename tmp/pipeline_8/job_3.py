import os

# define input files
input1_path = 'input1.txt'
input2_path = 'input2.txt'

# define output file
output3_path = 'output3.txt'

# define function to process input files and generate output
def process_files():
    with open(input1_path, 'r') as f1:
        with open(input2_path, 'r') as f2:
            with open(output3_path, 'w') as f3:
                f3.write(f1.read())
                f3.write(f2.read())

# call function to process files
process_files()

# delete input files
os.remove(input1_path)
os.remove(input2_path)

# print success message
print("Job 3 completed successfully.")