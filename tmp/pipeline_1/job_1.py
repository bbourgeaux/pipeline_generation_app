import os

# Function to create data from input resource
def create_data(input_file, output_file):
    # Read input file
    with open(input_file, 'r') as f:
        data = f.read()

    # Write data to output file
    with open(output_file, 'w') as f:
        f.write(data)

# Main function to execute job
def main():
    # Define input and output files
    input_file = "input_file.txt"
    output_file = "output_file.txt"

    # Call create_data function
    create_data(input_file, output_file)

# Execute main function
if __name__ == '__main__':
    main()