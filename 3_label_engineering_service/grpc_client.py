import grpc
from app.grpc import feature_pb2_grpc, feature_pb2


class GRPCClient:
    def __init__(self, host='localhost', port=8061):
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = feature_pb2_grpc.FeatureServiceStub(self.channel)

    def process_data(self, time_series_data: list):
        request = feature_pb2.ProcessRequest()
        for data in time_series_data:
            request.data.add(
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
        try:
            response = self.stub.Process(request)
            processed_data = [
                {
                    'timestamp': d.timestamp,
                    'date': d.date,
                    'open': d.open,
                    'high': d.high,
                    'low': d.low,
                    'close': d.close,
                    'volume': d.volume,
                    'adjusted_close': d.adjusted_close,
                    'prev_close': d.prev_close,
                    'change': d.change,
                    'change_p': d.change_p
                }
                for d in response.data
            ]
            return processed_data
        except grpc.RpcError as e:
            print(f'gRPC error: {e.code()} - {e.details()}')
            return None
