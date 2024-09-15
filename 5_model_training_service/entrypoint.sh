#!/bin/bash

# Function to clean up background processes
cleanup() {
    echo "Cleaning up..."
    kill -SIGTERM "$SERVER_PID" 2>/dev/null
    wait "$SERVER_PID" 2>/dev/null
}

# Trap SIGTERM and SIGINT signals to run the cleanup function
trap cleanup SIGTERM SIGINT

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
