# Financial Price Prediction

## Technologies Used
- **Python**
- **FastAPI:** For creating RESTful APIs.
- **gRPC:** For high-performance communication between services.
- **Docker:** For containerization of the application.
- **Kubernetes:** For deploying and managing the service in a scalable manner.

## Getting Started

### Prerequisites
- Python 3.9 or higher
- Docker
- Kubernetes (for deployment)

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/Moctader/Stock-Prices-Prediction/
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Running the Service

### Locally

1. Start the FastAPI server:

    ```bash
    uvicorn app.main:app --host 0.0.0.0 --port 8000
    ```

2. Start the gRPC server:

    ```bash
    python app/grpc_server.py
    ```

### Using Docker

1. Build the Docker image:

    ```bash
    docker build -t services:latest .
    ```

2. Run the Docker container:

    ```bash
    docker run -p 8000:8000 -p 50051:50051 services:latest
    ```

### Deploying to Kubernetes

1. Create a Kubernetes deployment file (e.g., `deployment.yaml`).

2. Apply the deployment:

    ```bash
    kubectl apply -f deployment.yaml
    ```

## Contributing
welcome contributions to enhance the functionality and performance of this service. Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch:

    ```bash
    git checkout -b feature-branch
    ```

3. Make your changes and commit them:

    ```bash
    git commit -am 'Add new feature'
    ```

4. Push to the branch:

    ```bash
    git push origin feature-branch
    ```

5. Create a new Pull Request.
