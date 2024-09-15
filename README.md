
Finanacial Price Prediction

Technologies Used
Python
FastAPI: For creating RESTful APIs.
gRPC: For high-performance communication between services.
Docker: For containerization of the application.
Kubernetes: For deploying and managing the service in a scalable manner.
Getting Started
Prerequisites
Python 3.9 or higher
Docker
Kubernetes (for deployment)
Installation
Clone the repository:

git clone https://github.com/arcada-uas/TAIS-Financial-Stock-Prices-Prediction.git
cd TAIS-Financial-Stock-Prices-Prediction/ingestion_service
Install dependencies:

pip install -r requirements.txt
Running the Service
Locally
Start the FastAPI server:

uvicorn app.main:app --host 0.0.0.0 --port 8000
Start the gRPC server:

python app/grpc_server.py
Using Docker
Build the Docker image:

docker build -t services:latest .
Run the Docker container:

docker run -p 8000:8000 -p 50051:50051 services:latest
Deploying to Kubernetes
Create a Kubernetes deployment file (e.g., deployment.yaml):


Apply the deployment:

kubectl apply -f deployment.yaml
Contributing
We welcome contributions to enhance the functionality and performance of this service. Please follow these steps to contribute:

Fork the repository.
Create a new branch (git checkout -b feature-branch).
Make your changes and commit them (git commit -am 'Add new feature').
Push to the branch (git push origin feature-branch).
Create a new Pull Request.
