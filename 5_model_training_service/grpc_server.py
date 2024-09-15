from concurrent import futures
import grpc
import bentoml_service_pb2
import bentoml_service_pb2_grpc
import logging
import pandas as pd
from app.services.data_broker_service import DataBrokerService
from app.services.data_prediction_service import DataPredictionService
from app.services.data_rmse_service import DataRMSEService


class BentoMLServiceServicer(bentoml_service_pb2_grpc.BentoMLServiceServicer):
    def __init__(self):
        self.data_broker_service = DataBrokerService()
        self.data_prediction_service = DataPredictionService()
        self.data_rmse_service = DataRMSEService()

    def GetDataHead(self, request, context):
        logging.info("GetDataHead called")
        try:
            data_head = self.data_broker_service.get_data_head()
            logging.info(f"data_head: {data_head}")
            response = bentoml_service_pb2.DataHeadResponse()
            for row in data_head:
                logging.info(f"Processing row: {row}")
                map_entry = response.data_head.add()
                for key, value in row.items():
                    if isinstance(value, pd.Timestamp):
                        value = value.strftime('%Y-%m-%d %H:%M:%S')
                    logging.info(f"Adding key: {key}, value: {value}")
                    map_entry.row[key] = str(value)
            return response
        except Exception as e:
            logging.error(f"Error in GetDataHead: {e}")
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return bentoml_service_pb2.DataHeadResponse()

    def GetPredictions(self, request, context):
        predictions = self.data_prediction_service.get_predictions()
        return bentoml_service_pb2.PredictionsResponse(predictions=predictions)

    def GetRMSE(self, request, context):
        rmse = self.data_rmse_service.get_rmse()
        return bentoml_service_pb2.RMEResponse(rmse=rmse)

    def GetInference(self, request, context):
        data_head = self.data_broker_service.get_data_head()
        predictions = self.data_prediction_service.get_predictions()
        rmse = self.data_rmse_service.get_rmse()

        response = bentoml_service_pb2.InferenceResponse()
        for row in data_head:
            map_entry = response.data_head.add()
            for key, value in row.items():
                if isinstance(value, pd.Timestamp):
                    value = value.strftime('%Y-%m-%d %H:%M:%S')
                map_entry.row[key] = str(value)

        response.predictions.extend(predictions)
        response.rmse = rmse
        return response


def serve():
    logging.basicConfig(level=logging.INFO)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    bentoml_service_pb2_grpc.add_BentoMLServiceServicer_to_server(
        BentoMLServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    logging.info("Server started on port 50051")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
