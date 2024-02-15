import os

# Function for the first job
def first_job():
    with open("input.txt", "r") as f_in:
        with open("output1.txt", "w") as f_out:
            for line in f_in:
                f_out.write(line)

# Function for the second job
def second_job():
    with open("output1.txt", "r") as f_in:
        with open("output2.txt", "w") as f_out:
            f_out.write(f_in.read())

# Function for the third job
def third_job():
    with open("output2.txt", "r") as f_in:
        print(f_in.read())

# Call the functions in the order of the jobs
first_job()
second_job()
third_job()