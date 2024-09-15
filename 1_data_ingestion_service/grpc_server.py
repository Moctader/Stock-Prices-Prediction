from concurrent import futures
import grpc
from app.grpc import ingestion_pb2_grpc
from app.services.ingestion_service import IngestionService
from app.db.session import get_db


class GRPCIngestionService(ingestion_pb2_grpc.IngestionServiceServicer):
    async def Ingest(self, request, context):
        symbol = request.symbol
        db = next(get_db())
        ingestion_service = IngestionService()
        financial_data, message = await ingestion_service.ingest_data(symbol, db)
        if not financial_data:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(message)
            return ingestion_pb2.IngestResponse(message=message)
        return ingestion_pb2.IngestResponse(message="Data ingested successfully")


def serve():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    ingestion_pb2_grpc.add_IngestionServiceServicer_to_server(
        GRPCIngestionService(), server)
    server.add_insecure_port('[::]:8061')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
