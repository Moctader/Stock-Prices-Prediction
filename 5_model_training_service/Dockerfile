# Use an official Debian runtime as a parent image
FROM debian:stable-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV BENTOML_HOME=/bentoml

# Install Python and other dependencies
RUN apt-get update \
    && apt-get install -y python3 python3-pip python3-venv \
    && apt-get clean

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Create and activate a virtual environment
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Create a directory for BentoML
RUN mkdir -p /bentoml

# Expose the port the app runs on
EXPOSE 8062

# Run BentoML serve command
CMD ["bentoml", "serve", "app.main.py:Start", "--reload"]