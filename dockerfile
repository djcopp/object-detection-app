# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Copy the requirements.txt file to our working directory /app
COPY app/requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app's source code from your host to your image filesystem.
COPY app/ .

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV NAME ObjectDetection

# Run app.py when the container launches
CMD ["python", "./app.py"]
