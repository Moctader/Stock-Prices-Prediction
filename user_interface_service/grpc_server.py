from concurrent import futures
import grpc
from app.grpc import interface_pb2_grpc, interface_pb2
from app.services.interface_service import InterfaceService
from app.db.session import get_db

class GRPCInterfaceService(interface_pb2_grpc.InterfaceServiceServicer):
    async def GetAAPLData(self, request, context):
        return await self.get_data(request, context, "AAPL")

    async def GetMSFTData(self, request, context):
        return await self.get_data(request, context, "MSFT")

    async def GetGOOGLData(self, request, context):
        return await self.get_data(request, context, "GOOGL")

    async def GetAMZNData(self, request, context):
        return await self.get_data(request, context, "AMZN")

    async def GetTSLAData(self, request, context):
        return await self.get_data(request, context, "TSLA")

    async def GetFBData(self, request, context):
        return await self.get_data(request, context, "FB")

    async def get_data(self, request, context, symbol):
        db = next(get_db())
        interface_service = InterfaceService()
        data, message = await interface_service.get_data(symbol, db)
        if not data:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(message)
            return interface_pb2.GetStockResponse()
        return interface_pb2.GetStockResponse(data=[
            interface_pb2.StockData(
                date=str(item.date),
                open=item.open,
                high=item.high,
                low=item.low,
                close=item.close,
                adjusted_close=item.adjusted_close,
                volume=item.volume,
                prev_close=item.prev_close,
                change=item.change,
                change_p=item.change_p
            ) for item in data
        ])

def serve():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    interface_pb2_grpc.add_InterfaceServiceServicer_to_server(
        GRPCInterfaceService(), server)
    server.add_insecure_port('[::]:8061')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
