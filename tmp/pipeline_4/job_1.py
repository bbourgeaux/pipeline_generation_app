import csv
import hashlib

# function to remove duplicates from a list
def remove_duplicates(lst):
    return list(set(lst))

# function to clean the dataset
def clean_data(data):
    # remove duplicates
    data = remove_duplicates(data)
    # clean inconsistencies
    data = [d for d in data if d[0] != '']
    return data

# function to hash a string
def hash_string(s):
    return hashlib.md5(s.encode('utf-8')).hexdigest()

# function to remove inconsistencies
def remove_inconsistencies(data):
    data = [(hash_string(d[0]), d[1]) for d in data if d[0] != '']
    return [(k, v) for k, v in dict(sorted(data, key=lambda x: x[0]))]

# main function
def main():
    # read the input file
    with open('data.csv', 'r') as f:
        data = [line.strip().split(',') for line in f.readlines()]

    # clean the dataset
    data = clean_data(data)

    # remove inconsistencies
    data = remove_inconsistencies(data)

    # write the output file
    with open('clean_data.csv', 'w') as f:
        for d in data:
            f.write(f'{d[0]},{d[1]}\n')

if __name__ == '__main__':
    main()