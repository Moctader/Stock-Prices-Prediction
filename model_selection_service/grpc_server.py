from concurrent import futures
import grpc
from app.grpc import feature_pb2_grpc, feature_pb2
from app.services.feature_service import FeatureService
from app.db.session import get_db


class GRPCFeatureService(feature_pb2_grpc.FeatureServiceServicer):
    async def Process(self, request, context):
        time_series_data = request.data
        db = next(get_db())
        feature_service = FeatureService()
        processed_data, _ = await feature_service.process_data(time_series_data, db)
        if not processed_data:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Data processing failed")
            return feature_pb2.ProcessResponse()

        response = feature_pb2.ProcessResponse()
        for data in processed_data:
            response.data.add(
                timestamp=data['timestamp'],
                date=data['date'],
                open=data['open'],
                high=data['high'],
                low=data['low'],
                close=data['close'],
                volume=data['volume'],
                adjusted_close=data['adjusted_close'],
                prev_close=data['prev_close'],
                change=data['change'],
                change_p=data['change_p']
            )
        return response


def serve():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    feature_pb2_grpc.add_FeatureServiceServicer_to_server(
        GRPCFeatureService(), server)
    server.add_insecure_port('[::]:8061')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
