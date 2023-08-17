# Use an official Python runtime as a parent image
FROM python:3.8-buster

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

RUN pip install --upgrade pip
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose a port for the service
ENV PORT=8081

# Run the command to start uvicorn
CMD uvicorn main:app --host 0.0.0.0 --port $PORT