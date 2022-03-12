#!/usr/bin/env python
# encoding: utf-8
import csv
import random

from faker import Faker


# Create a csv file with 100 lines of data
# Takes in a filepath and a list of headers as arguments
def generate_data(filename, headers):
    # Create a faker object
    fake = Faker()
    # Attempt to open the defined file in write mode
    try:
        with open(filename, 'w') as csvfile:
            # Create a csv writer object and write the header
            fieldnames = ['username', 'score']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            # Write 100 lines of data using the faker and random
            for i in range(100):
                writer.writerow({
                    headers[0]: fake.user_name(),
                    headers[1]: random.randint(0, 1000)
                })
            # Close the file
            csvfile.close()
    # Handle the exception if file is not found
    except FileNotFoundError:
        print("There has been an unexpected error opening the file. Please try again.")


# Check specified file exists and has correct headers
# Takes in a filepath and a list of headers as arguments
def check_file(filepath, headers):
    try:
        # Open data.csv
        with open(filepath, 'r') as f:
            # Read data.csv and check headers
            parser = csv.reader(f)
            curr_headers = next(parser)
            # Raise exception if headers are incorrect
            if curr_headers != headers:
                raise NameError('Incorrect headers')
            # Else close file
            else:
                f.close()
    # If data.csv does not exist, or has incorrect headers, create a new one
    except:
        generate_data(filepath, headers)


# Main function with name
if __name__ == '__main__':
    # Create a list of headers
    headers = ['username', 'score']
    # Check if data.csv exists, if not create one
    generate_data('data.csv', headers)
