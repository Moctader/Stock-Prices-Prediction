
# Quickstart

This quickstart demonstrates how to build a financial model service that provides stock price predictions and displays dataset information using BentoML. The service includes both REST API and gRPC endpoints.

## Prerequisites

Python 3.8+ and `pip` installed. See the [Python downloads page](https://www.python.org/downloads/) to learn more.

## Get started

Perform the following steps to run this project and deploy it to BentoCloud.

1. Install the required dependencies:

   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

2. Serve your model as an HTTP server. This starts a local server at [http://localhost:8061](http://localhost:8061/), making your model accessible as a web service.

   ```bash
   bentoml serve main.py:Svc --reload
   ```

3. To serve the gRPC server, run the following command:

   ```bash
   python grpc_server.py
   ```

4. You can test the gRPC client by running:

   ```bash
   python grpc_client.py
   ```

5. Once your service is ready, you can deploy it to [BentoCloud](https://www.bentoml.com/cloud). Make sure you have [logged in to BentoCloud](https://docs.bentoml.com/en/latest/bentocloud/how-tos/manage-access-token.html) and run the following command to deploy it.

   ```bash
   bentoml deploy .
   ```

   **Note**: Alternatively, you can manually build a Bento, [containerize it with Docker](https://docs.bentoml.com/en/latest/guides/containerization.html), and deploy it in any Docker-compatible environment.

## API Endpoints

### REST API

1. **Get Data Head**

   ```bash
   curl -X POST "http://127.0.0.1:8061/get_data_head"
   ```

2. **Get Prediction and MSE**

   ```bash
   curl -X POST "http://127.0.0.1:8061/predict" -H "Content-Type: application/json" -d '{}'
   ```

### gRPC API

1. **Get Data Head**

   Run the gRPC client:

   ```bash
   python grpc_client.py
   ```

## Running with Docker Compose

You can run both the gRPC server and client using Docker Compose. Follow these steps:

### 1. Unified Dockerfile

Create a Dockerfile named `Dockerfile.unified`:

```dockerfile
# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV BENTOML_HOME=/bentoml

# Install Python and other dependencies
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv curl && apt-get clean

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Create and activate a virtual environment
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install gRPC tools
RUN pip install grpcio grpcio-tools

# Expose the port the app runs on
EXPOSE 50051

# Copy the entrypoint script
COPY entrypoint.sh /app/entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Run the entrypoint script
CMD ["/app/entrypoint.sh"]
```

### 2. Entrypoint Script

Create a script named `entrypoint.sh`:

```bash
#!/bin/bash

# Start the gRPC server in the background
python grpc_server.py &
SERVER_PID=$!

# Wait for the gRPC server to start
echo "Waiting for gRPC server to start..."
sleep 10  # Adjust this time as necessary

# Run the gRPC client
python grpc_client.py

# Wait for the gRPC server process to finish
wait $SERVER_PID
```

Make the entrypoint script executable:

```bash
chmod +x entrypoint.sh
```

### 3. Docker Compose File

Create a `docker-compose.yml` file:

```yaml
version: '3.8'

services:
  grpc_service:
    build:
      context: .
      dockerfile: Dockerfile.unified
    ports:
      - "50051:50051"
    networks:
      - grpc_network

networks:
  grpc_network:
    driver: bridge
```

### 4. Running Docker Compose

To build and run the services using Docker Compose, use the following commands:

```bash
docker-compose down
docker-compose build
docker-compose up
```

### Clearing Docker Resources

If you need to stop and remove all containers, images, and volumes, use the following commands:

```bash
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
docker rmi $(docker images -q) -f
docker volume rm $(docker volume ls -q)
```

This `README.md` file provides a comprehensive guide to set up, run, and deploy your financial model service using BentoML, including both REST and gRPC endpoints. If you encounter any issues or need further assistance, feel free to reach out!
