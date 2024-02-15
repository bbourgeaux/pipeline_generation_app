import os

# Job 1
def job_1(input_files, output_file):
    # code for Job 1
    pass

# Job 2
def job_2(input_files, output_file):
    # code for Job 2
    pass

# Job 3
def job_3(input_files, output_file):
    # code for Job 3
    pass

# Main function
def main():
    # Read input files
    input_files = os.listdir("input")
    input1, input2 = input_files[:2]

    # Perform Jobs 1 to 3
    job_1(input1, "output1.txt")
    job_2(input1, "output2.txt")
    job_3(input1, "output3.txt")

if __name__ == "__main__":
    main()