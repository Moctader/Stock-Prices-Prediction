# Data Ingestion Service

## Overview

The Data Ingestion Service is the initial step in our MLOps pipeline. This service is responsible for collecting, cleaning, transforming, and preparing data from various sources. The objective is to ensure that the ingested data is of high quality, consistent, and relevant to the machine learning problems we are addressing.

## Responsibilities

- **Data Collection**: Gather data from diverse sources including databases, APIs, and flat files.
- **Data Cleaning**: Remove errors and inconsistencies to ensure data quality.
- **Data Transformation**: Convert data into a suitable format for analysis.
- **Data Preparation**: Prepare data for further processing in the ML pipeline.

## Technologies Used

- **Python**
- **FastAPI**: For creating RESTful APIs.
- **gRPC**: For high-performance communication between services.
- **Docker**: For containerization of the application.
- **Kubernetes**: For deploying and managing the service in a scalable manner.

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Docker
- Kubernetes (for deployment)

### Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/arcada-uas/TAIS-Financial-Stock-Prices-Prediction.git
    cd TAIS-Financial-Stock-Prices-Prediction/ingestion_service
    ```

2. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

### Running the Service

#### Locally

1. **Start the FastAPI server**:
    ```sh
    uvicorn app.main:app --host 0.0.0.0 --port 8000
    ```

2. **Start the gRPC server**:
    ```sh
    python app/grpc_server.py
    ```

#### Using Docker

1. **Build the Docker image**:
    ```sh
    docker build -t arcada-uas/ingestion-service:latest .
    ```

2. **Run the Docker container**:
    ```sh
    docker run -p 8000:8000 -p 50051:50051 your-docker-repo/ingestion-service:latest
    ```

#### Deploying to Kubernetes

1. **Create a Kubernetes deployment file** (e.g., `deployment.yaml`):
    ```yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: ingestion-service
    spec:
      replicas: 1
      selector:
        matchLabels:
          app: ingestion-service
      template:
        metadata:
          labels:
            app: ingestion-service
        spec:
          containers:
          - name: ingestion-service
            image: your-docker-repo/ingestion-service:latest
            ports:
            - containerPort: 8000
            - containerPort: 50051
            env:
            - name: ENV
              value: "production"
    ```

2. **Apply the deployment**:
    ```sh
    kubectl apply -f deployment.yaml
    ```

## Contributing

We welcome contributions to enhance the functionality and performance of this service. Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.


