# Use an official Debian runtime as a parent image
FROM debian:stable-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

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

# Ensure environment variables are set
ENV FASTAPI_PORT=8089
ENV GRPC_PORT=8061

# Expose the port for FastAPI
EXPOSE ${FASTAPI_PORT}

# Command to run FastAPI server
CMD export $(grep -v '^#' /app/.env | xargs) && \
    uvicorn app.main:app --host 0.0.0.0 --port ${FASTAPI_PORT}
