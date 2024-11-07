from protogen import helloworld_pb2_grpc
from protogen import helloworld_pb2
import grpc


def main():
    with grpc.insecure_channel("localhost:9000") as channel:
        stub = helloworld_pb2_grpc.HelloWorldStub(channel)
        res = stub.SayHello(helloworld_pb2.Greetings(name="lydia", body="Hello, World!"))
        print("Greeter client received: " + res.response)

        for res in stub.SayHelloStream(helloworld_pb2.Greetings(name="lydia", body="Hello, World!")):
            print("Greeter client received: " + res.response)


if __name__ == "__main__":
    main()
