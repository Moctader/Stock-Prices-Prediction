import grpc
import bentoml_service_pb2
import bentoml_service_pb2_grpc
import logging

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = bentoml_service_pb2_grpc.BentoMLServiceStub(channel)
        logging.info("Client connected to server on port 50051")

        # Get Data Head
        response = stub.GetDataHead(bentoml_service_pb2.Empty())
        logging.info("Data Head:")
        for row in response.data_head:
            logging.info(row.row)

        # Get Predictions
        response = stub.GetPredictions(bentoml_service_pb2.Empty())
        logging.info("Predictions: %s", response.predictions)

        # Get RMSE
        response = stub.GetRMSE(bentoml_service_pb2.Empty())
        logging.info("RMSE: %s", response.rmse)

        # Get Inference
        response = stub.GetInference(bentoml_service_pb2.Empty())
        logging.info("Inference Data Head:")
        for row in response.data_head:
            logging.info(row.row)
        logging.info("Inference Predictions: %s", response.predictions)
        logging.info("Inference RMSE: %s", response.rmse)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # run()
