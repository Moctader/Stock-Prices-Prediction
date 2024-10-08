# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import bentoml_service_pb2 as bentoml__service__pb2

GRPC_GENERATED_VERSION = '1.64.1'
GRPC_VERSION = grpc.__version__
EXPECTED_ERROR_RELEASE = '1.65.0'
SCHEDULED_RELEASE_DATE = 'June 25, 2024'
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    warnings.warn(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in bentoml_service_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
        + f' This warning will become an error in {EXPECTED_ERROR_RELEASE},'
        + f' scheduled for release on {SCHEDULED_RELEASE_DATE}.',
        RuntimeWarning
    )


class BentoMLServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetDataHead = channel.unary_unary(
                '/bentoml.BentoMLService/GetDataHead',
                request_serializer=bentoml__service__pb2.Empty.SerializeToString,
                response_deserializer=bentoml__service__pb2.DataHeadResponse.FromString,
                _registered_method=True)
        self.GetPredictions = channel.unary_unary(
                '/bentoml.BentoMLService/GetPredictions',
                request_serializer=bentoml__service__pb2.Empty.SerializeToString,
                response_deserializer=bentoml__service__pb2.PredictionsResponse.FromString,
                _registered_method=True)
        self.GetRMSE = channel.unary_unary(
                '/bentoml.BentoMLService/GetRMSE',
                request_serializer=bentoml__service__pb2.Empty.SerializeToString,
                response_deserializer=bentoml__service__pb2.RMEResponse.FromString,
                _registered_method=True)
        self.GetInference = channel.unary_unary(
                '/bentoml.BentoMLService/GetInference',
                request_serializer=bentoml__service__pb2.Empty.SerializeToString,
                response_deserializer=bentoml__service__pb2.InferenceResponse.FromString,
                _registered_method=True)


class BentoMLServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetDataHead(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetPredictions(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetRMSE(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetInference(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_BentoMLServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetDataHead': grpc.unary_unary_rpc_method_handler(
                    servicer.GetDataHead,
                    request_deserializer=bentoml__service__pb2.Empty.FromString,
                    response_serializer=bentoml__service__pb2.DataHeadResponse.SerializeToString,
            ),
            'GetPredictions': grpc.unary_unary_rpc_method_handler(
                    servicer.GetPredictions,
                    request_deserializer=bentoml__service__pb2.Empty.FromString,
                    response_serializer=bentoml__service__pb2.PredictionsResponse.SerializeToString,
            ),
            'GetRMSE': grpc.unary_unary_rpc_method_handler(
                    servicer.GetRMSE,
                    request_deserializer=bentoml__service__pb2.Empty.FromString,
                    response_serializer=bentoml__service__pb2.RMEResponse.SerializeToString,
            ),
            'GetInference': grpc.unary_unary_rpc_method_handler(
                    servicer.GetInference,
                    request_deserializer=bentoml__service__pb2.Empty.FromString,
                    response_serializer=bentoml__service__pb2.InferenceResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'bentoml.BentoMLService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('bentoml.BentoMLService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class BentoMLService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetDataHead(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/bentoml.BentoMLService/GetDataHead',
            bentoml__service__pb2.Empty.SerializeToString,
            bentoml__service__pb2.DataHeadResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetPredictions(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/bentoml.BentoMLService/GetPredictions',
            bentoml__service__pb2.Empty.SerializeToString,
            bentoml__service__pb2.PredictionsResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetRMSE(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/bentoml.BentoMLService/GetRMSE',
            bentoml__service__pb2.Empty.SerializeToString,
            bentoml__service__pb2.RMEResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetInference(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/bentoml.BentoMLService/GetInference',
            bentoml__service__pb2.Empty.SerializeToString,
            bentoml__service__pb2.InferenceResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
