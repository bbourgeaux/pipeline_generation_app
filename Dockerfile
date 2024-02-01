# syntax=docker/dockerfile:1

# Use an official Python runtime as the base image
FROM python:3.8

# Set the working directory in the container
WORKDIR /pipeline-generation-app

# Copy the requirements.txt file and install the Python dependencies
COPY requirements.txt requirements.txt
RUN pip3.8 install -r requirements.txt

# Copy the entire project into the container
COPY . .

# Start the Flask app when the container launches
CMD [ "python3.8", "-m" , "flask", "run", "--host=0.0.0.0"]
