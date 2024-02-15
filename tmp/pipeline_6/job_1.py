# Importing necessary libraries
import os
import shutil

# Function to perform first job
def first_job():
    # Reading input file
    with open('input.txt', 'r') as f_in:
        content = f_in.read()

    # Writing content to output file
    with open('output1.txt', 'w') as f_out:
        f_out.write(content)

# Calling the function
first_job()