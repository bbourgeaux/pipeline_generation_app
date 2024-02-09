import os

# Read the input file
with open('food_data.txt', 'r') as f:
    data = f.read()

# Remove duplicates
clean_data = set(data)

# Convert all items to lowercase
clean_data = {item.lower() for item in clean_data}

# Write to output file
with open('clean_food_data.txt', 'w') as f:
    f.write('\n'.join(clean_data))

