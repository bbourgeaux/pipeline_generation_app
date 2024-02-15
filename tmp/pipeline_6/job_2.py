# Importing necessary libraries
import os

# Function to perform first job
def first_job():
    with open("input.txt", "r") as input_file:
        with open("output1.txt", "w") as output_file:
            content = input_file.read()
            output_file.write(content)

# Function to perform second job
def second_job():
    with open("output1.txt", "r") as input_file:
        with open("output2.txt", "w") as output_file:
            content = input_file.read()
            output_file.write(content)

# Function to perform third job
def third_job():
    with open("output2.txt", "r") as input_file:
        print(input_file.read())

# Main function to execute the jobs in sequence
def main():
    # Executing first job
    first_job()
    
    # Executing second job
    second_job()
    
    # Executing third job
    third_job()

# Calling the main function
if __name__ == "__main__":
    main()