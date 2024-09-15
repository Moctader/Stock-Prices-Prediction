import grpc
from app.grpc import ingestion_pb2_grpc, ingestion_pb2


class GRPCClient:
    def __init__(self, host='localhost', port=8061):
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = ingestion_pb2_grpc.IngestionServiceStub(self.channel)

    def ingest_data(self, symbol: str):
        request = ingestion_pb2.IngestRequest(symbol=symbol)
        try:
            response = self.stub.Ingest(request)
            return response.message
        except grpc.RpcError as e:
            print(f'gRPC error: {e.code()} - {e.details()}')
            return None
