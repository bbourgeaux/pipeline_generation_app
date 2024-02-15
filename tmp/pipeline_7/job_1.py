import os

def generate_resource(input_file, output_file):
    # Perform the job to generate a new resource
    with open(input_file, 'r') as f_in:
        data = f_in.read()
        with open(output_file, 'w') as f_out:
            f_out.write(data)

# Example usage
generate_resource('example1.ext', 'example2.ext')