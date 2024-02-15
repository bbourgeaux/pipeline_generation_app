import os
import shutil

input_dir = "/path/to/input/directory"
output_3_file = "output_3.txt"

# Check if input directory exists
if not os.path.exists(input_dir):
    print(f"Error: Input directory '{input_dir}' does not exist.")
    exit(1)

# Create output directory if it doesn't exist
output_dir = f"{os.path.basename(input_dir)}_output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Move all files from input directory to output directory
for file in os.listdir(input_dir):
    src_file = os.path.join(input_dir, file)
    dst_file = os.path.join(output_dir, file)
    shutil.move(src_file, dst_file)

# Generate third file
with open(os.path.join(output_dir, output_3_file), "w") as f:
    f.write("This is the third file generated from the input directory.")

print(f"Successfully generated third file '{output_3_file}'.")