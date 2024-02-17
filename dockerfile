FROM python:3.8-slim-buster
WORKDIR /app

# Copy the requirements.txt file to our working directory /app
COPY app/requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy app's source code from host to your image filesystem
COPY app/ .

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV NAME ObjectDetection

CMD ["python", "app.py"]
