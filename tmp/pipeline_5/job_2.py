import os

# Function to generate second file
def generate_second_file():
    # Get input directory
    input_dir = os.getcwd()

    # Get output file
    output_file = os.path.join(input_dir, 'output_2.txt')

    # Open output file
    with open(output_file, 'w') as output_file:
        # Write output message
        output_file.write('Generated second file: This job generates the second file from the input directory.\n')

# Call function to generate second file
generate_second_file()