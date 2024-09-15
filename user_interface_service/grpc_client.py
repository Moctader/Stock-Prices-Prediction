import grpc
from app.grpc import interface_pb2_grpc, interface_pb2

class GRPCClient:
    def __init__(self, host='localhost', port=8061):
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = interface_pb2_grpc.InterfaceServiceStub(self.channel)

    def get_data(self, symbol: str):
        request = interface_pb2.GetStockRequest(symbol=symbol)
        try:
            if symbol == "AAPL":
                response = self.stub.GetAAPLData(request)
            elif symbol == "MSFT":
                response = self.stub.GetMSFTData(request)
            elif symbol == "GOOGL":
                response = self.stub.GetGOOGLData(request)
            elif symbol == "AMZN":
                response = self.stub.GetAMZNData(request)
            elif symbol == "TSLA":
                response = self.stub.GetTSLAData(request)
            elif symbol == "FB":
                response = self.stub.GetFBData(request)
            else:
                raise ValueError("Unsupported symbol")

            return response.data if response else None
        except grpc.RpcError as e:
            print(f'gRPC error: {e.code()} - {e.details()}')
            return None
