# Use an official Python runtime as a parent image
FROM python:3.11-slim-buster

RUN apt-get update && apt-get install -y git build-essential \
    python3-dev portaudio19-dev

#get the latest version of pip
RUN pip install --upgrade pip

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Expose the port that the FastAPI application runs on
EXPOSE 8000

# Run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]