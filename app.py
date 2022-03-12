#!/usr/bin/env python
# encoding: utf-8
import csv
import logging

from flask import Flask, jsonify, request

from fake_data import generate_data

logging.basicConfig(level=logging.DEBUG)

# Define file path and headers to use
FILE_PATH = "data.csv"
HEADERS = ['username', 'score']
# Check if data.csv exists with headers ['username', 'score']
# If not, create data.csv with specified headers
generate_data(FILE_PATH, HEADERS)
# Create the Flask application
app = Flask(__name__)


# Parses a csv file and returns a dictionary
def generate_dict(file):
    # Read data.csv using csv.reader
    reader = csv.reader(file)
    # Loop through each row, starting at the second row, and add to dictionary
    # This, in effect, removes the header row
    dict = {}
    for row in reader:
        if row[0] != HEADERS[0]:
            dict[row[0]] = int(row[1])
    # Return the dictionary
    return dict


# Create wrapper function to handle file opening and reading
# Takes a callback function as a parameter to process data
def read_file(callback):
    # Create return JSON object
    ret = jsonify({})
    # Attempt to open file specified by FILE_PATH for reading
    try:
        with open(FILE_PATH, 'r') as file:
            # Call callback function with a dict from generate_dict
            ret = callback(generate_dict(file))
            # Close file
            file.close()
    # Return error if file not found
    except FileNotFoundError:
        ret = jsonify({'error': 'File not found'})
    # Return the data
    return ret


# Create wrapper function to handle file opening, reading, and writing
# Takes a callback function as a parameter to manipulate data
def write_file(callback):
    # Create return JSON object
    ret = jsonify({})
    # Attempt to open file specified by FILE_PATH for reading and writing
    try:
        # Open file for reading
        dict = {}
        with open(FILE_PATH, 'r') as file:
            # Create dictionary from generate_dict
            dict = generate_dict(file)
            # Close file
            file.close()
        # Open file for writing
        with open(FILE_PATH, 'w') as file:
            # Call callback function with a dict from generate_dict
            dict = callback(dict)
            # Create a csv writer object and write the header
            writer = csv.DictWriter(file, fieldnames=HEADERS)
            writer.writeheader()
            # Loop through each key in the dictionary and write to file
            for key, value in dict.items():
                writer.writerow({
                    HEADERS[0]: key,
                    HEADERS[1]: value
                })
            # Close file
            file.close()
        # Return JSON object
        ret = jsonify({'success': 'Data successfully updated'})
    # Return error if file not found
    except FileNotFoundError:
        ret = jsonify({'error': 'File not found'})
    # Return the data
    return ret


# GET all data from file
@app.route('/', methods=['GET'])
def get_all():
    # Create callback function to pass to file handler
    def callback(dict):
        # Return JSON object
        return jsonify(dict)

    # Call and return from callback function with file handler
    return read_file(callback)


# GET the highest score and the respective username from file
@app.route('/highscore', methods=['GET'])
def get_highscores():
    # Create callback function to pass to file handler
    def callback(dict):
        # Create sorted list of scores
        sorted_scores = sorted(dict.values(), reverse=True)
        # Create sorted list of usernames
        sorted_usernames = sorted(dict.keys(), key=lambda x: dict[x], reverse=True)
        # Create dictionary to return from top 10 scores and usernames
        ret = {sorted_usernames[0]: sorted_scores[0]}
        # Return JSON object
        return jsonify(ret)

    # Call and return from callback function with file handler
    return read_file(callback)


# GET the score of the user with the given username
@app.route('/<username>', methods=['GET'])
def get_score(username):
    # Create callback function to pass to file handler
    def callback(dict):
        # Check if username is in dictionary
        if username in dict:
            # Return JSON object
            return jsonify({username: dict[username]})
        else:
            # Return error
            return jsonify({'error': 'Username not found'})

    # Call and return from callback function with file handler
    return read_file(callback)


# POST a new score to the file
@app.route('/', methods=['POST'])
def post_score():
    # Create callback function to pass to file handler
    def callback(dict):
        try:
            # Get JSON from request
            username = request.form['username']
            score = int(request.form['score'])
            # Check if username is in dictionary
            if username in dict:
                # Check if score is greater than current score
                if score > dict[username]:
                    # Update score
                    dict[username] = score
            # Else Add new username and score
            else:
                dict[username] = score
        except:
            return jsonify({'error': 'Invalid JSON'})
        # Return dictionary
        return dict

    # Call and return from callback function with file handler
    return write_file(callback)


# DELETE the score of the user with the given username
@app.route('/', methods=['DELETE'])
def delete_score():
    # Create callback function to pass to file handler
    def callback(dict):
        # Check if username is in dictionary
        if request.json['username'] in dict:
            # Delete username
            del dict[request.json['username']]
        # Return dictionary
        return dict

    # Call and return from callback function with file handler
    return write_file(callback)


# The main function
if __name__ == '__main__':
    # Run the flask application
    app.run()
