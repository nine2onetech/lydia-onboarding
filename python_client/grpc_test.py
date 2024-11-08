from protogen import helloworld_pb2_grpc, helloworld_pb2, bike_pb2_grpc
from google.protobuf import empty_pb2
import grpc


def main():
    with grpc.insecure_channel("localhost:9000") as channel:
        # HelloWorld Service
        stub = helloworld_pb2_grpc.HelloWorldStub(channel)
        res = stub.SayHello(helloworld_pb2.Greetings(name="lydia", body="Hello, World!"))
        print("Greeter client received: " + res.response)

        for res in stub.SayHelloStream(helloworld_pb2.Greetings(name="lydia", body="Hello, World!")):
            print("Greeter client received: " + res.response)

        # Bike Service
        bike_stub = bike_pb2_grpc.BikeStub(channel)
        try:
            res = bike_stub.GetStationList(empty_pb2.Empty(), timeout=15)  # 15초 타임아웃
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.DEADLINE_EXCEEDED:
                print("Timeout occurred: The request took longer than the allowed 15 seconds.")
            else:
                print(f"gRPC error: {e.code()} - {e.details()}")
        else:
            print("How many stations?:", res.count)

        for res in bike_stub.GetRealTimeStationStatus(empty_pb2.Empty()):
            print("Station Name:", res.stn_name, "Bike count:", res.parked_bike_cnt)
        print("Done")


if __name__ == "__main__":
    main()
